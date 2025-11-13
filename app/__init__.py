"""
Initialization file for the Flask application.
Sets up the Flask app, database, migrations, and blueprints.
"""

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from flask_cors import CORS
from config import Config
from flask_restx import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_caching import Cache
from flask_login import login_required
import json

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

# Custom Jinja2 filter for pretty JSON
def tojson_pretty(value):
    return json.dumps(value, indent=2, ensure_ascii=False)
app.jinja_env.filters['tojson_pretty'] = tojson_pretty

@app.before_request
def bypass_login_for_swagger():
    """Disable authentication for Swagger UI."""
    if request.path.startswith("/swagger"):
        request._login_disabled = True  # Disable authentication for this request

# Swagger UI configuration
SWAGGER_URL = '/swagger'  # URL for accessing Swagger UI
API_URL = '/swagger.json'  # URL for the API specification

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
    description='A Centralized API for third-party game providers.',
    doc='/swagger/'
)

# Import and register blueprints
from app.routes.admin.auth import bp as auth_bp
from app.routes.admin.dashboard import bp as dashboard_bp

app.register_blueprint(auth_bp, url_prefix='/admin')
app.register_blueprint(dashboard_bp, url_prefix='/admin')

# Import models
from app import models

# Define admin dashboard route
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

def create_app():
    """
    Factory function to create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    # Initialize extensions with the app
    db.init_app(app)
    cache.init_app(app)  # Ensure cache is initialized here
    migrate.init_app(app, db)
    login_manager.init_app(app)
    CORS(app)

    # Import models to ensure they are registered
    from app import models

    # Import and add namespaces
    from app.routes.api.category1 import category1_ns
    from app.routes.api.category2 import category2_ns
    from app.routes.api.category3 import category3_ns
    from app.routes.api.category4 import category4_ns
    from app.routes.api.category5 import category5_ns
    from app.routes.api.vblink import vblink_ns
    
    api.add_namespace(category1_ns)
    api.add_namespace(category2_ns)
    api.add_namespace(category3_ns)
    api.add_namespace(category4_ns)
    api.add_namespace(category5_ns)
    api.add_namespace(vblink_ns)

    # Register Swagger UI blueprint
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app

# Create the app
app = create_app()

# Verify cache initialization (optional debugging)
with app.app_context():
    cache.set("test_key", "test_value")
    print("Cache test:", cache.get("test_key"))  # Should print "test_value"