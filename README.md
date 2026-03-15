# SmartFarmAI - AI-Powered Farming Solutions

A full-stack AI agricultural platform providing crop recommendations, disease detection, weather alerts, and marketplace features for farmers.

## Features

- 🌱 **Crop Recommendation** - ML-based crop suggestions based on soil, climate, and weather
- 🦠 **Disease Detection** - AI-powered plant disease identification with treatment recommendations
- ⛅ **Weather Alerts** - Real-time weather monitoring and agricultural alerts
- 🛒 **Marketplace** - Connect with buyers and sellers for agricultural products
- 📚 **Knowledge Base** - Educational articles on farming best practices
- 🌍 **Multi-language Support** - English, Hindi, Telugu, Tamil, Marathi, Bengali

## Tech Stack

### Backend
- **Framework**: Flask 2.x
- **Database**: SQLAlchemy ORM with SQLite
- **Authentication**: Flask-Login
- **API**: RESTful JSON endpoints

### Frontend
- **UI Framework**: Bootstrap 5
- **Templates**: Jinja2
- **Styling**: Custom CSS with green agricultural theme
- **JavaScript**: Vanilla JS with offline support

### Alternative UI
- **Streamlit App**: `streamlit_app.py` (lightweight alternative interface)

## Local Development

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. **Clone repository**
```bash
git clone https://github.com/abbassyed110/SmartFarmAI.git
cd SmartFarmAI
```

2. **Install dependencies**
```bash
pip install -r requirements_streamlit.txt
```

3. **Run Flask backend** (on port 5000)
```bash
python run.py
```

4. **Access the app**
- Flask UI: http://127.0.0.1:5000
- Streamlit UI: http://localhost:8501 (run `streamlit run streamlit_app.py` in separate terminal)

## Deployment

### Deploy Flask Backend (Heroku)

1. Create Heroku app
2. Add `Procfile`:
```
web: gunicorn app:app
```

3. Deploy:
```bash
git push heroku main
```

### Deploy Streamlit App (Streamlit Cloud)

1. Go to https://streamlit.io/cloud
2. Click "Deploy an app"
3. Connect your GitHub account
4. Select repository: `abbassyed110/SmartFarmAI`
5. Select branch: `main`
6. Select file: `streamlit_app.py`
7. Deploy

**Note**: Update `BACKEND_URL` in `streamlit_app.py` to point to your deployed Flask backend

## Project Structure

```
SmartFarmAI/
├── app.py                 # Flask app factory
├── routes.py              # Route handlers (800+ lines)
├── models.py              # SQLAlchemy ORM models
├── run.py                 # Development server launcher
├── streamlit_app.py       # Streamlit alternative UI
├── ml_models/             # ML model modules
│   ├── crop_recommendation.py
│   ├── disease_identification.py
│   └── weather_prediction.py
├── static/                # Frontend assets
│   ├── css/
│   ├── js/
│   └── img/
├── templates/             # Jinja2 HTML templates
├── instance/              # Instance folder (DB, config)
└── uploads/               # User uploads

```

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - User login
- `GET /logout` - User logout

### Dashboard
- `GET /dashboard` - User dashboard with crops, weather, listings

### Crop Recommendation
- `GET /crop_recommendation` - Form page
- `POST /crop_recommendation` - Submit recommendation request
- `POST /add_to_farm_plan` - Save recommended crop to farm plan
- `POST /api/v1/crop_recommendation` - JSON API

### Disease Detection
- `GET /disease_detection` - Disease detection page
- `POST /disease_detection` - Upload image for diagnosis
- `POST /api/v1/disease_detection` - JSON API

### Weather
- `GET /weather` - Weather page
- `POST /generate_weather_alerts` - Generate weather alerts
- `GET /api/v1/weather_alerts` - JSON API

### Marketplace
- `GET /marketplace` - View listings
- `POST /add_listing` - Create new listing

### Profile
- `GET /profile` - View/edit profile
- `POST /profile` - Update profile

## Configuration

### Environment Variables
```
SESSION_SECRET=your-secret-key
DATABASE_URL=sqlite:///agritech.db
UPLOAD_FOLDER=uploads
```

### Supported Languages
- English (en)
- हिन्दी (hi)
- తెలుగు (te)
- தமிழ் (ta)
- मराठी (mr)
- বাংলা (bn)

## Database Models

- **User** - Farmer profiles with authentication
- **FarmerCrop** - Crops planted by users
- **MarketplaceListing** - Agricultural product listings
- **WeatherAlert** - Weather notifications
- **DiseaseDiagnosis** - Disease detection history
- **CropRecommendation** - Recommendation history
- **KnowledgeArticle** - Educational content

## Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is open source and available under the MIT License.

## Author

Abbas Ayed - [GitHub](https://github.com/abbassyed110)

## Support

For issues and questions:
- GitHub Issues: https://github.com/abbassyed110/SmartFarmAI/issues
- Email: abbassayed7799@gmail.com

---

**Note**: This is currently a development version. For production deployment, ensure:
- Database is backed up
- SSL certificates are installed
- Environment variables are properly configured
- Rate limiting is implemented
- Input validation is enhanced
