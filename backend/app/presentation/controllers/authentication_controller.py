# app/presentation/controllers/auth_controller.py
from flask import Blueprint
from flask_restx import Api, Resource, fields
from dependency_injector.wiring import inject, Provide
from app.infrastructure.container import Container
from app.core.application.services.iauthentication_service import IAuthenticationService
from app.core.application.dtos.auth.login_dto import LoginDTO
from app.core.application.dtos.auth.register_dto import RegisterDTO

# Create Blueprint
auth_blueprint = Blueprint('auth_api', __name__)

# Create API instance
api = Api(
    auth_blueprint,
    version='1.0',
    title='Authentication API',
    description='API endpoints for user authentication',
    doc='/docs/auth',
    default_endpoint=None,
    prefix='/auth'
)

# Model Definitions
login_model = api.model('Login', {
    'emailOrUsername': fields.String(required=True, description='User email address or username'),
    'password': fields.String(required=True, description='User password')
})

register_model = api.model('Register', {
    'email': fields.String(required=True, description='User email address'),
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='User password'),
    'confirm_password': fields.String(required=True, description='Confirm password')
})

auth_response_model = api.model('AuthResponse', {
    'access_token': fields.String(description='JWT access token'),
    'refresh_token': fields.String(description='JWT refresh token'),
    'token_type': fields.String(description='Token type', default='Bearer'),
    'access_token_expires': fields.DateTime(description='Access token expiration time'),
    'refresh_token_expires': fields.DateTime(description='Refresh token expiration time'),
    'user_id': fields.Integer(description='User ID'),
    'username': fields.String(description='Username'),
    'email': fields.String(description='User email'),
    'permissions': fields.List(fields.String, description='User permissions')
})

# Controllers
@api.route('/register')
class Register(Resource):
    @api.doc('register_user')
    @api.expect(register_model)
    @api.marshal_with(auth_response_model)
    @api.response(201, 'User successfully registered')
    @api.response(400, 'Validation error')
    @inject
    def post(self, auth_service: IAuthenticationService = Provide[Container.authentication_service]):
        """Register a new user"""
        try:
            register_dto = RegisterDTO(**api.payload)
            return auth_service.register(register_dto), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/login')
class Login(Resource):
    @api.doc('login_user')
    @api.expect(login_model)
    @api.marshal_with(auth_response_model)
    @api.response(200, 'Successfully logged in')
    @api.response(401, 'Authentication failed')
    @inject
    def post(self, auth_service: IAuthenticationService = Provide[Container.authentication_service]):
        """Login user and return tokens"""
        try:
            login_dto = LoginDTO(email_or_username=api.payload['emailOrUsername'], password=api.payload['password'])
            return auth_service.login(login_dto)
        except ValueError as e:
            api.abort(401, str(e))

@api.route('/refresh')
class RefreshToken(Resource):
    @api.doc('refresh_token')
    @api.response(200, 'Token successfully refreshed')
    @api.response(401, 'Invalid refresh token')
    @api.marshal_with(auth_response_model)
    @inject
    def post(self, auth_service: IAuthenticationService = Provide[Container.authentication_service]):
        """Refresh access token using refresh token"""
        try:
            auth_header = api.request_headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                api.abort(401, 'Missing or invalid refresh token')
            refresh_token = auth_header.split(' ')[1]
            return auth_service.refresh_token(refresh_token)
        except ValueError as e:
            api.abort(401, str(e))

@api.route('/logout')
class Logout(Resource):
    @api.doc('logout_user')
    @api.response(204, 'Successfully logged out')
    @api.response(401, 'Authentication required')
    @inject
    def post(self, auth_service: IAuthenticationService = Provide[Container.authentication_service]):
        """Logout user and invalidate tokens"""
        try:
            # Assuming you have a way to get the current user's ID from the token
            # You might want to implement a decorator or middleware for this
            user_id = api.get_current_user_id()  # This is a placeholder
            auth_service.logout(user_id)
            return '', 204
        except ValueError as e:
            api.abort(401, str(e))

# Error handlers
@api.errorhandler(ValueError)
def handle_validation_error(error: ValueError):
    return {'message': str(error), 'error_type': 'Validation Error'}, 400

@api.errorhandler(Exception)
def handle_general_error(error: Exception):
    return {'message': 'An unexpected error occurred', 'error': str(error)}, 500