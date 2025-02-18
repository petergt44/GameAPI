from flask_restx import Namespace, Resource, fields
from app.services.category2_service import Category2Service
from app.utils.error_handling import handle_errors

category2_ns = Namespace('category2', description='Category 2 game provider operations')

login_request = category2_ns.model('LoginRequest', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

user_request = category2_ns.model('UserRequest', {
    'new_username': fields.String(required=True),
    'new_password': fields.String(required=True)
})

@category2_ns.route('/login')
class Category2Login(Resource):
    @category2_ns.expect(login_request)
    @category2_ns.response(200, 'Success')
    @handle_errors
    def post(self):
        data = category2_ns.payload
        service = Category2Service(data['username'], data['password'])
        result = service.login()
        return result, 200

@category2_ns.route('/add_user')
class Category2AddUser(Resource):
    @category2_ns.expect(login_request, user_request)
    @category2_ns.response(201, 'User created')
    @handle_errors
    def post(self):
        data = category2_ns.payload
        service = Category2Service(data['username'], data['password'])
        result = service.add_user(data['new_username'], data['new_password'])
        return result, 201