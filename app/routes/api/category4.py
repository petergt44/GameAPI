"""
API routes for Category 4 game providers.
"""

from flask_restx import Namespace, Resource, fields
from app.services.category4_service import Category4Service
from app.utils.error_handling import handle_errors


category4_ns = Namespace('category4', description='Category 4 game provider operations')

# Request models
login_request = category4_ns.model('LoginRequest', {
    'username': fields.String(required=True, description='Game provider username'),
    'password': fields.String(required=True, description='Game provider password')
})

user_request = category4_ns.model('UserRequest', {
    'new_username': fields.String(required=True, description='New username'),
    'new_password': fields.String(required=True, description='New password')
})

# Response models
login_response = category4_ns.model('LoginResponse', {
    'message': fields.String(description='Login status message'),
    'token': fields.String(description='Authentication token')
})

user_response = category4_ns.model('UserResponse', {
    'message': fields.String(description='Operation result'),
    'user_id': fields.String(description='Created user ID')
})

@category4_ns.route('/login')
class Category4Login(Resource):
    @category4_ns.expect(login_request)
    @category4_ns.response(200, 'Success', login_response)
    @category4_ns.response(401, 'Invalid credentials')
    @handle_errors
    def post(self):
        """Authenticate with Category 4 provider"""
        data = category4_ns.payload
        service = Category4Service(data['username'], data['password'])
        result = service.login()
        return result, 200

@category4_ns.route('/add_user')
class Category4AddUser(Resource):
    @category4_ns.expect(login_request, user_request)
    @category4_ns.response(201, 'User created', user_response)
    @category4_ns.response(400, 'Bad request')
    @handle_errors
    def post(self):
        """Create new user in Category 4 provider"""
        data = category4_ns.payload
        service = Category4Service(data['username'], data['password'])
        result = service.add_user(data['new_username'], data['new_password'])
        return result, 201