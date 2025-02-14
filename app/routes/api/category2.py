from flask_restx import Namespace, Resource, fields
from app.services.category2_service import Category2Service

category2_ns = Namespace('category2', description='Category 2 game provider operations')

# Define models
login_model = category2_ns.model('LoginResponse', {
    'message': fields.String(description='Login status message'),
    'token': fields.String(description='Authentication token')
})

@category2_ns.route('/login')
class Category2Login(Resource):
    @category2_ns.doc('login')
    @category2_ns.response(200, 'Login successful', login_model)
    def post(self):
        """Login to a Category 2 game provider."""
        service = Category2Service(base_url="https://example.com", username="user", password="pass")
        return service.login()