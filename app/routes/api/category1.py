"""
Routes for interacting with Category 1 game providers.
"""

from flask import Blueprint, request, jsonify
from app.services.game_service import Category1Service
from app.utils.error_handling import handle_errors

from flask_restx import Namespace, Resource, fields


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


# Create a namespace for Category 1
category1_ns = Namespace('category1', description='Category 1 game provider operations')

# Defines model for the API response
user_model = category1_ns.model('UserResponse', {
    'username': fields.String(description='Username of the new user'),
    'password': fields.String(description='Password of the new user')
})

login_model = category1_ns.model('LoginResponse', {
    'message': fields.String(description='Login status message'),
    'token': fields.String(description='Authentication token')
})


@category1_ns.route('/login')
class Category1Login(Resource):
    @category1_ns.doc('login')
    @category1_ns.response(200, 'Login successful', login_model)
    def post(self):
        """Login to a Category 1 game provider."""
        service = Category1Service(base_url="https://example.com", username="user", password="pass")
        return service.login()


@category1_ns.route('/add_user')
class AddUser(Resource):
    @category1_ns.doc('add_user')
    @category1_ns.expect(user_model)
    @category1_ns.response(201, 'User added successfully')
    def post(self):
        """Add a new user to the Category 1 game provider."""
        return {
            'message': 'User added successfully'
        }, 201