"""
API routes for Category 1 game providers.
"""

from flask_restx import Namespace, Resource, fields
from app.services.category1_service import Category1Service
from app.models import Provider
from app import db

category1_ns = Namespace('category1', description='Category 1 game operations')

# Request models
user_request = category1_ns.model('Category1AddUser', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'new_username': fields.String(required=True, description='New account username'),
    'new_password': fields.String(required=True, description='New account password')
})

recharge_request = category1_ns.model('Category1Recharge', {
    'provider_id': fields.Integer(required=True, description='Provider ID'),
    'username': fields.String(required=True, description='User account username'),
    'amount': fields.Float(required=True, description='Amount to recharge')
})

@category1_ns.route('/add_user')
class Category1AddUser(Resource):
    @category1_ns.expect(user_request)
    def post(self):
        """Add a new user to a Category 1 provider."""
        data = category1_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY1':
            return {"message": "Invalid provider for Category 1"}, 400
        service = Category1Service(provider)
        result = service.add_user(data['new_username'], data['new_password'])
        return result, 201 if "User created" in result["message"] else 400

@category1_ns.route('/recharge')
class Category1Recharge(Resource):
    @category1_ns.expect(recharge_request)
    def post(self):
        """Recharge a user's account for a Category 1 provider."""
        data = category1_ns.payload
        provider = Provider.query.get(data['provider_id'])
        if not provider or provider.category != 'CATEGORY1':
            return {"message": "Invalid provider for Category 1"}, 400
        service = Category1Service(provider)
        result = service.recharge(data['username'], data['amount'])
        return result, 200 if "Recharged successfully" in result["message"] else 400
