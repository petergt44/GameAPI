from flask_restx import Namespace, Resource, fields
from app.services.category1_service import Category1Service
from app.utils.error_handling import handle_errors

category1_ns = Namespace('category1', description='Category 1 game provider operations')

# Request models
login_request = category1_ns.model('LoginRequest', {
    'username': fields.String(required=True, description='Game provider username'),
    'password': fields.String(required=True, description='Game provider password')
})

user_request = category1_ns.model('UserRequest', {
    'new_username': fields.String(required=True, description='New username'),
    'new_password': fields.String(required=True, description='New password')
})

# Response models
login_response = category1_ns.model('LoginResponse', {
    'message': fields.String(description='Login status message'),
    'token': fields.String(description='Authentication token')
})

user_response = category1_ns.model('UserResponse', {
    'message': fields.String(description='Operation result'),
    'user_id': fields.String(description='Created user ID')
})

@category1_ns.route('/login')
class Category1Login(Resource):
    @category1_ns.expect(login_request)
    @category1_ns.response(200, 'Success', login_response)
    @category1_ns.response(401, 'Invalid credentials')
    @handle_errors
    def post(self):
        """Authenticate with Category 1 provider"""
        data = category1_ns.payload
        service = Category1Service(data['username'], data['password'])
        result = service.login()
        return result, 200

@category1_ns.route('/add_user')
class Category1AddUser(Resource):
    @category1_ns.expect(login_request, user_request)
    @category1_ns.response(201, 'User created', user_response)
    @category1_ns.response(400, 'Bad request')
    @handle_errors
    def post(self):
        """Create new user in Category 1 provider"""
        data = category1_ns.payload
        service = Category1Service(data['username'], data['password'])
        result = service.add_user(data['new_username'], data['new_password'])
        return result, 201

@category1_ns.route('/recharge')
class Category1Recharge(Resource):
    @category1_ns.expect(login_request, {
        'username': fields.String(required=True),
        'amount': fields.Float(required=True)
    })
    @category1_ns.response(200, 'Success')
    @handle_errors
    def post(self):
        """Recharge user balance"""
        data = category1_ns.payload
        service = Category1Service(data['username'], data['password'])
        result = service.recharge(data['username'], data['amount'])
        return result, 200