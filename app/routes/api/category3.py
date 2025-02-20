"""
API routes for Category 3 game providers.
"""

from flask_restx import Namespace, Resource, fields
from app.services.category3_service import Category3Service
from app.models import Provider

category3_ns = Namespace('category3', description='Category 3 game operations')

user_request = category3_ns.model('Category3AddUser', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'new_username': fields.String(required=True, description='New account username'),
    'new_password': fields.String(required=True, description='New account password')
})

recharge_request = category3_ns.model('Category3Recharge', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='User account username'),
    'amount': fields.Float(required=True, description='Amount to recharge/redeem')
})

balance_request = category3_ns.model('Category3Balance', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='User account username')
})

password_request = category3_ns.model('Category3ChangePassword', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='User account username'),
    'new_password': fields.String(required=True, description='New password')
})

agent_balance_request = category3_ns.model('Category3AgentBalance', {
    'provider_id': fields.Integer(required=True, description='Provider ID')
})

@category3_ns.route('/add_user')
class Category3AddUser(Resource):
    @category3_ns.expect(user_request)
    def post(self):
        """Add a new user to a Category 3 provider."""
        data = category3_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY3':
            return {"message": "Invalid provider for Category 3"}, 400
        service = Category3Service(provider)
        result = service.add_user(data['new_username'], data['new_password'])
        return result, 201 if "User created" in result["message"] else 400

@category3_ns.route('/recharge')
class Category3Recharge(Resource):
    @category3_ns.expect(recharge_request)
    def post(self):
        """Recharge a user's account."""
        data = category3_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY3':
            return {"message": "Invalid provider for Category 3"}, 400
        service = Category3Service(provider)
        result = service.recharge(data['username'], data['amount'])
        return result, 200 if "Recharged successfully" in result["message"] else 400

@category3_ns.route('/redeem')
class Category3Redeem(Resource):
    @category3_ns.expect(recharge_request)
    def post(self):
        """Redeem funds from a user's account."""
        data = category3_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY3':
            return {"message": "Invalid provider for Category 3"}, 400
        service = Category3Service(provider)
        result = service.redeem(data['username'], data['amount'])
        return result, 200 if "Redeemed successfully" in result["message"] else 400

@category3_ns.route('/balance')
class Category3Balance(Resource):
    @category3_ns.expect(balance_request)
    def post(self):
        """Fetch a user's balance."""
        data = category3_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY3':
            return {"message": "Invalid provider for Category 3"}, 400
        service = Category3Service(provider)
        result = service.get_balances(data['username'])
        return result, 200 if "Balance fetched" in result["message"] else 400

@category3_ns.route('/change_password')
class Category3ChangePassword(Resource):
    @category3_ns.expect(password_request)
    def post(self):
        """Change a user's password."""
        data = category3_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY3':
            return {"message": "Invalid provider for Category 3"}, 400
        service = Category3Service(provider)
        result = service.change_password(data['username'], data['new_password'])
        return result, 200 if "Password changed" in result["message"] else 400

@category3_ns.route('/agent_balance')
class Category3AgentBalance(Resource):
    @category3_ns.expect(agent_balance_request)
    def post(self):
        """Fetch the agent's balance."""
        data = category3_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY3':
            return {"message": "Invalid provider for Category 3"}, 400
        service = Category3Service(provider)
        result = service.get_agent_balance()
        return result, 200 if "Agent balance fetched" in result["message"] else 400