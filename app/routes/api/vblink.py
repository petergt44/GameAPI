from flask_restx import Namespace, Resource, fields

# Create a namespace for VBLink
vblink_ns = Namespace('vblink', description='VBLink game provider operations')

# Define a model for the API response
login_model = vblink_ns.model('LoginResponse', {
    'message': fields.String(description='Login status message'),
    'token': fields.String(description='Authentication token')
})

@vblink_ns.route('/login')
class VBlinkLogin(Resource):
    @vblink_ns.doc('login')
    @vblink_ns.response(200, 'Login successful', login_model)
    def post(self):
        """Login to the VBLink game provider."""
        return {
            'message': 'Login successful',
            'token': 'abc123'
        }, 200