
"""
Service class for Category 1 game providers (e.g., Gameroom).
Handles token-based authentication and operations.
"""

from flask_restx import Namespace, Resource, fields
from app.services.category1_service import Category1Service
from app.models import Provider
from flask import current_app

category1_ns = Namespace('category1', description='Category 1 game provider operations')

# Request models
login_request = category1_ns.model('Category1Login', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Provider username'),
    'password': fields.String(required=True, description='Provider password')
})

user_request = category1_ns.model('Category1AddUser', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'new_username': fields.String(required=True, description='New account username'),
    'new_password': fields.String(required=True, description='New account password')
})

transaction_request = category1_ns.model('Category1Transaction', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Username'),
    'amount': fields.Float(required=True, description='Transaction amount')
})

reset_request = category1_ns.model('Category1ResetPassword', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Username'),
    'new_password': fields.String(required=True, description='New password')
})

balance_request = category1_ns.model('Category1Balance', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Username')
})

agent_balance_request = category1_ns.model('Category1AgentBalance', {
    'provider_id': fields.Integer(required=True, description='Provider ID')
})

response_model = category1_ns.model('Response', {
    'message': fields.String(description='Operation status message'),
    'error': fields.String(description='Error message if applicable', required=False),
    'token': fields.String(description='Authentication token', required=False),
    'user_id': fields.String(description='User ID', required=False),
    'username': fields.String(description='Username', required=False),
    'balance': fields.String(description='Balance', required=False)
})

@category1_ns.route('/login')
class Category1Login(Resource):
    @category1_ns.expect(login_request)
    @category1_ns.marshal_with(response_model, code=200)
    def post(self):
        """Authenticate with a Category 1 provider."""
        data = category1_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        current_app.logger.info(f"Received request data: {data}")
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category.name != 'CATEGORY1':
            current_app.logger.error(f"Invalid provider for ID: {data.get('provider_id')}")
            return {"message": "Invalid provider for Category 1"}, 400
        current_app.logger.info(f"Using provider: {provider.to_dict()}")
        service = Category1Service(provider)
        result = service.login(data['username'], data['password'])
        status_code = 200 if "Login successful" in result["message"] else 400
        return result, status_code

@category1_ns.route('/add_user')
class Category1AddUser(Resource):
    @category1_ns.expect(user_request)
    @category1_ns.marshal_with(response_model, code=201)
    def post(self):
        """Add a new user to a Category 1 provider."""
        data = category1_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            current_app.logger.error(f"No provider found for ID: {data['provider_id']}")
            return {"message": "Invalid provider for Category 1"}, 400
        if provider.category.name != 'CATEGORY1':
            current_app.logger.error(f"Provider {provider.id} category mismatch: {provider.category}")
            return {"message": "Invalid provider for Category 1"}, 400
        service = Category1Service(provider)
        result = service.add_user(data['new_username'], data['new_password'])
        status_code = 201 if "User created" in result["message"] else 400
        return result, status_code

@category1_ns.route('/recharge')
class Category1Recharge(Resource):
    @category1_ns.expect(transaction_request)
    @category1_ns.marshal_with(response_model, code=200)
    def post(self):
        """Recharge a user's account in a Category 1 provider."""
        data = category1_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category.name != 'CATEGORY1':
            current_app.logger.error(f"Invalid provider for ID: {data.get('provider_id')}")
            return {"message": "Invalid provider for Category 1"}, 400
        service = Category1Service(provider)
        result = service.recharge(data['username'], data['amount'])
        status_code = 200 if "Recharged successfully" in result["message"] else 400
        return result, status_code

@category1_ns.route('/redeem')
class Category1Redeem(Resource):
    @category1_ns.expect(transaction_request)
    @category1_ns.marshal_with(response_model, code=200)
    def post(self):
        """Redeem funds from a user's account in a Category 1 provider."""
        data = category1_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category.name != 'CATEGORY1':
            current_app.logger.error(f"Invalid provider for ID: {data.get('provider_id')}")
            return {"message": "Invalid provider for Category 1"}, 400
        service = Category1Service(provider)
        result = service.redeem(data['username'], data['amount'])
        status_code = 200 if "Redeemed successfully" in result["message"] else 400
        return result, status_code

@category1_ns.route('/reset_password')
class Category1ResetPassword(Resource):
    @category1_ns.expect(reset_request)
    @category1_ns.marshal_with(response_model, code=200)
    def post(self):
        """Reset a user's password in a Category 1 provider."""
        data = category1_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category.name != 'CATEGORY1':
            current_app.logger.error(f"Invalid provider for ID: {data.get('provider_id')}")
            return {"message": "Invalid provider for Category 1"}, 400
        service = Category1Service(provider)
        result = service.change_password(data['username'], data['new_password'])
        status_code = 200 if "Password changed successfully" in result["message"] else 400
        return result, status_code

@category1_ns.route('/balance')
class Category1Balance(Resource):
    @category1_ns.expect(balance_request)
    @category1_ns.marshal_with(response_model, code=200)
    def post(self):
        """Fetch a user's balance from a Category 1 provider."""
        data = category1_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category.name != 'CATEGORY1':
            current_app.logger.error(f"Invalid provider for ID: {data.get('provider_id')}")
            return {"message": "Invalid provider for Category 1"}, 400
        service = Category1Service(provider)
        result = service.get_balances(data['username'])
        status_code = 200 if "Balance fetched" in result["message"] else 400
        return result, status_code

@category1_ns.route('/agent_balance')
class Category1AgentBalance(Resource):
    @category1_ns.expect(agent_balance_request)
    @category1_ns.marshal_with(response_model, code=200)
    def post(self):
        """Fetch the agent's balance from a Category 1 provider."""
        data = category1_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category.name != 'CATEGORY1':
            current_app.logger.error(f"Invalid provider for ID: {data.get('provider_id')}")
            return {"message": "Invalid provider for Category 1"}, 400
        service = Category1Service(provider)
        result = service.get_agent_balance()
        status_code = 200 if "Agent balance fetched" in result["message"] else 400
        return result, status_code