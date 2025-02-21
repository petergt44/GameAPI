"""
API routes for Category 4 game providers (e.g., Vblink).
"""

from flask_restx import Namespace, Resource, fields
from app.services.category4_service import Category4Service
from app.models import Provider
from flask import current_app

category4_ns = Namespace('category4', description='Category 4 game provider operations')

login_request = category4_ns.model('Category4Login', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Provider username'),
    'password': fields.String(required=True, description='Provider password')
})

user_request = category4_ns.model('Category4AddUser', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'new_username': fields.String(required=True, description='New account username'),
    'new_password': fields.String(required=True, description='New account password')
})

transaction_request = category4_ns.model('Category4Transaction', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Username'),
    'amount': fields.Float(required=True, description='Transaction amount')
})

reset_request = category4_ns.model('Category4ResetPassword', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Username'),
    'new_password': fields.String(required=True, description='New password')
})

balance_request = category4_ns.model('Category4Balance', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Username')
})

agent_balance_request = category4_ns.model('Category4AgentBalance', {
    'provider_id': fields.Integer(required=True, description='Provider ID')
})

response_model = category4_ns.model('Response', {
    'message': fields.String(description='Operation status message'),
    'error': fields.String(description='Error message if applicable', required=False),
    'token': fields.String(description='Authentication token', required=False),
    'username': fields.String(description='Username', required=False),
    'balance': fields.String(description='Balance', required=False)
})

@category4_ns.route('/login')
class Category4Login(Resource):
    @category4_ns.expect(login_request)
    @category4_ns.marshal_with(response_model, code=200)
    def post(self):
        """Authenticate with a Category 4 provider."""
        data = category4_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            current_app.logger.error(f"No provider found for ID: {data['provider_id']}")
            return {"message": "Invalid provider for Category 4"}, 400
        if provider.category.name != 'CATEGORY4':
            current_app.logger.error(f"Provider {provider.id} category mismatch: {provider.category}")
            return {"message": "Invalid provider for Category 4"}, 400
        service = Category4Service(provider)
        result = service.login(data['username'], data['password'])
        status_code = 200 if "Login successful" in result["message"] else 400
        return result, status_code

@category4_ns.route('/add_user')
class Category4AddUser(Resource):
    @category4_ns.expect(user_request)
    @category4_ns.marshal_with(response_model, code=201)
    def post(self):
        """Add a new user to a Category 4 provider."""
        data = category4_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            current_app.logger.error(f"No provider found for ID: {data['provider_id']}")
            return {"message": "Invalid provider for Category 4"}, 400
        if provider.category.name != 'CATEGORY4':
            current_app.logger.error(f"Provider {provider.id} category mismatch: {provider.category}")
            return {"message": "Invalid provider for Category 4"}, 400
        service = Category4Service(provider)
        result = service.add_user(data['new_username'], data['new_password'])
        status_code = 201 if "User created" in result["message"] else 400
        return result, status_code

@category4_ns.route('/recharge')
class Category4Recharge(Resource):
    @category4_ns.expect(transaction_request)
    @category4_ns.marshal_with(response_model, code=200)
    def post(self):
        """Recharge a user's account in a Category 4 provider."""
        data = category4_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            current_app.logger.error(f"No provider found for ID: {data['provider_id']}")
            return {"message": "Invalid provider for Category 4"}, 400
        if provider.category.name != 'CATEGORY4':
            current_app.logger.error(f"Provider {provider.id} category mismatch: {provider.category}")
            return {"message": "Invalid provider for Category 4"}, 400
        service = Category4Service(provider)
        result = service.recharge(data['username'], data['amount'])
        status_code = 200 if "Recharged successfully" in result["message"] else 400
        return result, status_code

@category4_ns.route('/redeem')
class Category4Redeem(Resource):
    @category4_ns.expect(transaction_request)
    @category4_ns.marshal_with(response_model, code=200)
    def post(self):
        """Redeem funds from a user's account in a Category 4 provider."""
        data = category4_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            current_app.logger.error(f"No provider found for ID: {data['provider_id']}")
            return {"message": "Invalid provider for Category 4"}, 400
        if provider.category.name != 'CATEGORY4':
            current_app.logger.error(f"Provider {provider.id} category mismatch: {provider.category}")
            return {"message": "Invalid provider for Category 4"}, 400
        service = Category4Service(provider)
        result = service.redeem(data['username'], data['amount'])
        status_code = 200 if "Redeemed successfully" in result["message"] else 400
        return result, status_code

@category4_ns.route('/reset_password')
class Category4ResetPassword(Resource):
    @category4_ns.expect(reset_request)
    @category4_ns.marshal_with(response_model, code=200)
    def post(self):
        """Reset a user's password in a Category 4 provider."""
        data = category4_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            current_app.logger.error(f"No provider found for ID: {data['provider_id']}")
            return {"message": "Invalid provider for Category 4"}, 400
        if provider.category.name != 'CATEGORY4':
            current_app.logger.error(f"Provider {provider.id} category mismatch: {provider.category}")
            return {"message": "Invalid provider for Category 4"}, 400
        service = Category4Service(provider)
        result = service.change_password(data['username'], data['new_password'])
        status_code = 200 if "Password changed successfully" in result["message"] else 400
        return result, status_code

@category4_ns.route('/balance')
class Category4Balance(Resource):
    @category4_ns.expect(balance_request)
    @category4_ns.marshal_with(response_model, code=200)
    def post(self):
        """Fetch a user's balance from a Category 4 provider."""
        data = category4_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            current_app.logger.error(f"No provider found for ID: {data['provider_id']}")
            return {"message": "Invalid provider for Category 4"}, 400
        if provider.category.name != 'CATEGORY4':
            current_app.logger.error(f"Provider {provider.id} category mismatch: {provider.category}")
            return {"message": "Invalid provider for Category 4"}, 400
        service = Category4Service(provider)
        result = service.get_balances(data['username'])
        status_code = 200 if "Balance fetched" in result["message"] else 400
        return result, status_code

@category4_ns.route('/agent_balance')
class Category4AgentBalance(Resource):
    @category4_ns.expect(agent_balance_request)
    @category4_ns.marshal_with(response_model, code=200)
    def post(self):
        """Fetch the agent's balance from a Category 4 provider."""
        data = category4_ns.payload
        if data is None:
            return {"message": "Request body is missing or invalid", "error": "Please provide a valid JSON payload"}, 400
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            current_app.logger.error(f"No provider found for ID: {data['provider_id']}")
            return {"message": "Invalid provider for Category 4"}, 400
        if provider.category.name != 'CATEGORY4':
            current_app.logger.error(f"Provider {provider.id} category mismatch: {provider.category}")
            return {"message": "Invalid provider for Category 4"}, 400
        service = Category4Service(provider)
        result = service.get_agent_balance()
        status_code = 200 if "Agent balance fetched" in result["message"] else 400
        return result, status_code