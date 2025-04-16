# app/presentation/controllers/user_controller.py
from flask import Blueprint
from flask_restx import Api, Namespace, Resource, fields
from dependency_injector.wiring import inject, Provide
from app.infrastructure.container import Container
from app.core.application.services.iuser_service import IUserService
from app.core.application.dtos.user.create_user_dto import CreateUserDTO
from app.core.application.dtos.user.update_user_dto import UpdateUserDTO, UpdateUserSystemDTO, UpdatePasswordDTO

# Create Blueprint
user_blueprint = Blueprint('user_api', __name__)

# Create API instance
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Enter your bearer token in the format: Bearer <token>'
    }
}

api = Api(
    user_blueprint,
    version='1.0',
    title='User Management API',
    description='API endpoints for user management',
    doc='/docs/users',
    authorizations=authorizations,
    security='Bearer',
    default_endpoint=None,
    prefix='/users'
)

# Model Definitions
user_model = api.model('User', {
    'id': fields.Integer(description='User identifier'),
    'email': fields.String(required=True, description='User email address'),
    'username': fields.String(required=True, description='Username')
})

user_profile_model = api.inherit('UserProfile', user_model, {
    'is_verified': fields.Boolean(description='Email verification status'),
    'is_active': fields.Boolean(description='Account status')
})

user_detail_model = api.inherit('UserDetail', user_profile_model, {
    'auth_method': fields.String(description='Authentication method'),
    'last_login_at': fields.DateTime(description='Last login timestamp'),
    'created_at': fields.DateTime(description='Account creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

user_list_model = api.model('UserList', {
    'data': fields.List(fields.Nested(user_model))
})

# Request Models
create_user_model = api.model('CreateUser', {
    'email': fields.String(required=True, description='User email address'),
    'username': fields.String(required=True, description='Username (3-50 characters)', 
                            min_length=3, max_length=50),
    'password': fields.String(required=True, description='Password (min 8 characters)', 
                            min_length=8)
})

update_user_model = api.model('UpdateUser', {
    'email': fields.String(description='New email address'),
    'username': fields.String(description='New username', 
                            min_length=3, max_length=50)
})

update_system_model = api.model('UpdateUserSystem', {
    'auth_method': fields.String(description='Authentication method'),
    'is_active': fields.Boolean(description='Account status'),
    'is_verified': fields.Boolean(description='Verification status'),
    'last_login_at': fields.DateTime(description='Last login timestamp')
})

update_password_model = api.model('UpdatePassword', {
    'current_password': fields.String(required=True, min_length=8),
    'new_password': fields.String(required=True, min_length=8)
})

@api.route('/')
class UserRoot(Resource):
    @staticmethod
    @api.doc('list_users')
    @api.marshal_with(user_list_model)
    @inject
    def get(user_service: IUserService = Provide[Container.user_service]):
        """Get all users"""
        users = user_service.get_all_users()
        return {'data': users}

@api.route('/create')
class CreateUser(Resource):
    @staticmethod
    @api.doc('create_user')
    @api.expect(create_user_model)
    @api.marshal_with(user_model, code=201)
    @api.response(409, 'User already exists')
    @inject
    def post(user_service: IUserService = Provide[Container.user_service]):
        """Create a new user"""
        try:
            dto = CreateUserDTO(**api.payload)
            return user_service.create_user(dto), 201
        except ValueError as e:
            api.abort(409, str(e))

@api.route('/<int:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class User(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    @inject
    def get(self, user_id: int, user_service: IUserService = Provide[Container.user_service]):
        """Get user details"""
        user = user_service.get_user_by_id(user_id)
        if not user:
            api.abort(404, "User not found")
        return user

    @api.doc('update_user')
    @api.expect(update_user_model)
    @api.marshal_with(user_model)
    @inject
    def put(self, user_id: int, user_service: IUserService = Provide[Container.user_service]):
        """Update user information"""
        try:
            dto = UpdateUserDTO(**api.payload)
            return user_service.update_user(user_id, dto)
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_user')
    @api.response(204, 'User deleted')
    @inject
    def delete(self, user_id: int, user_service: IUserService = Provide[Container.user_service]):
        """Delete user"""
        try:
            user_service.delete_user(user_id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))

@api.route('/<int:user_id>/system')
@api.param('user_id', 'The user identifier')
class UserSystem(Resource):
    @api.doc('get_user detail')
    @api.marshal_with(user_detail_model)
    @inject
    def get(self, user_id: int, user_service: IUserService = Provide[Container.user_service]):
        """Get user details"""
        user = user_service.get_user_detail(user_id)
        if not user:
            api.abort(404, "User not found")
        return user

    @api.doc('update_user_system')
    @api.expect(update_system_model)
    @api.marshal_with(user_detail_model)
    @inject
    def put(self, user_id: int, user_service: IUserService = Provide[Container.user_service]):
        """Update user system settings"""
        try:
            dto = UpdateUserSystemDTO(**api.payload)
            return user_service.update_user_system(user_id, dto)
        except ValueError as e:
            api.abort(404, str(e))

@api.route('/<int:user_id>/password')
@api.param('user_id', 'The user identifier')
class UserPassword(Resource):
    @api.doc('update_password')
    @api.expect(update_password_model)
    @api.response(204, 'Password updated')
    @inject
    def put(self, user_id: int, user_service: IUserService = Provide[Container.user_service]):
        """Update user password"""
        try:
            dto = UpdatePasswordDTO(**api.payload)
            user_service.update_password(user_id, dto)
            return '', 204
        except ValueError as e:
            api.abort(400, str(e))

# Error handlers
@api.errorhandler(ValueError)
def handle_validation_error(error):
    return {'message': str(error)}, 400

@api.errorhandler(Exception)
def handle_general_error(error):
    return {'message': 'An unexpected error occurred'}, 500