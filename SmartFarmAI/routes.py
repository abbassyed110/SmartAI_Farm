import os
import json
import logging
from datetime import datetime
from flask import render_template, redirect, url_for, request, flash, jsonify, session, Blueprint, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from models import (
    User, FarmerCrop, MarketplaceListing, WeatherAlert, 
    DiseaseDiagnosis, CropRecommendation, KnowledgeArticle
)
from utils import get_weather_data, allowed_file, format_date
from ml_models.crop_recommendation import predict_crop
from ml_models.disease_identification import identify_disease
from ml_models.weather_prediction import predict_weather_alerts
from app import db  # Only import `db`, not `app`

logger = logging.getLogger(__name__)

bp = Blueprint('routes', __name__)

# Context processor to add variables to all templates
@bp.context_processor
def inject_now():
    return {'now': datetime.now()}

# Custom Jinja2 filters
# Flask 3 Blueprint no longer supports bp.template_filter(), so register via app in create_app
def from_json(value):
    """Convert a JSON string into a Python object"""
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return {}

# Home route
@bp.route('/')
def index():
    return render_template('index.html')

# User Authentication Routes
@bp.route('/login', methods=['GET', 'POST'])
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

@bp.route('/register', methods=['GET', 'POST'])
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

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Set language
@bp.route('/set_language/<lang>')
def set_language(lang):
    session['language'] = lang
    if current_user.is_authenticated:
        current_user.language_preference = lang
        db.session.commit()
    return redirect(request.referrer or url_for('index'))

# Dashboard
@bp.route('/dashboard')
@login_required
def dashboard():
    # Get user's crops
    user_crops_query = FarmerCrop.query.filter_by(user_id=current_user.id).all()
    
    # Convert SQLAlchemy objects to dictionaries for JSON serialization
    user_crops = []
    for crop in user_crops_query:
        user_crops.append({
            'id': crop.id,
            'crop_name': crop.crop_name,
            'planting_date': format_date(crop.planting_date) if crop.planting_date else None,
            'expected_harvest_date': format_date(crop.expected_harvest_date) if crop.expected_harvest_date else None,
            'area_planted': crop.area_planted,
            'status': crop.status,
            'notes': crop.notes,
            'created_at': format_date(crop.created_at) if crop.created_at else None
        })
    
    # Get weather data for user's location
    weather_data = None
    if current_user.farm_latitude and current_user.farm_longitude:
        weather_data = get_weather_data(current_user.farm_latitude, current_user.farm_longitude)
    
    # Get user's active marketplace listings
    listings_query = MarketplaceListing.query.filter_by(user_id=current_user.id, is_active=True).all()
    listings = []
    for listing in listings_query:
        listings.append({
            'id': listing.id,
            'crop_name': listing.crop_name,
            'quantity': listing.quantity,
            'unit': listing.unit,
            'price_per_unit': listing.price_per_unit,
            'description': listing.description,
            'location': listing.location,
            'created_at': format_date(listing.created_at) if listing.created_at else None
        })
    
    # Get user's unread weather alerts
    alerts_query = WeatherAlert.query.filter_by(user_id=current_user.id, is_read=False).all()
    alerts = []
    for alert in alerts_query:
        alerts.append({
            'id': alert.id,
            'alert_type': alert.alert_type,
            'alert_message': alert.alert_message,
            'severity': alert.severity,
            'start_date': format_date(alert.start_date) if alert.start_date else None,
            'end_date': format_date(alert.end_date) if alert.end_date else None,
            'created_at': format_date(alert.created_at) if alert.created_at else None
        })
    
    return render_template(
        'dashboard.html',
        crops=user_crops,
        weather=weather_data,
        listings=listings,
        alerts=alerts
    )

# User Profile
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.phone = request.form.get('phone')
        current_user.language_preference = request.form.get('language')
        current_user.farm_size = float(request.form.get('farm_size') or 0)
        current_user.farm_location = request.form.get('farm_location')
        
        # Try to get lat/long from form
        try:
            current_user.farm_latitude = float(request.form.get('farm_latitude') or 0)
            current_user.farm_longitude = float(request.form.get('farm_longitude') or 0)
        except ValueError:
            flash('Invalid latitude or longitude values', 'error')
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html')

# Crop Management Routes
@bp.route('/crop_recommendation', methods=['GET', 'POST'])
@login_required
def crop_recommendation():
    if request.method == 'POST':
        try:
            soil_type = request.form.get('soil_type')
            ph_value = float(request.form.get('ph_value'))
            rainfall = float(request.form.get('rainfall'))
            temperature = float(request.form.get('temperature'))
            humidity = float(request.form.get('humidity'))
            
            # Call ML model to get crop recommendations
            recommended_crops = predict_crop(soil_type, ph_value, rainfall, temperature, humidity)
            
            # Save the recommendation
            recommendation = CropRecommendation(
                user_id=current_user.id,
                soil_type=soil_type,
                ph_value=ph_value,
                rainfall=rainfall,
                temperature=temperature,
                humidity=humidity,
                recommended_crops=json.dumps(recommended_crops)
            )
            db.session.add(recommendation)
            db.session.commit()
            
            # Pass the recommendation data directly, not as JSON
            return render_template(
                'crop_recommendation.html',
                recommended_crops=recommended_crops,  # This is already a Python list of dicts
                soil_type=soil_type,
                ph_value=ph_value,
                rainfall=rainfall,
                temperature=temperature,
                humidity=humidity
            )
            
        except Exception as e:
            logger.error(f"Error in crop recommendation: {str(e)}")
            flash('An error occurred while processing your request', 'error')
    
    # Get user's previous recommendations
    previous_recommendations = CropRecommendation.query.filter_by(user_id=current_user.id).order_by(CropRecommendation.created_at.desc()).limit(5).all()
    
    # Pre-process recommendations to parse the JSON data
    for recommendation in previous_recommendations:
        try:
            # Parse the JSON string into a Python object
            if recommendation.recommended_crops:
                recommendation.parsed_crops = json.loads(recommendation.recommended_crops)
            else:
                recommendation.parsed_crops = []
        except Exception as e:
            logger.error(f"Error parsing recommendation data: {str(e)}")
            recommendation.parsed_crops = []
    
    return render_template('crop_recommendation.html', previous_recommendations=previous_recommendations)

@bp.route('/add_crop', methods=['POST'])
@login_required
def add_crop():
    crop_name = request.form.get('crop_name')
    planting_date_str = request.form.get('planting_date')
    expected_harvest_date_str = request.form.get('expected_harvest_date')
    area_planted = float(request.form.get('area_planted') or 0)
    notes = request.form.get('notes')
    
    try:
        planting_date = datetime.strptime(planting_date_str, '%Y-%m-%d').date() if planting_date_str else None
        expected_harvest_date = datetime.strptime(expected_harvest_date_str, '%Y-%m-%d').date() if expected_harvest_date_str else None

        new_crop = FarmerCrop(
            user_id=current_user.id,
            crop_name=crop_name,
            planting_date=planting_date,
            expected_harvest_date=expected_harvest_date,
            area_planted=area_planted,
            status="growing",
            notes=notes
        )
        
        db.session.add(new_crop)
        db.session.commit()
        flash('Crop added successfully', 'success')
    except Exception as e:
        logger.error(f"Error adding crop: {str(e)}")
        flash('Error adding crop', 'error')
    
    return redirect(url_for('dashboard'))


@bp.route('/add_to_farm_plan', methods=['POST'])
@login_required
def add_to_farm_plan():
    crop_name = None
    if request.is_json:
        payload = request.get_json(silent=True) or {}
        crop_name = payload.get('crop_name')
    if not crop_name:
        crop_name = request.form.get('crop_name')

    if not crop_name:
        return jsonify({'error': 'crop_name is required'}), 400

    try:
        new_crop = FarmerCrop(
            user_id=current_user.id,
            crop_name=crop_name,
            planting_date=None,
            expected_harvest_date=None,
            area_planted=0,
            status='planned',
            notes='Added from crop recommendation'
        )
        db.session.add(new_crop)
        db.session.commit()

        return jsonify({'message': 'Crop added to farm plan'}), 201
    except Exception as e:
        logger.error(f"Error adding crop to farm plan: {str(e)}")
        return jsonify({'error': 'Could not add crop to farm plan'}), 500

@bp.route('/update_crop/<int:crop_id>', methods=['POST'])
@login_required
def update_crop(crop_id):
    crop = FarmerCrop.query.get_or_404(crop_id)
    
    # Ensure the crop belongs to the current user
    if crop.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    
    crop.status = request.form.get('status')
    crop.notes = request.form.get('notes')
    
    db.session.commit()
    flash('Crop updated successfully', 'success')
    return redirect(url_for('dashboard'))

# Disease Detection
@bp.route('/disease_detection', methods=['GET', 'POST'])
@login_required
def disease_detection():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'plant_image' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['plant_image']
        crop_name = request.form.get('crop_name')
        
        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Call disease identification model
                disease, confidence, treatment = identify_disease(filepath, crop_name)
                
                # Save diagnosis in database
                diagnosis = DiseaseDiagnosis(
                    user_id=current_user.id,
                    crop_name=crop_name,
                    image_path=filepath,
                    diagnosis_result=disease,
                    confidence_score=confidence,
                    treatment_recommendation=treatment
                )
                db.session.add(diagnosis)
                db.session.commit()
                
                return render_template(
                    'disease_detection.html',
                    disease=disease,
                    confidence=confidence,
                    treatment=treatment,
                    image_path=filename,
                    crop_name=crop_name
                )
                
            except Exception as e:
                logger.error(f"Error in disease detection: {str(e)}")
                flash('Error processing image', 'error')
                return redirect(request.url)
    
    # Get user's previous diagnoses
    previous_diagnoses = DiseaseDiagnosis.query.filter_by(user_id=current_user.id).order_by(DiseaseDiagnosis.created_at.desc()).limit(5).all()
    
    return render_template('disease_detection.html', previous_diagnoses=previous_diagnoses)

# Weather Routes
@bp.route('/weather')
@login_required
def weather():
    weather_data = None
    alerts = []
    
    if current_user.farm_latitude and current_user.farm_longitude:
        # Get current weather data
        weather_data = get_weather_data(current_user.farm_latitude, current_user.farm_longitude)
        
        # Get weather alerts for the user
        alerts = WeatherAlert.query.filter_by(user_id=current_user.id).order_by(WeatherAlert.created_at.desc()).limit(10).all()
        
        # Mark alerts as read
        for alert in alerts:
            if not alert.is_read:
                alert.is_read = True
        
        db.session.commit()
    
    return render_template('weather.html', weather_data=weather_data, alerts=alerts)

@bp.route('/generate_weather_alerts')
@login_required
def generate_weather_alerts():
    if not current_user.farm_latitude or not current_user.farm_longitude:
        flash('Please set your farm location in your profile', 'error')
        return redirect(url_for('weather'))
    
    try:
        # Generate weather alerts using ML model
        alerts = predict_weather_alerts(current_user.farm_latitude, current_user.farm_longitude)
        
        # Save alerts to database
        for alert_data in alerts:
            alert = WeatherAlert(
                user_id=current_user.id,
                alert_type=alert_data['type'],
                alert_message=alert_data['message'],
                severity=alert_data['severity'],
                start_date=alert_data['start_date'],
                end_date=alert_data['end_date'],
                is_read=False
            )
            db.session.add(alert)
        
        db.session.commit()
        flash('Weather alerts generated successfully', 'success')
    except Exception as e:
        logger.error(f"Error generating weather alerts: {str(e)}")
        flash('Error generating weather alerts', 'error')
    
    return redirect(url_for('weather'))

# REST API Endpoints (model integrations)
@bp.route('/api/v1/crop_recommendation', methods=['POST'])
@login_required
def api_crop_recommendation():
    data = request.get_json() or {}
    required = ['soil_type', 'ph_value', 'rainfall', 'temperature', 'humidity']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({'error': 'Missing fields: ' + ', '.join(missing)}), 400

    try:
        soil_type = data['soil_type']
        ph_value = float(data['ph_value'])
        rainfall = float(data['rainfall'])
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])

        recommendations = predict_crop(soil_type, ph_value, rainfall, temperature, humidity)

        recommendation = CropRecommendation(
            user_id=current_user.id,
            soil_type=soil_type,
            ph_value=ph_value,
            rainfall=rainfall,
            temperature=temperature,
            humidity=humidity,
            recommended_crops=json.dumps(recommendations)
        )
        db.session.add(recommendation)
        db.session.commit()

        return jsonify({'recommended_crops': recommendations}), 200
    except Exception as e:
        logger.error(f"API crop recommendation error: {e}")
        return jsonify({'error': 'Failed to generate recommendation'}), 500


@bp.route('/api/v1/disease_detection', methods=['POST'])
@login_required
def api_disease_detection():
    data = request.get_json() or {}
    image_path = data.get('image_path')
    crop_name = data.get('crop_name')

    if not image_path or not crop_name:
        return jsonify({'error': 'image_path and crop_name are required'}), 400

    if not os.path.exists(image_path):
        return jsonify({'error': 'Image not found on server path'}), 404

    try:
        disease, confidence, treatment = identify_disease(image_path, crop_name)
        diagnosis = DiseaseDiagnosis(
            user_id=current_user.id,
            crop_name=crop_name,
            image_path=image_path,
            diagnosis_result=disease,
            confidence_score=confidence,
            treatment_recommendation=treatment
        )
        db.session.add(diagnosis)
        db.session.commit()

        return jsonify({
            'disease': disease,
            'confidence': round(confidence, 2),
            'treatment': treatment
        }), 200
    except Exception as e:
        logger.error(f"API disease detection error: {e}")
        return jsonify({'error': 'Failed to identify disease'}), 500


@bp.route('/api/v1/weather_alerts', methods=['GET'])
@login_required
def api_weather_alerts():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)

    if lat is None or lon is None:
        return jsonify({'error': 'lat and lon query parameters are required'}), 400

    try:
        alerts = predict_weather_alerts(lat, lon)
        return jsonify({'alerts': [
            {
                'type': a['type'],
                'message': a['message'],
                'severity': a['severity'],
                'start_date': a['start_date'].isoformat() if hasattr(a['start_date'], 'isoformat') else str(a['start_date']),
                'end_date': a['end_date'].isoformat() if hasattr(a['end_date'], 'isoformat') else str(a['end_date'])
            } for a in alerts
        ]}), 200
    except Exception as e:
        logger.error(f"API weather alerts error: {e}")
        return jsonify({'error': 'Failed to fetch weather alerts'}), 500


# Marketplace Routes
@bp.route('/marketplace')
def marketplace():
    listings = MarketplaceListing.query.filter_by(is_active=True).order_by(MarketplaceListing.created_at.desc()).all()
    return render_template('marketplace.html', listings=listings)

@bp.route('/add_listing', methods=['POST'])
@login_required
def add_listing():
    try:
        crop_name = request.form.get('crop_name')
        quantity = float(request.form.get('quantity'))
        unit = request.form.get('unit')
        price_per_unit = float(request.form.get('price_per_unit'))
        description = request.form.get('description')
        location = request.form.get('location', current_user.farm_location)
        
        listing = MarketplaceListing(
            user_id=current_user.id,
            crop_name=crop_name,
            quantity=quantity,
            unit=unit,
            price_per_unit=price_per_unit,
            description=description,
            location=location,
            is_active=True
        )
        
        db.session.add(listing)
        db.session.commit()
        flash('Listing added successfully', 'success')
    except Exception as e:
        logger.error(f"Error adding listing: {str(e)}")
        flash('Error adding listing', 'error')
    
    return redirect(url_for('marketplace'))

@bp.route('/update_listing/<int:listing_id>', methods=['POST'])
@login_required
def update_listing(listing_id):
    listing = MarketplaceListing.query.get_or_404(listing_id)
    
    # Ensure the listing belongs to the current user
    if listing.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('marketplace'))
    
    try:
        listing.quantity = float(request.form.get('quantity'))
        listing.price_per_unit = float(request.form.get('price_per_unit'))
        listing.description = request.form.get('description')
        listing.is_active = 'is_active' in request.form
        
        db.session.commit()
        flash('Listing updated successfully', 'success')
    except Exception as e:
        logger.error(f"Error updating listing: {str(e)}")
        flash('Error updating listing', 'error')
    
    return redirect(url_for('marketplace'))

# Knowledge Base
@bp.route('/knowledge_base')
def knowledge_base():
    category = request.args.get('category', 'all')
    
    if category != 'all':
        articles = KnowledgeArticle.query.filter_by(category=category).order_by(KnowledgeArticle.created_at.desc()).all()
    else:
        articles = KnowledgeArticle.query.order_by(KnowledgeArticle.created_at.desc()).all()
    
    categories = db.session.query(KnowledgeArticle.category).distinct().all()
    categories = [c[0] for c in categories]
    
    return render_template('knowledge_base.html', articles=articles, categories=categories, current_category=category)

@bp.route('/knowledge_article/<int:article_id>')
def knowledge_article(article_id):
    article = KnowledgeArticle.query.get_or_404(article_id)
    return render_template('knowledge_base.html', article=article)

# Error handlers
@bp.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', error='Page not found'), 404

@bp.errorhandler(500)
def internal_server_error(e):
    return render_template('base.html', error='Internal server error'), 500
