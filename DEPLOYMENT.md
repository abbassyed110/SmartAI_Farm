# Project Structure

This SmartFarmAI project is now split into frontend and backend for easy deployment:

## Directory Structure

```
SmartFarmAI/
├── frontend/           # Frontend files - deploy to Vercel
│   ├── templates/      # HTML templates
│   ├── static/         # CSS, JS, and other static assets
│   ├── index5.html     # Main HTML file
│   ├── package.json    # Frontend dependencies (optional for Vercel)
│   └── vercel.json     # Vercel configuration
│
├── backend/            # Backend API - deploy to Render
│   ├── app.py          # Flask app setup
│   ├── run.py          # Application entry point
│   ├── routes.py       # API routes
│   ├── models.py       # Database models
│   ├── utils.py        # Utility functions
│   ├── ml_models/      # ML model files
│   ├── uploads/        # Uploaded files storage
│   ├── instance/       # Instance folder
│   ├── requirements.txt # Python dependencies
│   ├── render.yaml     # Render deployment configuration
│   └── .env.example    # Environment variables template
│
└── README.md
```

## Deployment Instructions

### Frontend (Vercel)

1. Sign up at [vercel.com](https://vercel.com)
2. Create a new project and connect your GitHub repository
3. Set the root directory to `frontend`
4. Deploy - Vercel will automatically host your static files

### Backend (Render)

1. Sign up at [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set the root directory to `backend`
5. Set the build command: `pip install -r requirements.txt`
6. Set the start command: `gunicorn -w 4 -b 0.0.0.0:$PORT run:app`
7. Add environment variables:
   - `SESSION_SECRET`: Generate a random secret
   - `DATABASE_URL`: PostgreSQL connection string (for production)
   - `FLASK_ENV`: production

## Running Locally

1. **Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   python run.py
   ```

2. **Frontend:**
   Open `frontend/index5.html` in your browser or use a local server:
   ```bash
   cd frontend
   python -m http.server 8000
   ```

## Environment Variables

Copy `.env.example` to `.env` and update with your configuration:
```bash
SESSION_SECRET=your-secret-key
DATABASE_URL=sqlite:///agritech.db
FLASK_ENV=development
```

## Notes

- The backend Flask app has been configured to serve templates from the frontend folder
- Update the backend API URL in your frontend JavaScript files to point to your Render deployment
- For production, use a PostgreSQL database instead of SQLite
