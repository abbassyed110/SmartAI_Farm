import os
import json
import logging
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session, current_app

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
    # Register the blueprint
    app.register_blueprint(bp)
    
    # Register the context processor
    app.context_processor(inject_now)
    
    # Register custom filter
    app.template_filter('fromjson')(from_json)
    
    # Routes will be registered as part of the app registration
    # This ensures compatibility with both approaches
    
    # Home route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Add the rest of your routes here
    # (Removed for brevity, but would be included in actual implementation)