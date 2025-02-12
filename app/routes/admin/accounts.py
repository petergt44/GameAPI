"""
Routes for managing admin accounts.
"""

from flask import Blueprint, jsonify, request
from app.models import Account
from app import db

bp = Blueprint('accounts', __name__)

@bp.route('/admin/api/accounts', methods=['GET'])
def get_accounts():
    """Fetch all accounts."""
    accounts = Account.query.all()
    return jsonify([account.to_dict() for account in accounts])

@bp.route('/admin/api/accounts', methods=['POST'])
def create_account():
    """Create a new account."""
    data = request.get_json()
    account = Account(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(account)
    db.session.commit()
    return jsonify(account.to_dict()), 201