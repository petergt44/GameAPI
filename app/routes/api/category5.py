"""
API routes for Category g game providers.
"""

from flask_restx import Namespace, Resource, fields
from app.services.category5_service import Category5Service
from app.models import Provider
from flask import current_app

category5_ns = Namespace('category5', description='Category 5 game provider operations')

login_request = category5_ns.model('Category5Login', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Provider username'),
    'password': fields.String(required=True, description='Provider password')
})

user_request = category5_ns.model('Category5AddUser', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'new_username': fields.String(required=True, description='New account username'),
    'new_password': fields.String(required=True, description='New account password')
})

transaction_request = category5_ns.model('Category5Transaction', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Username'),
    'amount': fields.Float(required=True, description='Transaction amount')
})

reset_request = category5_ns.model('Category5ResetPassword', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Username'),
    'new_password': fields.String(required=True, description='New password')
})

balance_request = category5_ns.model('Category5Balance', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Username')
})

agent_balance_request = category5_ns.model('Category5AgentBalance', {
    'provider_id': fields.Integer(required=True, description='Provider ID')
})

response_model = category5_ns.model('Response', {
    'message': fields.String(description='Operation status message'),
    'error': fields.String(description='Error message if applicable', required=False),
    'token': fields.String(description='Authentication token', required=False),
    'username': fields.String(description='Username', required=False),
    'balance': fields.String(description='Balance', required=False)
})

@category5_ns.route('/login')
class Category5Login(Resource):
    @category5_ns.expect(login_request)
    @category5_ns.marshal_with(response_model, code=200)
    def post(self):
        """Authenticate with a Category 5 provider."""
        data = category5_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            current_app.logger.error(f"No provider found for ID: {data['provider_id']}")
            return {"message": "Invalid provider for Category 5"}, 400
        if provider.category.name != 'CATEGORY5':
            current_app.logger.error(f"Provider {provider.id} category mismatch: {provider.category}")
            return {"message": "Invalid provider for Category 5"}, 400
        service = Category5Service(provider)
        result = service.login(data['username'], data['password'])
        status_code = 200 if "Login successful" in result["message"] else 400
        return result, status_code

@category5_ns.route('/add_user')
class Category5AddUser(Resource):
    @category5_ns.expect(user_request)
    @category5_ns.marshal_with(response_model, code=201)
    def post(self):
        """Add a new user to a Category 5 provider."""
        data = category5_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            current_app.logger.error(f"No provider found for ID: {data['provider_id']}")
            return {"message": "Invalid provider for Category 5"}, 400
        if provider.category.name != 'CATEGORY5':
            current_app.logger.error(f"Provider {provider.id} category mismatch: {provider.category}")
            return {"message": "Invalid provider for Category 5"}, 400
        service = Category5Service(provider)
        result = service.add_user(data['new_username'], data['new_password'])
        status_code = 201 if "User created" in result["message"] else 400
        return result, status_code

@category5_ns.route('/recharge')
class Category5Recharge(Resource):
    @category5_ns.expect(transaction_request)
    @category5_ns.marshal_with(response_model, code=200)
    def post(self):
        """Recharge a user's account in a Category 5 provider."""
        data = category5_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            current_app.logger.error(f"No provider found for ID: {data['provider_id']}")
            return {"message": "Invalid provider for Category 5"}, 400
        if provider.category.name != 'CATEGORY5':
            current_app.logger.error(f"Provider {provider.id} category mismatch: {provider.category}")
            return {"message": "Invalid provider for Category 5"}, 400
        service = Category5Service(provider)
        result = service.recharge(data['username'], data['amount'])
        status_code = 200 if "Recharged successfully" in result["message"] else 400
        return result, status_code

@category5_ns.route('/redeem')
class Category5Redeem(Resource):
    @category5_ns.expect(transaction_request)
    @category5_ns.marshal_with(response_model, code=200)
    def post(self):
        """Redeem funds from a user's account in a Category 5 provider."""
        data = category5_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            current_app.logger.error(f"No provider found for ID: {data['provider_id']}")
            return {"message": "Invalid provider for Category 5"}, 400
        if provider.category.name != 'CATEGORY5':
            current_app.logger.error(f"Provider {provider.id} category mismatch: {provider.category}")
            return {"message": "Invalid provider for Category 5"}, 400
        service = Category5Service(provider)
        result = service.redeem(data['username'], data['amount'])
        status_code = 200 if "Redeemed successfully" in result["message"] else 400
        return result, status_code

@category5_ns.route('/reset_password')
class Category5ResetPassword(Resource):
    @category5_ns.expect(reset_request)
    @category5_ns.marshal_with(response_model, code=200)
    def post(self):
        """Reset a user's password in a Category 5 provider."""
        data = category5_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            current_app.logger.error(f"No provider found for ID: {data['provider_id']}")
            return {"message": "Invalid provider for Category 5"}, 400
        if provider.category.name != 'CATEGORY5':
            current_app.logger.error(f"Provider {provider.id} category mismatch: {provider.category}")
            return {"message": "Invalid provider for Category 5"}, 400
        service = Category5Service(provider)
        result = service.change_password(data['username'], data['new_password'])
        status_code = 200 if "Password changed successfully" in result["message"] else 400
        return result, status_code

@category5_ns.route('/balance')
class Category5Balance(Resource):
    @category5_ns.expect(balance_request)
    @category5_ns.marshal_with(response_model, code=200)
    def post(self):
        """Fetch a user's balance from a Category 5 provider."""
        data = category5_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            current_app.logger.error(f"No provider found for ID: {data['provider_id']}")
            return {"message": "Invalid provider for Category 5"}, 400
        if provider.category.name != 'CATEGORY5':
            current_app.logger.error(f"Provider {provider.id} category mismatch: {provider.category}")
            return {"message": "Invalid provider for Category 5"}, 400
        service = Category5Service(provider)
        result = service.get_balances(data['username'])
        status_code = 200 if "Balance fetched" in result["message"] else 400
        return result, status_code

@category5_ns.route('/agent_balance')
class Category5AgentBalance(Resource):
    @category5_ns.expect(agent_balance_request)
    @category5_ns.marshal_with(response_model, code=200)
    def post(self):
        """Fetch the agent's balance from a Category 5 provider."""
        data = category5_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            current_app.logger.error(f"No provider found for ID: {data['provider_id']}")
            return {"message": "Invalid provider for Category 5"}, 400
        if provider.category.name != 'CATEGORY5':
            current_app.logger.error(f"Provider {provider.id} category mismatch: {provider.category}")
            return {"message": "Invalid provider for Category 5"}, 400
        service = Category5Service(provider)
        result = service.get_agent_balance()
        status_code = 200 if "Agent balance fetched" in result["message"] else 400
        return result, status_code