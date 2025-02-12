"""
Routes for authentication (login, logout).
"""

from flask import Blueprint, request, jsonify
from app.models import Account
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/admin/api/login', methods=['POST'])
def login():
    """Authenticate a user."""
    data = request.get_json()
    account = Account.query.filter_by(username=data['username']).first()
    if account and account.password == data['password']:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401