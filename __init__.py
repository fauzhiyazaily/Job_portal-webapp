from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Create extensions
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    # Create Flask app instance
    app = Flask(__name__)

    # Basic configuration
    app.config['SECRET_KEY'] = 'dev-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobportal.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Import and register blueprint
    from app.routes import bp
    app.register_blueprint(bp)

    return app


# Import models at the bottom to avoid circular imports
from app import models