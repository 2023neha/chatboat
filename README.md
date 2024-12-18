# chatboat
Project Overview
ShopSmart AI is a comprehensive e-commerce solution featuring an intelligent chatbot frontend and a robust Flask backend. The project combines an interactive user interface with advanced product recommendation and search capabilities.
Key Features

Interactive AI-powered shopping assistant
Dynamic product recommendations
Advanced search functionality
Responsive web design
Simulated product database with Faker

System Architecture
Frontend (ecommerce-chatbot-fixed.html)

Responsive, mobile-friendly chatbot interface
Dynamic product suggestions
Keyword-based product category detection
Animated UI with smooth interactions

Backend (shopsmart_backend.py)

Flask-based RESTful API
SQLAlchemy ORM for database management
Advanced product search with multiple filters
Random product recommendation system
Comprehensive error handling

Prerequisites
Software Requirements

Python 3.8+
pip (Python package manager)
Flask
SQLAlchemy
Flask-CORS
Faker

Installation & Setup
1. Clone the Repository
bashCopygit clone https://github.com/yourusername/shopsmart-ai.git
cd shopsmart-ai
2. Create Virtual Environment
bashCopypython3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install Dependencies
bashCopypip install flask flask-sqlalchemy flask-cors flask-migrate werkzeug faker
4. Initialize Database
bashCopyexport FLASK_APP=shopsmart_backend.py
flask db upgrade
5. Run the Application
bashCopypython shopsmart_backend.py
6. Access the Chatbot

Open ecommerce-chatbot-fixed.html in a web browser
Ensure backend server is running

API Endpoints
Product Search

Endpoint: /api/products/search
Methods: GET
Parameters:

q: Search query
category: Product category
min_price: Minimum price
max_price: Maximum price
sort_by: Sorting method



Product Recommendations

Endpoint: /api/recommendations
Methods: GET
Parameters:

category: Optional category filter



Categories

Endpoint: /api/categories
Methods: GET

Project Components
Database Models

Category: Product categories
Product: Detailed product information
SearchHistory: User search tracking
User: User account management

Key Technologies

Python
Flask
SQLAlchemy
HTML5
CSS3
JavaScript

Customization
Extending Product Database

Modify generate_product_features() function
Update populate_database() to add more categories/products

UI Customization

Edit CSS in ecommerce-chatbot-fixed.html
Adjust color schemes and layout

Deployment Considerations

Use production-grade WSGI server (Gunicorn, uWSGI)
Configure environment variables
Use PostgreSQL for production database
Implement proper authentication
