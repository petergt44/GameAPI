"""
Initialization file for the Flask application.
Sets up the Flask app, database, migrations, and blueprints.
"""

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from flask_cors import CORS
from config import Config
from flask_restx import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_caching import Cache

from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
cache = Cache()


@login_manager.user_loader
def load_user(user_id):
    return None  # Return None to indicate no user is logged in


class AnonymousUser(UserMixin):
    """Allows unauthenticated users to access routes without triggering login."""
    def is_authenticated(self):
        return False

login_manager.anonymous_user = AnonymousUser

@app.before_request
def bypass_login_for_swagger():
    """Disable authentication for Swagger UI."""
    if request.path.startswith("/swagger"):
        request._login_disabled = True  # Disable authentication for this request


# Swagger UI configuration
SWAGGER_URL = '/swagger'  # URL for accessing Swagger UI
API_URL = '/swagger.json'  # URL for the API specification

# Create Swagger UI blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Game Provider API'
    }
)

# Initialize Flask-RESTX API
api = Api(
    app,
    version='1.0',
    title='Game Provider API',
    description='A centralized API for third-party game providers.',
    doc='/swagger/'  # Enable Swagger UI at /swagger/
)

def create_app():
    """
    Factory function to create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """

    # Initialize extensions with the app
    db.init_app(app)
    cache.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    CORS(app)


    # Import and add namespaces
    from app.routes.api.category1 import category1_ns
    from app.routes.api.category2 import category2_ns
    from app.routes.api.category3 import category3_ns
    from app.routes.api.category4 import category4_ns
    from app.routes.api.vblink import vblink_ns
    
    api.add_namespace(category1_ns)
    api.add_namespace(category2_ns)
    api.add_namespace(category3_ns)
    api.add_namespace(category4_ns)
    api.add_namespace(vblink_ns)

    # Register Swagger UI blueprint
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app