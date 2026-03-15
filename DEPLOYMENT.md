# SmartAI_Farm Deployment Guide

## Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/abbassyed110/SmartAI_Farm.git
cd SmartAI_Farm
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Flask Backend (Terminal 1)
```bash
python run.py
```
This starts the Flask API on `http://127.0.0.1:5000`

### 4. Run Streamlit App (Terminal 2)
```bash
streamlit run streamlit_app.py
```
This opens Streamlit UI on `http://localhost:8501`

---

## Streamlit Cloud Deployment

### Prerequisites
1. GitHub account with public repository ✅
2. Streamlit account (free at https://streamlit.io/cloud)

### Steps to Deploy

#### Step 1: Prepare Your Repository
```bash
cd SmartAI_Farm
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### Step 2: Deploy on Streamlit Cloud

1. Go to **https://streamlit.io/cloud**
2. Click **"New app"** button
3. In the deployment dialog:
   - **Repository**: `abbassyed110/SmartAI_Farm`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
4. Click **"Deploy"**

Streamlit will automatically:
- Install dependencies from `requirements.txt`
- Deploy the app at a unique URL (e.g., `https://smartai-farm.streamlit.app`)

#### Step 3: Configure Backend URL (After Deployment)

Since the Streamlit app makes API calls to the Flask backend:

1. **Option A: Local Backend**
   - Keep Flask running on your machine
   - App will work only when Flask is running
   - Not ideal for production

2. **Option B: Deploy Flask Backend** (Recommended)
   - Deploy Flask on Heroku, AWS, or other service
   - Get the production URL (e.g., `https://smartai-farm-api.herokuapp.com`)
   - Add to Streamlit Cloud secrets:
     - Go to app → Settings → Advanced settings → Secrets
     - Paste:
       ```toml
       BACKEND_URL = "https://your-deployed-flask-url"
       ```

---

## Backend Deployment Options

### Deploy Flask on Heroku

#### Step 1: Prepare Procfile
Create `Procfile` in root directory:
```
web: gunicorn app:app
```

#### Step 2: Install Heroku CLI
```bash
# Windows
choco install heroku-cli

# Or download from https://devcenter.heroku.com/articles/heroku-cli
```

#### Step 3: Deploy
```bash
heroku login
heroku create smartai-farm-api
git push heroku main
heroku open
```

### Deploy Flask on AWS

1. Use EC2 or Elastic Beanstalk
2. Use RDS for database
3. Use Route53 for domain

### Deploy Flask on DigitalOcean

1. Create Droplet (5$/month)
2. Install Python, Flask, Gunicorn, Nginx
3. Deploy using Git or Docker

---

## Local Development with Secrets

### Create Local Secrets File

1. Create `.streamlit/secrets.toml`:
```toml
BACKEND_URL = "http://127.0.0.1:5000"
```

2. This file is in `.gitignore` (won't be pushed to GitHub)

3. Run Streamlit:
```bash
streamlit run streamlit_app.py
```

---

## Directory Structure for Deployment

```
SmartAI_Farm/
├── streamlit_app.py           # Main Streamlit app
├── requirements.txt            # Python dependencies
├── .streamlit/
│   ├── config.toml            # Streamlit configuration
│   ├── secrets.toml.example   # Secrets template
│   └── secrets.toml           # Local secrets (NOT tracked)
├── Procfile                    # For Heroku deployment
├── DEPLOYMENT.md              # This file
└── ... (other files)
```

---

## Troubleshooting

### Issue: "Error installing requirements"
**Solution**: Update `requirements.txt` with compatible versions:
```
streamlit>=1.28.0
requests>=2.31.0
pandas>=2.0.0
Pillow>=10.0.0
protobuf~=3.20
```

### Issue: "Backend connection failed"
**Solution**: 
1. Ensure Flask is running (local development)
2. Check `BACKEND_URL` in secrets matches your Flask URL
3. Flask must be publicly accessible for Streamlit Cloud

### Issue: "ModuleNotFoundError"
**Solution**: 
1. Make sure all imports are in `requirements.txt`
2. Check Python version compatibility (3.8+)

### Issue: "Database connection failed"
**Solution**:
1. For local development, ensure `agritech.db` exists
2. For production, configure proper database service

---

## Environment Variables

### For Streamlit Cloud

In your app's Secrets:
```toml
# Required
BACKEND_URL = "https://your-flask-url.com"

# Optional
DATABASE_URL = "postgresql://user:pass@host/db"
WEATHER_API_KEY = "your-key"
DEBUG = true
```

### For Local Development

Create `.streamlit/secrets.toml`:
```toml
BACKEND_URL = "http://127.0.0.1:5000"
```

---

## Performance Tips

1. **Cache API calls**: Use `@st.cache_data` decorator
2. **Optimize images**: Compress before upload
3. **Use CDN**: Host static files on CloudFlare
4. **Database indexing**: Index frequently queried fields

---

## Support

- GitHub Issues: https://github.com/abbassyed110/SmartAI_Farm/issues
- Documentation: See `README.md`
- Contact: abbassayed7799@gmail.com

---

## Updates & Maintenance

### Pull Latest Changes
```bash
git pull origin main
```

### Update Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Push New Changes
```bash
git add .
git commit -m "Your message"
git push origin main
```

Streamlit Cloud will auto-redeploy on git push!

---

**Last Updated**: March 15, 2026
