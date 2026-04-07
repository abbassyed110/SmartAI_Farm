# SmartFarmAI - AI-Powered Agricultural Intelligence Platform

A comprehensive agricultural technology platform powered by machine learning, providing intelligent crop recommendations, disease identification, weather predictions, and a farmers' marketplace.

## 📁 Project Structure

```
SmartFarmAI/
├── frontend/                    # React/JavaScript frontend (Vercel)
│   ├── templates/              # HTML templates
│   ├── static/                 # CSS, JS, images
│   │   ├── css/
│   │   ├── js/
│   ├── index5.html             # Main entry point
│   ├── package.json            # Frontend dependencies
│   ├── vercel.json             # Vercel configuration
│   └── .gitignore
│
├── backend/                     # Flask API (Render)
│   ├── app.py                  # Flask application factory
│   ├── run.py                  # Application entry point
│   ├── routes.py               # API endpoints
│   ├── models.py               # Database models
│   ├── utils.py                # Utility functions
│   ├── config.py               # Configuration settings
│   ├── ml_models/              # Machine learning models
│   │   ├── crop_recommendation.py
│   │   ├── disease_identification.py
│   │   └── weather_prediction.py
│   ├── uploads/                # Uploaded files storage
│   ├── instance/               # Instance configuration
│   ├── requirements.txt        # Python dependencies
│   ├── render.yaml             # Render deployment config
│   ├── .env.example            # Environment variables template
│   └── .gitignore
│
├── DEPLOYMENT.md               # Deployment guide
└── README.md                   # This file
```

## 🚀 Features

- **Crop Recommendation**: AI-powered suggestions based on soil conditions and weather
- **Disease Detection**: Identify crop diseases using image recognition
- **Weather Prediction**: Real-time weather forecasts integrated with farming data
- **Knowledge Base**: Comprehensive agricultural information and best practices
- **Farmer's Marketplace**: Connect buyers and sellers in the agricultural community
- **Offline Support**: Works offline with progressive web app capabilities
- **Multi-language Support**: Support for multiple languages for global accessibility

## 🛠 Tech Stack

### Frontend
- HTML5
- CSS3 (with animations)
- Vanilla JavaScript
- Progressive Web App (PWA)

### Backend
- Python 3.14+
- Flask (Web framework)
- Flask-SQLAlchemy (ORM)
- Flask-Login (Authentication)
- Scikit-learn (ML models)
- NumPy & Pandas (Data processing)

### Database
- SQLite (development)
- PostgreSQL (production)

### Deployment
- **Frontend**: Vercel
- **Backend**: Render

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+ (optional, for frontend development)
- Git
- pip and virtualenv

## 🔧 Local Development

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run the application
python run.py
```

The backend API will be available at `http://localhost:5000`

### Frontend Setup

```bash
cd frontend

# Option 1: Using Python built-in server
python -m http.server 8000

# Option 2: Using Node.js http-server (if installed)
npm install -g http-server
http-server
```

The frontend will be available at `http://localhost:8000`

## 🌐 Environment Variables

Create a `.env` file in the backend folder:

```env
SESSION_SECRET=your-secret-key-here
DATABASE_URL=sqlite:///agritech.db
FLASK_ENV=development
FLASK_DEBUG=True
```

For production on Render:
- `SESSION_SECRET`: Generate a secure random string
- `DATABASE_URL`: PostgreSQL connection string
- `FLASK_ENV`: production

## 📦 Deployment

### Deploy to Vercel (Frontend)

1. Go to [vercel.com](https://vercel.com)
2. Create a new project and connect your GitHub repo
3. Set root directory to `frontend`
4. Deploy!

### Deploy to Render (Backend)

1. Go to [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repo
4. Set root directory to `backend`
5. Configure the following:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT run:app`
   - **Environment Variables**: See `.env.example`

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

## 📱 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout
- `GET /profile` - Get user profile

### Crop Management
- `POST /crop-recommendation` - Get crop recommendations
- `GET /crops` - List all crops

### Disease Detection
- `POST /disease-detection` - Upload image for disease detection
- `GET /diseases` - List known diseases

### Weather
- `GET /weather` - Get weather data
- `GET /weather/forecast` - Get weather forecast

### Marketplace
- `GET /marketplace` - List marketplace items
- `POST /marketplace` - Create listing
- `PUT /marketplace/<id>` - Update listing
- `DELETE /marketplace/<id>` - Delete listing

### Knowledge Base
- `GET /knowledge-base` - Get articles
- `GET /knowledge-base/<id>` - Get article details

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, email support@smartfarmAI.com or open an issue in the GitHub repository.

## 📞 Contact

- **Project Lead**: Abbas Syed
- **GitHub**: [abbassyed110](https://github.com/abbassyed110)
- **Repository**: [SmartAI_Farm](https://github.com/abbassyed110/SmartAI_Farm)

---

Made with ❤️ for farmers worldwide
