"""
Routes for interacting with Category 1 game providers.
"""

from flask import Blueprint, request, jsonify
from app.services.game_service import Category1Service
from app.utils.error_handling import handle_errors

bp = Blueprint('category1', __name__)

@bp.route('/api/category1/login', methods=['POST'])
@handle_errors
def login():
    """Login to a Category 1 game provider."""
    data = request.get_json()
    service = Category1Service(data['username'], data['password'])
    result = service.login()
    return jsonify(result), 200

@bp.route('/api/category1/add_user', methods=['POST'])
@handle_errors
def add_user():
    """Add a new user to a Category 1 game provider."""
    data = request.get_json()
    service = Category1Service(data['username'], data['password'])
    result = service.add_user(data['new_username'], data['new_password'])
    return jsonify(result), 201