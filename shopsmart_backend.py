import os
import random
import re
from datetime import datetime
from typing import List, Dict, Any

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func, JSON
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from faker import Faker

# Configuration
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-super-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///shopsmart.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DEBUG = True
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')

# Flask Application Setup
app = Flask(__name__)
app.config.from_object(Config)

# Database and Extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

# Database Models
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy='dynamic')

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # Enhanced product attributes
    brand = db.Column(db.String(100))
    stock_quantity = db.Column(db.Integer, default=0)
    features = db.Column(JSON)
    tags = db.Column(JSON)
    
    # Recommendation and matching attributes
    match_percentage = db.Column(db.Integer, default=0)
    popularity_score = db.Column(db.Float, default=0.0)
    
    # Tracking and media
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': f"${self.price:.2f}",
            'category': self.category.name if self.category else None,
            'brand': self.brand,
            'features': self.features,
            'match_percentage': self.match_percentage,
            'image_url': self.image_url or 'default_image.jpg'
        }

class SearchHistory(db.Model):
    __tablename__ = 'search_histories'
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Optional user preferences
    preferred_categories = db.Column(JSON)
    search_histories = db.relationship('SearchHistory', backref='user', lazy='dynamic')

# Utility Functions
def generate_product_features(category):
    feature_templates = {
        'Electronics': [
            'Battery Life', 'Screen Resolution', 'Connectivity', 
            'Processor Speed', 'Memory Capacity'
        ],
        'Fashion': [
            'Material', 'Size Range', 'Color Options', 
            'Style', 'Fit Type'
        ],
        'Home & Living': [
            'Dimensions', 'Material', 'Color', 
            'Care Instructions', 'Special Features'
        ]
    }
    return random.sample(feature_templates.get(category, []), 3)

def populate_database():
    # Create Categories
    categories_data = ['Electronics', 'Fashion', 'Home & Living']
    existing_categories = Category.query.all()
    
    if not existing_categories:
        for cat_name in categories_data:
            category = Category(name=cat_name)
            db.session.add(category)
        db.session.commit()

    # Clear existing products
    Product.query.delete()
    
    fake = Faker()
    categories = Category.query.all()

    # Generate 100 Products
    products = []
    for _ in range(100):
        category = random.choice(categories)
        product = Product(
            name=fake.catch_phrase(),
            description=fake.paragraph(nb_sentences=3),
            price=round(random.uniform(50, 500), 2),
            category_id=category.id,
            brand=fake.company(),
            stock_quantity=random.randint(10, 500),
            features=generate_product_features(category.name),
            tags=[category.name.lower(), 'trending'],
            match_percentage=random.randint(70, 100),
            popularity_score=random.uniform(0.5, 5.0),
            image_url=f"https://via.placeholder.com/300x400?text={category.name.replace(' ', '+')}"
        )
        products.append(product)

    db.session.add_all(products)
    db.session.commit()
    print(f"Populated database with {len(products)} products!")

# Search and Recommendation Utility
def advanced_search(
    query: str = '', 
    category: str = '', 
    min_price: float = None, 
    max_price: float = None,
    sort_by: str = 'match_percentage'
) -> List[Dict[str, Any]]:
    """Advanced product search with multiple filters."""
    try:
        # Base query
        search_query = Product.query

        # Category filter
        if category:
            category_obj = Category.query.filter_by(name=category).first()
            if category_obj:
                search_query = search_query.filter_by(category_id=category_obj.id)

        # Price range filter
        if min_price is not None:
            search_query = search_query.filter(Product.price >= min_price)
        if max_price is not None:
            search_query = search_query.filter(Product.price <= max_price)

        # Text search across name and description
        if query:
            search_query = search_query.filter(
                func.lower(Product.name).contains(query.lower()) | 
                func.lower(Product.description).contains(query.lower())
            )

        # Sorting
        if sort_by == 'price_low':
            search_query = search_query.order_by(Product.price.asc())
        elif sort_by == 'price_high':
            search_query = search_query.order_by(Product.price.desc())
        else:
            search_query = search_query.order_by(Product.match_percentage.desc())

        # Limit results
        results = search_query.limit(20).all()
        return [product.to_dict() for product in results]

    except SQLAlchemyError as e:
        print(f"Search error: {e}")
        return []

# API Routes
@app.route('/api/products/search', methods=['GET'])
def search_products():
    """Endpoint for product search with multiple filters."""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort_by', 'match_percentage')

    results = advanced_search(
        query=query, 
        category=category, 
        min_price=min_price, 
        max_price=max_price,
        sort_by=sort_by
    )

    return jsonify(results)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Retrieve all product categories."""
    categories = Category.query.all()
    return jsonify([category.name for category in categories])

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Get product recommendations based on category or random."""
    category_name = request.args.get('category', '')
    
    if category_name:
        category = Category.query.filter_by(name=category_name).first()
        if category:
            recommendations = (
                Product.query
                .filter_by(category_id=category.id)
                .order_by(Product.match_percentage.desc())
                .limit(10)
                .all()
            )
        else:
            recommendations = []
    else:
        # Random recommendations
        recommendations = Product.query.order_by(func.random()).limit(10).all()

    return jsonify([product.to_dict() for product in recommendations])

@app.route('/api/health', methods=['GET'])
def health_check():
    """System health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'total_products': Product.query.count(),
        'total_categories': Category.query.count()
    })

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Application Entry Point
def create_app():
    with app.app_context():
        db.create_all()
        
        # Populate database if empty
        if Product.query.count() == 0:
            populate_database()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
