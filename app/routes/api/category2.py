"""
API routes for Category 2 game providers (e.g., Game Vault).
"""

from flask_restx import Namespace, Resource, fields
from app.services.category2_service import Category2Service
from app.models import Provider
from flask import current_app


category2_ns = Namespace('category2', description='Category 2 game provider operations')

# Request models
login_request = category2_ns.model('Category2Login', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Provider username'),
    'password': fields.String(required=True, description='Provider password')
})

user_request = category2_ns.model('Category2AddUser', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'new_username': fields.String(required=True, description='New account username'),
    'new_password': fields.String(required=True, description='New account password')
})

transaction_request = category2_ns.model('Category2Transaction', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Username'),
    'amount': fields.Float(required=True, description='Transaction amount')
})

reset_request = category2_ns.model('Category2ResetPassword', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Username'),
    'new_password': fields.String(required=True, description='New password')
})

balance_request = category2_ns.model('Category2Balance', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Username')
})

agent_balance_request = category2_ns.model('Category2AgentBalance', {
    'provider_id': fields.Integer(required=True, description='Provider ID')
})

# Response model
response_model = category2_ns.model('Response', {
    'message': fields.String(description='Operation status message'),
    'error': fields.String(description='Error message if applicable', required=False),
    'token': fields.String(description='Authentication token', required=False),
    'username': fields.String(description='Username', required=False),
    'balance': fields.String(description='Balance', required=False)
})

@category2_ns.route('/login')
class Category2Login(Resource):
    @category2_ns.expect(login_request)
    @category2_ns.marshal_with(response_model, code=200)
    def post(self):
        """Authenticate with a Category 2 provider."""
        data = category2_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        current_app.logger.info(f"Received request data: {data}")
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            current_app.logger.error(f"No provider found for ID: {data['provider_id']}")
            return {"message": "Invalid provider for Category 2"}, 400
        # Use .name to get the string value of the Enum
        if provider.category.name != 'CATEGORY2':
            current_app.logger.error(f"Provider {provider.id} category mismatch: {provider.category}")
            return {"message": "Invalid provider for Category 2"}, 400
        current_app.logger.info(f"Using provider: {provider.to_dict()}")
        service = Category2Service(provider)
        result = service.login(data['username'], data['password'])
        status_code = 200 if "Login successful" in result["message"] else 400
        return result, status_code

@category2_ns.route('/add_user')
class Category2AddUser(Resource):
    @category2_ns.expect(user_request)
    @category2_ns.marshal_with(response_model, code=201)
    def post(self):
        """Add a new user to a Category 2 provider."""
        data = category2_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY2':
            return {"message": "Invalid provider for Category 2"}, 400
        service = Category2Service(provider)
        result = service.add_user(data['new_username'], data['new_password'])
        status_code = 201 if "User created" in result["message"] else 400
        return result, status_code

@category2_ns.route('/recharge')
class Category2Recharge(Resource):
    @category2_ns.expect(transaction_request)
    @category2_ns.marshal_with(response_model, code=200)
    def post(self):
        """Recharge a user's account in a Category 2 provider."""
        data = category2_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY2':
            return {"message": "Invalid provider for Category 2"}, 400
        service = Category2Service(provider)
        result = service.recharge(data['username'], data['amount'])
        status_code = 200 if "Recharged successfully" in result["message"] else 400
        return result, status_code

@category2_ns.route('/redeem')
class Category2Redeem(Resource):
    @category2_ns.expect(transaction_request)
    @category2_ns.marshal_with(response_model, code=200)
    def post(self):
        """Redeem funds from a user's account in a Category 2 provider."""
        data = category2_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY2':
            return {"message": "Invalid provider for Category 2"}, 400
        service = Category2Service(provider)
        result = service.redeem(data['username'], data['amount'])
        status_code = 200 if "Redeemed successfully" in result["message"] else 400
        return result, status_code

@category2_ns.route('/reset_password')
class Category2ResetPassword(Resource):
    @category2_ns.expect(reset_request)
    @category2_ns.marshal_with(response_model, code=200)
    def post(self):
        """Reset a user's password in a Category 2 provider."""
        data = category2_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY2':
            return {"message": "Invalid provider for Category 2"}, 400
        service = Category2Service(provider)
        result = service.change_password(data['username'], data['new_password'])
        status_code = 200 if "Password changed successfully" in result["message"] else 400
        return result, status_code

@category2_ns.route('/balance')
class Category2Balance(Resource):
    @category2_ns.expect(balance_request)
    @category2_ns.marshal_with(response_model, code=200)
    def post(self):
        """Fetch a user's balance from a Category 2 provider."""
        data = category2_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY2':
            return {"message": "Invalid provider for Category 2"}, 400
        service = Category2Service(provider)
        result = service.get_balances(data['username'])
        status_code = 200 if "Balance fetched" in result["message"] else 400
        return result, status_code

@category2_ns.route('/agent_balance')
class Category2AgentBalance(Resource):
    @category2_ns.expect(agent_balance_request)
    @category2_ns.marshal_with(response_model, code=200)
    def post(self):
        """Fetch the agent's balance from a Category 2 provider."""
        data = category2_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY2':
            return {"message": "Invalid provider for Category 2"}, 400
        service = Category2Service(provider)
        result = service.get_agent_balance()
        status_code = 200 if "Agent balance fetched" in result["message"] else 400
        return result, status_code