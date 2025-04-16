from flask import Blueprint
from flask_restx import Api, Namespace, Resource, fields
from dependency_injector.wiring import inject, Provide
from app.infrastructure.container import Container
from app.core.application.services.irole_service import IRoleService
from app.core.application.dtos.role.create_role_dto import CreateRoleDTO
from app.core.application.dtos.role.update_role_dto import UpdateRoleDTO

# Create Blueprint
role_blueprint = Blueprint('role_api', __name__)

# Create API instance
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Enter your bearer token in the format: Bearer <token>'
    }
}

# Create API instance
api = Api(
    role_blueprint,
    version='1.0',
    title='Role Management API',
    description='API endpoints for role management',
    doc='/docs/roles',
    authorizations=authorizations,
    security='Bearer',
    default_endpoint=None,
    prefix='/roles'
)

# Model Definitions
role_model = api.model('Role', {
    'id': fields.Integer(description='Role identifier'),
    'name': fields.String(required=True, description='Role name'),
    'permissions': fields.List(fields.String, description='List of permissions', default=[])
})

role_detail_model = api.inherit('RoleDetail', role_model, {
    'description': fields.String(description='Role description'),
    'created_at': fields.DateTime(description='Role creation timestamp'),
    'updated_at': fields.DateTime(description='Role last update timestamp')
})

role_list_model = api.model('RoleList', {
    'data': fields.List(fields.Nested(role_model))
})

# Request Models
create_role_model = api.model('CreateRole', {
    'name': fields.String(
        required=True,
        description='Role name',
        min_length=1,
        max_length=50,
        example='admin'
    ),
    'description': fields.String(
        description='Role description',
        max_length=255,
        example='Administrator role with full access'
    ),
    'permissions': fields.List(
        fields.String,
        description='List of permissions',
        example=['read', 'write', 'delete']
    )
})

update_role_model = api.model('UpdateRole', {
    'name': fields.String(
        description='New role name',
        min_length=1,
        max_length=50,
        example='super_admin'
    ),
    'description': fields.String(
        description='New role description',
        max_length=255,
        example='Updated administrator role'
    ),
    'permissions': fields.List(
        fields.String,
        description='Updated list of permissions',
        example=['read', 'write', 'delete', 'manage_users']
    )
})

permissions_model = api.model('AvailablePermissions', {
    'permissions': fields.List(fields.String, description='List of available permissions')
})

@api.route('/')
class RoleRoot(Resource):
    @staticmethod
    @api.doc('list_roles')
    @api.marshal_with(role_list_model)
    @inject
    def get(role_service: IRoleService = Provide[Container.role_service]):
        """Get all roles"""
        roles = role_service.get_all_roles()
        return {'data': roles}

@api.route('/create')
class CreateRole(Resource):
    @staticmethod
    @api.doc('create_role')
    @api.expect(create_role_model)
    @api.marshal_with(role_detail_model, code=201)
    @api.response(409, 'Role already exists')
    @inject
    def post(role_service: IRoleService = Provide[Container.role_service]):
        """Create a new role"""
        try:
            dto = CreateRoleDTO(**api.payload)
            return role_service.create_role(dto), 201
        except ValueError as e:
            api.abort(409, str(e))

@api.route('/<int:role_id>')
@api.param('role_id', 'The role identifier')
@api.response(404, 'Role not found')
class Role(Resource):
    @api.doc('get_role')
    @api.marshal_with(role_detail_model)
    @inject
    def get(self, role_id: int, role_service: IRoleService = Provide[Container.role_service]):
        """Get role details"""
        role = role_service.get_role_details(role_id)
        if not role:
            api.abort(404, "Role not found")
        return role

    @api.doc('update_role')
    @api.expect(update_role_model)
    @api.marshal_with(role_detail_model)
    @inject
    def put(self, role_id: int, role_service: IRoleService = Provide[Container.role_service]):
        """Update role information"""
        try:
            dto = UpdateRoleDTO(**api.payload)
            updated_role = role_service.update_role(role_id, dto)
            if not updated_role:
                api.abort(404, "Role not found")
            return updated_role
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_role')
    @api.response(204, 'Role deleted')
    @inject
    def delete(self, role_id: int, role_service: IRoleService = Provide[Container.role_service]):
        """Delete role"""
        try:
            role_service.delete_role(role_id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))

@api.route('/<string:role_name>')
@api.param('role_name', 'The given role name')
@api.response(404, 'Role not found')
class RoleByName(Resource):
    @api.doc('get_role_by_name')
    @api.marshal_with(role_detail_model)
    @inject
    def get(self, role_name: str, role_service: IRoleService = Provide[Container.role_service]):
        """Get role details"""
        role = role_service.get_role_by_name(role_name)
        if not role:
            api.abort(404, "Role not found")
        return role

    @api.doc('update_role')
    @api.expect(update_role_model)
    @api.marshal_with(role_detail_model)
    @inject
    def put(self, role_name: str, role_service: IRoleService = Provide[Container.role_service]):
        """Update role information"""
        try:
            dto = UpdateRoleDTO(**api.payload)
            updated_role = role_service.update_role(role_name, dto)
            if not updated_role:
                api.abort(404, "Role not found")
            return updated_role
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_role')
    @api.response(204, 'Role deleted')
    @inject
    def delete(self, role_name: str, role_service: IRoleService = Provide[Container.role_service]):
        """Delete role"""
        try:
            role_service.delete_role(role_name)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))

@api.route('/permissions')
class AvailablePermissions(Resource):
    @staticmethod
    @api.doc('get_available_permissions')
    @api.marshal_with(permissions_model)
    @inject
    def get(role_service: IRoleService = Provide[Container.role_service]):
        """Get list of available permissions"""
        permissions = role_service.get_available_permissions()
        return {'permissions': list(permissions)}

# Error handlers
@api.errorhandler(ValueError)
def handle_validation_error(error):
    return {'message': str(error)}, 400

@api.errorhandler(Exception)
def handle_general_error(error):
    return {'message': 'An unexpected error occurred'}, 500