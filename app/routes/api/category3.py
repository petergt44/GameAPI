from flask_restx import Namespace, Resource, fields
from app.services.category3_service import Category3Service
from app.utils.error_handling import handle_errors

category3_ns = Namespace('category3', description='Category 3 game provider operations')

# Request models
login_request = category3_ns.model('LoginRequest', {
    'username': fields.String(required=True, description='Game provider username'),
    'password': fields.String(required=True, description='Game provider password')
})

user_request = category3_ns.model('UserRequest', {
    'new_username': fields.String(required=True, description='New username'),
    'new_password': fields.String(required=True, description='New password')
})

# Response models
login_response = category3_ns.model('LoginResponse', {
    'message': fields.String(description='Login status message'),
    'token': fields.String(description='Authentication token')
})

user_response = category3_ns.model('UserResponse', {
    'message': fields.String(description='Operation result'),
    'user_id': fields.String(description='Created user ID')
})

@category3_ns.route('/login')
class Category3Login(Resource):
    @category3_ns.expect(login_request)
    @category3_ns.response(200, 'Success', login_response)
    @category3_ns.response(401, 'Invalid credentials')
    @handle_errors
    def post(self):
        """Authenticate with Category 3 provider"""
        data = category3_ns.payload
        service = Category3Service(data['username'], data['password'])
        result = service.login()
        return result, 200

@category3_ns.route('/add_user')
class Category3AddUser(Resource):
    @category3_ns.expect(login_request, user_request)
    @category3_ns.response(201, 'User created', user_response)
    @category3_ns.response(400, 'Bad request')
    @handle_errors
    def post(self):
        """Create new user in Category 3 provider"""
        data = category3_ns.payload
        service = Category3Service(data['username'], data['password'])
        result = service.add_user(data['new_username'], data['new_password'])
        return result, 201

@category3_ns.route('/recharge')
class Category3Recharge(Resource):
    @category3_ns.expect(login_request, {
        'username': fields.String(required=True),
        'amount': fields.Float(required=True)
    })
    @category3_ns.response(200, 'Success')
    @handle_errors
    def post(self):
        """Recharge user balance"""
        data = category3_ns.payload
        service = Category3Service(data['username'], data['password'])
        result = service.recharge(data['username'], data['amount'])
        return result, 200