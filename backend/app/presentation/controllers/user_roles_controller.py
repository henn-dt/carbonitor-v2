# app/presentation/controllers/user_roles_controller.py
from flask import Blueprint
from flask_restx import Api, Namespace, Resource, fields
from dependency_injector.wiring import inject, Provide
from app.infrastructure.container import Container
from app.core.application.services.iuser_roles_service import IUserRolesService
from app.core.application.dtos.user_roles.user_roles_dto import UserRolesRoleDTO, UserRolesUserDTO
from app.core.application.dtos.user_roles.create_user_roles_dto import AssignRoleToUserDTO, AssignRolesToUserDTO, AssignUserToRoleDTO, AssignUsersToRoleDTO

# Create Blueprint
user_roles_blueprint = Blueprint('user_roles_api', __name__)

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
    user_roles_blueprint,
    version='1.0',
    title='User Roles Management API',
    description='API endpoints for managing user roles',
    doc='/docs/user-roles',
    authorizations=authorizations,
    security='Bearer',
    default_endpoint=None,
    prefix='/user-roles'
)

# Model Definitions
user_dto_model = api.model('UserDTO', {
    'id': fields.Integer(description='User identifier', required=False),
    'username': fields.String(description='Username', required=False),
    'email': fields.String(description='User email', required=False)
})

role_dto_model = api.model('RoleDTO', {
    'id': fields.Integer(description='Role identifier', required=False),
    'role_name': fields.String(description='Role name', required=False),
    'role_permissions': fields.List(fields.String, description='Role permissions', required=False)
})

user_roles_response_model = api.model('UserRolesResponse', {
    'user': fields.Nested(user_dto_model),
    'roles': fields.List(fields.Nested(role_dto_model), required=False),
    'permissions': fields.List(fields.String, description='Aggregated permissions', required=False)
})

role_users_response_model = api.model('RoleUsersResponse', {
    'role': fields.Nested(role_dto_model),
    'users': fields.List(fields.Nested(user_dto_model), required=False)
})

# Request Models
assign_role_to_user_model = api.model('AssignRoleToUser', {
    'user': fields.Nested(user_dto_model, required=True),
    'role': fields.Nested(role_dto_model, required=True)
})

assign_roles_to_user_model = api.model('AssignRolesToUser', {
    'user': fields.Nested(user_dto_model, required=True),
    'roles': fields.List(fields.Nested(role_dto_model), required=True)
})

assign_user_to_role_model = api.model('AssignUserToRole', {
    'role': fields.Nested(role_dto_model, required=True),
    'user': fields.Nested(user_dto_model, required=True)
})

assign_users_to_role_model = api.model('AssignUsersToRole', {
    'role': fields.Nested(role_dto_model, required=True),
    'users': fields.List(fields.Nested(user_dto_model), required=True)
})

# Controllers
@api.route('/user/<int:user_id>/roles')
@api.param('user_id', 'The user identifier')
class UserRoles(Resource):
    @api.doc('get_user_roles')
    @api.marshal_with(user_roles_response_model)
    @inject
    def get(self, user_id: int, user_roles_service: IUserRolesService = Provide[Container.user_roles_service]):
        """Get all roles and aggregated permissions for a user"""
        try:
            user_dto = UserRolesUserDTO(id=user_id)
            return user_roles_service.get_roles_by_user(user_dto)
        except ValueError as e:
            api.abort(404, str(e))

@api.route('/role/<int:role_id>/users')
@api.param('role_id', 'The role identifier')
class RoleUsers(Resource):
    @api.doc('get_role_users')
    @api.marshal_with(role_users_response_model)
    @inject
    def get(self, role_id: int, user_roles_service: IUserRolesService = Provide[Container.user_roles_service]):
        """Get all users assigned to a role"""
        try:
            role_dto = UserRolesRoleDTO(id=role_id)
            return user_roles_service.get_users_by_role(role_dto)
        except ValueError as e:
            api.abort(404, str(e))

@api.route('/assign/role-to-user')
class AssignRoleToUser(Resource):
    @api.doc('assign_role_to_user')
    @api.expect(assign_role_to_user_model)
    @api.marshal_with(user_roles_response_model)
    @inject
    def post(self, user_roles_service: IUserRolesService = Provide[Container.user_roles_service]):
        """Assign a role to a user"""
        try:
            payload = api.payload
            user_dto = UserRolesUserDTO(**payload['user'])
            role_dto = UserRolesRoleDTO(**payload['role'])
            dto = AssignRoleToUserDTO(user=user_dto, role=role_dto)
            return user_roles_service.assign_role_to_user(dto)
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/assign/roles-to-user')
class AssignRolesToUser(Resource):
    @api.doc('assign_roles_to_user')
    @api.expect(assign_roles_to_user_model)
    @api.marshal_with(user_roles_response_model)
    @inject
    def post(self, user_roles_service: IUserRolesService = Provide[Container.user_roles_service]):
        """Assign multiple roles to a user"""
        try:
            payload = api.payload
            user_dto = UserRolesUserDTO(**payload['user'])
            roles_dto = [UserRolesRoleDTO(**role) for role in payload['roles']]
            dto = AssignRolesToUserDTO(user=user_dto, roles=roles_dto)
            return user_roles_service.assign_roles_to_user(dto)
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/assign/user-to-role')
class AssignUserToRole(Resource):
    @api.doc('assign_user_to_role')
    @api.expect(assign_user_to_role_model)
    @api.marshal_with(role_users_response_model)
    @inject
    def post(self, user_roles_service: IUserRolesService = Provide[Container.user_roles_service]):
        """Assign a user to a role"""
        try:
            payload = api.payload
            user_dto = UserRolesUserDTO(**payload['user'])
            role_dto = UserRolesRoleDTO(**payload['role'])
            dto = AssignUserToRoleDTO(user=user_dto, role=role_dto)
            return user_roles_service.assign_user_to_role(dto)
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/assign/users-to-role')
class AssignUsersToRole(Resource):
    @api.doc('assign_users_to_role')
    @api.expect(assign_users_to_role_model)
    @api.marshal_with(role_users_response_model)
    @inject
    def post(self, user_roles_service: IUserRolesService = Provide[Container.user_roles_service]):
        """Assign multiple users to a role"""
        try:
            payload = api.payload
            role_dto = UserRolesRoleDTO(**payload['role'])
            users_dto = [UserRolesUserDTO(**user) for user in payload['users']]
            dto = AssignUsersToRoleDTO(role=role_dto, users=users_dto)
            return user_roles_service.assign_users_to_role(dto)
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/check/user/<int:user_id>/has-role')
@api.param('user_id', 'The user identifier')
class CheckUserHasRole(Resource):
    @api.doc('check_user_has_role')
    @inject
    def get(self, user_id: int, user_roles_service: IUserRolesService = Provide[Container.user_roles_service]):
        """Check if a user has any role"""
        return {'has_role': user_roles_service.has_role(user_id)}

@api.route('/check/role/<int:role_id>/has-user')
@api.param('role_id', 'The role identifier')
class CheckRoleHasUser(Resource):
    @api.doc('check_role_has_user')
    @inject
    def get(self, role_id: int, user_roles_service: IUserRolesService = Provide[Container.user_roles_service]):
        """Check if a role has any user"""
        return {'has_user': user_roles_service.has_user(role_id)}

# Error handlers
@api.errorhandler(ValueError)
def handle_validation_error(error: ValueError):
    return { 'message': str(error), 'error_type': 'Validation Error'}, 400

@api.errorhandler(Exception)
def handle_general_error(error: Exception):
    return {'message': 'An unexpected error occurred', 'error': str(error)}, 500