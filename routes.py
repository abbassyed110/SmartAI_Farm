import os
import json
import logging
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

# Create Blueprint for modular usage
bp = Blueprint('main', __name__)

# Define the JSON converter function outside of decorators
def from_json(value):
    """Convert a JSON string into a Python object"""
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return {}

# Context processor to add variables to all templates
def inject_now():
    return {'now': datetime.now()}

# Setup function to register all routes
def setup_routes(app):
    # Import these here to avoid circular imports
    from app import db
    from models import (
        User, FarmerCrop, MarketplaceListing, WeatherAlert, 
        DiseaseDiagnosis, CropRecommendation, KnowledgeArticle
    )
    from utils import get_weather_data, allowed_file, format_date
    from ml_models.crop_recommendation import predict_crop
    from ml_models.disease_identification import identify_disease
    from ml_models.weather_prediction import predict_weather_alerts
    
    # Register the blueprint
    app.register_blueprint(bp)
    
    # Register the context processor
    app.context_processor(inject_now)
    
    # Register custom filter
    app.template_filter('fromjson')(from_json)
    
    # Home route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # User Authentication Routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('dashboard'))
            else:
                flash('Invalid username or password', 'error')
        
        return render_template('login.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            full_name = request.form.get('full_name')
            phone = request.form.get('phone')
            language = request.form.get('language', 'en')
            
            # Validation
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return render_template('register.html')
            
            existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                flash('Username or email already exists', 'error')
                return render_template('register.html')
            
            # Create new user
            new_user = User(
                username=username,
                email=email,
                full_name=full_name,
                phone=phone,
                language_preference=language
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        
        return render_template('register.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    # Set language
    @app.route('/set_language/<lang>')
    def set_language(lang):
        session['language'] = lang
        if current_user.is_authenticated:
            current_user.language_preference = lang
            db.session.commit()
        return redirect(request.referrer or url_for('index'))
    
    # Dashboard
    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')
    
    # User Profile
    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        return render_template('profile.html')
    
    # Crop Management Routes
    @app.route('/crop_recommendation', methods=['GET', 'POST'])
    @login_required
    def crop_recommendation():
        return render_template('crop_recommendation.html')
    
    # Disease Detection
    @app.route('/disease_detection', methods=['GET', 'POST'])
    @login_required
    def disease_detection():
        return render_template('disease_detection.html')
    
    # Weather Routes
    @app.route('/weather')
    @login_required
    def weather():
        return render_template('weather.html')
    
    # Marketplace Routes
    @app.route('/marketplace')
    def marketplace():
        return render_template('marketplace.html')
    
    # Knowledge Base
    @app.route('/knowledge_base')
    def knowledge_base():
        return render_template('knowledge_base.html')
    
    # Offline Access
    @app.route('/offline')
    def offline():
        return render_template('offline.html')