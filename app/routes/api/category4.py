"""
API routes for Category 4 game providers.
"""

from flask_restx import Namespace, Resource, fields
from app.services.category4_service import Category4Service
from app.models import Provider

category4_ns = Namespace('category4', description='Category 4 game operations')

user_request = category4_ns.model('Category4AddUser', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'new_username': fields.String(required=True, description='New account username'),
    'new_password': fields.String(required=True, description='New account password')
})

recharge_request = category4_ns.model('Category4Recharge', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='User account username'),
    'amount': fields.Float(required=True, description='Amount to recharge/redeem')
})

balance_request = category4_ns.model('Category4Balance', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='User account username')
})

password_request = category4_ns.model('Category4ChangePassword', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='User account username'),
    'new_password': fields.String(required=True, description='New password')
})

agent_balance_request = category4_ns.model('Category4AgentBalance', {
    'provider_id': fields.Integer(required=True, description='Provider ID')
})

@category4_ns.route('/add_user')
class Category4AddUser(Resource):
    @category4_ns.expect(user_request)
    def post(self):
        """Add a new user to a Category 4 provider."""
        data = category4_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY4':
            return {"message": "Invalid provider for Category 4"}, 400
        service = Category4Service(provider)
        result = service.add_user(data['new_username'], data['new_password'])
        return result, 201 if "User created" in result["message"] else 400

@category4_ns.route('/recharge')
class Category4Recharge(Resource):
    @category4_ns.expect(recharge_request)
    def post(self):
        """Recharge a user's account."""
        data = category4_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY4':
            return {"message": "Invalid provider for Category 4"}, 400
        service = Category4Service(provider)
        result = service.recharge(data['username'], data['amount'])
        return result, 200 if "Recharged successfully" in result["message"] else 400

@category4_ns.route('/redeem')
class Category4Redeem(Resource):
    @category4_ns.expect(recharge_request)
    def post(self):
        """Redeem funds from a user's account."""
        data = category4_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY4':
            return {"message": "Invalid provider for Category 4"}, 400
        service = Category4Service(provider)
        result = service.redeem(data['username'], data['amount'])
        return result, 200 if "Redeemed successfully" in result["message"] else 400

@category4_ns.route('/balance')
class Category4Balance(Resource):
    @category4_ns.expect(balance_request)
    def post(self):
        """Fetch a user's balance."""
        data = category4_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY4':
            return {"message": "Invalid provider for Category 4"}, 400
        service = Category4Service(provider)
        result = service.get_balances(data['username'])
        return result, 200 if "Balance fetched" in result["message"] else 400

@category4_ns.route('/change_password')
class Category4ChangePassword(Resource):
    @category4_ns.expect(password_request)
    def post(self):
        """Change a user's password."""
        data = category4_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY4':
            return {"message": "Invalid provider for Category 4"}, 400
        service = Category4Service(provider)
        result = service.change_password(data['username'], data['new_password'])
        return result, 200 if "Password changed" in result["message"] else 400

@category4_ns.route('/agent_balance')
class Category4AgentBalance(Resource):
    @category4_ns.expect(agent_balance_request)
    def post(self):
        """Fetch the agent's balance."""
        data = category4_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY4':
            return {"message": "Invalid provider for Category 4"}, 400
        service = Category4Service(provider)
        result = service.get_agent_balance()
        return result, 200 if "Agent balance fetched" in result["message"] else 400