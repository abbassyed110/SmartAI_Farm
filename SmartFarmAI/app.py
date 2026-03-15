import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from models import User
    try:
        return User.query.get(int(user_id))
    except Exception:
        return None

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")  # Add fallback for local dev

    # Configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///agritech.db")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["UPLOAD_FOLDER"] = "uploads"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'

    # Create uploads folder if it doesn't exist
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    # Register blueprints and routes
    with app.app_context():
        from models import User  # Import models after db is initialized
        db.create_all()

        from routes import bp as routes_bp, from_json  # Import routes and the custom filter
        app.register_blueprint(routes_bp)

        # Add un-prefixed endpoint aliases for template compatibility
        # This allows using url_for('index') as well as url_for('routes.index')
        for rule in list(app.url_map.iter_rules()):
            if rule.endpoint.startswith('routes.'):
                short_endpoint = rule.endpoint.split('.', 1)[1]
                if short_endpoint not in app.view_functions:
                    app.add_url_rule(
                        rule.rule,
                        endpoint=short_endpoint,
                        view_func=app.view_functions[rule.endpoint],
                        methods=rule.methods,
                        defaults=rule.defaults,
                        strict_slashes=rule.strict_slashes,
                    )

        # Register the custom Jinja2 filter
        app.jinja_env.filters['fromjson'] = from_json

    return app
