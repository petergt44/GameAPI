"""
API routes for Category 3 game providers (e.g., Fire Kirin).
"""

from flask_restx import Namespace, Resource, fields
from app.services.category3_service import Category3Service
from app.models import Provider

category3_ns = Namespace('category3', description='Category 3 game provider operations')

# Request models
login_request = category3_ns.model('Category3Login', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Provider username'),
    'password': fields.String(required=True, description='Provider password')
})

user_request = category3_ns.model('Category3AddUser', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'new_username': fields.String(required=True, description='New account username'),
    'new_password': fields.String(required=True, description='New account password')
})

transaction_request = category3_ns.model('Category3Transaction', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Username'),
    'amount': fields.Float(required=True, description='Transaction amount')
})

reset_request = category3_ns.model('Category3ResetPassword', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Username'),
    'new_password': fields.String(required=True, description='New password')
})

balance_request = category3_ns.model('Category3Balance', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='Username')
})

agent_balance_request = category3_ns.model('Category3AgentBalance', {
    'provider_id': fields.Integer(required=True, description='Provider ID')
})

# Response model
response_model = category3_ns.model('Response', {
    'message': fields.String(description='Operation status message'),
    'error': fields.String(description='Error message if applicable', required=False),
    'username': fields.String(description='Username', required=False),
    'balance': fields.String(description='Balance', required=False)
})

@category3_ns.route('/login')
class Category3Login(Resource):
    @category3_ns.expect(login_request)
    @category3_ns.marshal_with(response_model, code=200)
    def post(self):
        """Authenticate with a Category 3 provider."""
        data = category3_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY3':
            return {"message": "Invalid provider for Category 3"}, 400
        service = Category3Service(provider)
        result = service.login(data['username'], data['password'])
        status_code = 200 if "Login successful" in result["message"] else 400
        return result, status_code

@category3_ns.route('/add_user')
class Category3AddUser(Resource):
    @category3_ns.expect(user_request)
    @category3_ns.marshal_with(response_model, code=201)
    def post(self):
        """Add a new user to a Category 3 provider."""
        data = category3_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY3':
            return {"message": "Invalid provider for Category 3"}, 400
        service = Category3Service(provider)
        result = service.add_user(data['new_username'], data['new_password'])
        status_code = 201 if "User created" in result["message"] else 400
        return result, status_code

@category3_ns.route('/recharge')
class Category3Recharge(Resource):
    @category3_ns.expect(transaction_request)
    @category3_ns.marshal_with(response_model, code=200)
    def post(self):
        """Recharge a user's account in a Category 3 provider."""
        data = category3_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY3':
            return {"message": "Invalid provider for Category 3"}, 400
        service = Category3Service(provider)
        result = service.recharge(data['username'], data['amount'])
        status_code = 200 if "Recharged successfully" in result["message"] else 400
        return result, status_code

@category3_ns.route('/redeem')
class Category3Redeem(Resource):
    @category3_ns.expect(transaction_request)
    @category3_ns.marshal_with(response_model, code=200)
    def post(self):
        """Redeem funds from a user's account in a Category 3 provider."""
        data = category3_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY3':
            return {"message": "Invalid provider for Category 3"}, 400
        service = Category3Service(provider)
        result = service.redeem(data['username'], data['amount'])
        status_code = 200 if "Redeemed successfully" in result["message"] else 400
        return result, status_code

@category3_ns.route('/reset_password')
class Category3ResetPassword(Resource):
    @category3_ns.expect(reset_request)
    @category3_ns.marshal_with(response_model, code=200)
    def post(self):
        """Reset a user's password in a Category 3 provider."""
        data = category3_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY3':
            return {"message": "Invalid provider for Category 3"}, 400
        service = Category3Service(provider)
        result = service.change_password(data['username'], data['new_password'])
        status_code = 200 if "Password changed successfully" in result["message"] else 400
        return result, status_code

@category3_ns.route('/balance')
class Category3Balance(Resource):
    @category3_ns.expect(balance_request)
    @category3_ns.marshal_with(response_model, code=200)
    def post(self):
        """Fetch a user's balance from a Category 3 provider."""
        data = category3_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY3':
            return {"message": "Invalid provider for Category 3"}, 400
        service = Category3Service(provider)
        result = service.get_balances(data['username'])
        status_code = 200 if "Balance fetched" in result["message"] else 400
        return result, status_code

@category3_ns.route('/agent_balance')
class Category3AgentBalance(Resource):
    @category3_ns.expect(agent_balance_request)
    @category3_ns.marshal_with(response_model, code=200)
    def post(self):
        """Fetch the agent's balance from a Category 3 provider."""
        data = category3_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY3':
            return {"message": "Invalid provider for Category 3"}, 400
        service = Category3Service(provider)
        result = service.get_agent_balance()
        status_code = 200 if "Agent balance fetched" in result["message"] else 400
        return result, status_code