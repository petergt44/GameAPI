"""
Routes for managing API logs.
"""

from flask import Blueprint, jsonify, request
from app.models import APILog
from app import db

bp = Blueprint('logs', __name__)

@bp.route('/admin/api/logs', methods=['GET'])
def get_logs():
    """Fetch all API logs."""
    logs = APILog.query.all()
    return jsonify([log.to_dict() for log in logs])