"""
Routes for managing API tokens.
"""

from flask import Blueprint, jsonify, request
from app.models import Token
from app import db

bp = Blueprint('tokens', __name__)

@bp.route('/admin/api/tokens', methods=['GET'])
def get_tokens():
    """Fetch all tokens."""
    tokens = Token.query.all()
    return jsonify([token.to_dict() for token in tokens])

@bp.route('/admin/api/tokens', methods=['POST'])
def create_token():
    """Create a new token."""
    data = request.get_json()
    token = Token(
        account_id=data['account_id'],
        token=data['token'],
        valid_until=data['valid_until']
    )
    db.session.add(token)
    db.session.commit()
    return jsonify(token.to_dict()), 201