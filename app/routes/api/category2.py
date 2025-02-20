"""
API routes for Category 2 game providers.
"""

from flask_restx import Namespace, Resource, fields
from app.services.category2_service import Category2Service
from app.models import Provider

category2_ns = Namespace('category2', description='Category 2 game operations')

user_request = category2_ns.model('Category2AddUser', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'new_username': fields.String(required=True, description='New account username'),
    'new_password': fields.String(required=True, description='New account password')
})

recharge_request = category2_ns.model('Category2Recharge', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='User account username'),
    'amount': fields.Float(required=True, description='Amount to recharge/redeem')
})

balance_request = category2_ns.model('Category2Balance', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='User account username')
})

password_request = category2_ns.model('Category2ChangePassword', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='User account username'),
    'new_password': fields.String(required=True, description='New password')
})

agent_balance_request = category2_ns.model('Category2AgentBalance', {
    'provider_id': fields.Integer(required=True, description='Provider ID')
})

@category2_ns.route('/add_user')
class Category2AddUser(Resource):
    @category2_ns.expect(user_request)
    def post(self):
        """Add a new user to a Category 2 provider."""
        data = category2_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY2':
            return {"message": "Invalid provider for Category 2"}, 400
        service = Category2Service(provider)
        result = service.add_user(data['new_username'], data['new_password'])
        return result, 201 if "User created" in result["message"] else 400

@category2_ns.route('/recharge')
class Category2Recharge(Resource):
    @category2_ns.expect(recharge_request)
    def post(self):
        """Recharge a user's account."""
        data = category2_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY2':
            return {"message": "Invalid provider for Category 2"}, 400
        service = Category2Service(provider)
        result = service.recharge(data['username'], data['amount'])
        return result, 200 if "Recharged successfully" in result["message"] else 400

@category2_ns.route('/redeem')
class Category2Redeem(Resource):
    @category2_ns.expect(recharge_request)
    def post(self):
        """Redeem funds from a user's account."""
        data = category2_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY2':
            return {"message": "Invalid provider for Category 2"}, 400
        service = Category2Service(provider)
        result = service.redeem(data['username'], data['amount'])
        return result, 200 if "Redeemed successfully" in result["message"] else 400

@category2_ns.route('/balance')
class Category2Balance(Resource):
    @category2_ns.expect(balance_request)
    def post(self):
        """Fetch a user's balance."""
        data = category2_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY2':
            return {"message": "Invalid provider for Category 2"}, 400
        service = Category2Service(provider)
        result = service.get_balances(data['username'])
        return result, 200 if "Balance fetched" in result["message"] else 400

@category2_ns.route('/change_password')
class Category2ChangePassword(Resource):
    @category2_ns.expect(password_request)
    def post(self):
        """Change a user's password."""
        data = category2_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY2':
            return {"message": "Invalid provider for Category 2"}, 400
        service = Category2Service(provider)
        result = service.change_password(data['username'], data['new_password'])
        return result, 200 if "Password changed" in result["message"] else 400

@category2_ns.route('/agent_balance')
class Category2AgentBalance(Resource):
    @category2_ns.expect(agent_balance_request)
    def post(self):
        """Fetch the agent's balance."""
        data = category2_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY2':
            return {"message": "Invalid provider for Category 2"}, 400
        service = Category2Service(provider)
        result = service.get_agent_balance()
        return result, 200 if "Agent balance fetched" in result["message"] else 400