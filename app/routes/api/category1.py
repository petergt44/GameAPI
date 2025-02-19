"""
Namespaces Service to instantiate Category1
"""

from flask_restx import Namespace, Resource, fields
from app.services.category1_service import Category1Service

category1_ns = Namespace('category1', description='Category 1 game provider operations')

login_request = category1_ns.model('Category1Login', {
    'username': fields.String(required=True, description='Provider username'),
    'password': fields.String(required=True, description='Provider password')
})
user_request = category1_ns.model('Category1AddUser', {
    'username': fields.String(required=True, description='Admin username'),
    'password': fields.String(required=True, description='Admin password'),
    'new_username': fields.String(required=True, description='New account username'),
    'new_password': fields.String(required=True, description='New account password')
})
transaction_request = category1_ns.model('Category1Transaction', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
    'amount': fields.Float(required=True, description='Transaction amount')
})
reset_request = category1_ns.model('Category1Reset', {
    'username': fields.String(required=True, description='Username'),
    'new_password': fields.String(required=True, description='New password')
})

@category1_ns.route('/login')
class Category1Login(Resource):
    @category1_ns.expect(login_request)
    def post(self):
        data = category1_ns.payload
        service = Category1Service()
        return service.login(data['username'], data['password'])

@category1_ns.route('/add_user')
class Category1AddUser(Resource):
    @category1_ns.expect(user_request)
    def post(self):
        data = category1_ns.payload
        service = Category1Service()
        return service.add_user(data['new_username'], data['new_password']), 201

@category1_ns.route('/recharge')
class Category1Recharge(Resource):
    @category1_ns.expect(transaction_request)
    def post(self):
        data = category1_ns.payload
        service = Category1Service()
        return service.recharge(data['username'], data['amount'])

@category1_ns.route('/redeem')
class Category1Redeem(Resource):
    @category1_ns.expect(transaction_request)
    def post(self):
        data = category1_ns.payload
        service = Category1Service()
        return service.redeem(data['username'], data['amount'])

@category1_ns.route('/reset_password')
class Category1ResetPassword(Resource):
    @category1_ns.expect(reset_request)
    def post(self):
        data = category1_ns.payload
        service = Category1Service()
        return service.reset_password(data['username'], data['new_password'])

@category1_ns.route('/balance')
class Category1Balance(Resource):
    @category1_ns.expect(login_request)
    def post(self):
        data = category1_ns.payload
        service = Category1Service()
        return service.get_balances(data['username'])
