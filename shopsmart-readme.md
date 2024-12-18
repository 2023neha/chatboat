# 🛍️ ShopSmart AI - Intelligent E-Commerce Assistant

## Project Overview

ShopSmart AI is an intelligent, conversational e-commerce shopping assistant that provides personalized product recommendations through an intuitive web interface. Leveraging advanced search algorithms and machine learning techniques, the application helps users discover products tailored to their preferences.

### 🌟 Key Features
- 💬 Conversational AI Interface
- 🔍 Advanced Product Search
- 🤖 Intelligent Recommendation Engine
- 📊 Dynamic Product Filtering
- 🌈 Mood-based Product Suggestions

## Technology Stack

### Frontend
- HTML5
- CSS3 (Responsive Design)
- Vanilla JavaScript

### Backend
- Python 3.8+
- Flask Web Framework
- SQLAlchemy ORM
- Flask-Migrate
- Faker (for data generation)

### Database
- SQLite (Development)
- PostgreSQL (Production-Ready)

## Project Structure
```
shopsmart-ai/
│
├── frontend/
│   └── shopsmart-chatbot.html      # Main frontend application
│
├── backend/
│   ├── shopsmart_backend.py         # Flask backend server
│   └── requirements.txt             # Python dependencies
│
├── database/
│   └── shopsmart.db                 # SQLite database
│
├── tests/
│   ├── test_backend.py              # Backend unit tests
│   └── test_frontend.js             # Frontend integration tests
│
├── docs/
│   └── technical_documentation.md   # Detailed project documentation
│
├── .env.example                     # Environment configuration template
├── .gitignore
├── LICENSE
└── README.md
```

## Prerequisites

### Frontend
- Modern web browser (Chrome, Firefox, Safari, Edge)
- No additional dependencies

### Backend
- Python 3.8+
- pip (Python Package Manager)
- Virtual Environment recommended

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/shopsmart-ai.git
cd shopsmart-ai
```

### 2. Backend Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 3. Database Initialization
```bash
# Run migrations
flask db upgrade

# Populate initial data (optional)
python backend/shopsmart_backend.py --populate
```

### 4. Run Backend Server
```bash
python backend/shopsmart_backend.py
```

### 5. Run Frontend
- Open `frontend/shopsmart-chatbot.html` in your web browser

## Configuration

### Environment Variables
- `SECRET_KEY`: Application secret key
- `DATABASE_URL`: Database connection string
- `JWT_SECRET_KEY`: JWT authentication secret
- `DEBUG`: Enable/disable debug mode

## API Endpoints

### Product Search
- `/api/products/search`: Advanced product search
  - Parameters: `q` (query), `category`, `min_price`, `max_price`, `sort_by`

### Recommendations
- `/api/recommendations`: Get product recommendations
- `/api/categories`: Retrieve product categories

### System Health
- `/api/health`: Check application health

## Testing

### Backend Tests
```bash
python -m pytest tests/test_backend.py
```

## Deployment

### Local Deployment
- Ensure prerequisites are met
- Run backend server
- Open frontend HTML

### Production Deployment
- Use gunicorn/uwsgi for Flask backend
- Configure PostgreSQL database
- Set up CORS and security headers

## Contribution Guidelines

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

### Areas for Contribution
- Recommendation algorithm improvements
- Frontend UI/UX enhancements
- Additional search filters
- Machine learning integration

## Known Limitations
- Mock data generation
- Simplified recommendation engine
- No persistent user sessions

## Future Roadmap
- [ ] User authentication
- [ ] Advanced ML recommendation system
- [ ] Real-time product updates
- [ ] Personalized user profiles

## Performance Optimization
- Efficient database querying
- Caching mechanisms
- Asynchronous recommendation loading

## Security Considerations
- Parameterized database queries
- Password hashing
- CORS configuration
- Environment-based configuration

## License
MIT License

## Authors
- Your Name <your.email@example.com>

## Support
For issues or questions, please open a GitHub issue.

---

**Happy Smart Shopping! 🛒✨**
