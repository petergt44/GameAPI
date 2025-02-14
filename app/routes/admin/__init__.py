"""
Initialization file for admin routes.
"""

from flask import Blueprint, render_template
from .auth import bp as auth_bp
from .accounts import bp as accounts_bp
from .tokens import bp as tokens_bp
from .logs import bp as logs_bp

# Create a Blueprint for the admin dashboard
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_dashboard():
    """Render the admin dashboard."""
    return render_template('admin/dashboard.html')  # You'll need to create this template

# Register all admin routes
admin_bp.register_blueprint(auth_bp, url_prefix='/admin/api')
admin_bp.register_blueprint(accounts_bp, url_prefix='/admin/api')
admin_bp.register_blueprint(tokens_bp, url_prefix='/admin/api')
admin_bp.register_blueprint(logs_bp, url_prefix='/admin/api')