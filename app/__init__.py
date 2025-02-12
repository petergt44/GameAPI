"""
Initialization file for the Flask application.
Sets up the Flask app, database, migrations, and blueprints.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    """
    Factory function to create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    CORS(app)

    # Register blueprints
    from app.routes.admin import auth, accounts, tokens, logs
    from app.routes.api import category1 #vblink

    app.register_blueprint(auth.bp)
    app.register_blueprint(accounts.bp)
    app.register_blueprint(tokens.bp)
    app.register_blueprint(logs.bp)
    # app.register_blueprint(vblink.bp)
    app.register_blueprint(category1.bp)

    return app