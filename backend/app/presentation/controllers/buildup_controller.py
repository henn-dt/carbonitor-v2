from datetime import datetime

from app.config import Config
from app.core.application.dtos.buildup.buildup_dto import (BuildupCreate_DTO, BuildupResponse_DTO, BuildupUpdate_DTO, MappedBuildup_DTO)
from app.core.application.services.ibuildup_service import IBuildupService
from app.infrastructure.container import Container
from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from flask_restx import Api, Namespace, Resource, fields, marshal

buildup_blueprint = Blueprint('buildup', __name__)
api = Api(
    buildup_blueprint,
    version='1.0',
    title='buildup API',
    description='API for managing EPD buildups',
    doc='/docs/buildups',
    default_endpoint=None,
    prefix='/buildups'
)


buildup_ns = Namespace('buildups', description='buildup operations', path='/')
api.add_namespace(buildup_ns)

# Custom DateTime field to handle your format
class CustomDateTime(fields.Raw):
    def format(self, value):
        if value:
            if isinstance(value, str):
                return value
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return None

# API Models
buildup_input_model = buildup_ns.model('buildupInput', {
    'status': fields.String(required=True, description='buildup status'),
    'user_created': fields.String(description='User who created the buildup'),
    'user_updated': fields.String(description='User who last updated the buildup'),
    'name': fields.String(required=True, description='Buildup name'),
    'description': fields.String(required=False, description='Buildup description'),
    'unit': fields.String(required=False, description='Buildup reference unit'),
    'comment': fields.String(required=False, description='Buildup comment'),
    'classification': fields.Raw(required=False, description='Buildup classification dictionary'),
    'quantity': fields.Float(required=False, description='Buildup reference quantity'),
    'meta_data': fields.Raw(required=False, description='Buildup additional information'),
    'products': fields.Raw(required=False, description='Buildup products dictionary'),
    'results': fields.Raw(required=False, description='Buildup products dictionary'),

})

buildup_output_model = buildup_ns.inherit('buildup', buildup_input_model, {
    'id': fields.Integer(readonly=True, description='buildup identifier'),
    'date_created': CustomDateTime(readonly=True, description='Creation date'),
    'date_updated': CustomDateTime(readonly=True, description='Last update date'),
})


@buildup_ns.route('/')
class buildupList(Resource):
    @inject
    @buildup_ns.doc('list_buildups')
    @buildup_ns.marshal_list_with(buildup_output_model)
    def get(self, buildup_service: IBuildupService = Provide[Container.buildup_service]):
        """List all buildups"""
        buildups = buildup_service.get_all_buildups()
        return [buildup_dto for buildup_dto in buildups]

    @inject
    @buildup_ns.doc('create_buildup')
    @buildup_ns.expect(buildup_input_model)
    @buildup_ns.marshal_with(buildup_output_model, code=201)
    def post(self, buildup_service: IBuildupService = Provide[Container.buildup_service]):
        """Create a new buildup"""
        data : dict = buildup_ns.payload
        keys_to_ignore_list = ['date_created', 'date_updated']
        ignored_values_list = [data.pop(key, f"key {key} not present") for key in keys_to_ignore_list ]
        buildup = BuildupCreate_DTO(**(data))
        
        buildup.date_created = datetime.utcnow()
        buildup.status = 'active'
        
        created_buildup : BuildupResponse_DTO = buildup_service.create_buildup(buildup)
        return created_buildup.model_dump(), 201

@buildup_ns.route('/<int:id>')
@buildup_ns.param('id', 'The buildup identifier')
class buildupItem(Resource):
    @inject
    @buildup_ns.doc('get_buildup')
    @buildup_ns.marshal_with(buildup_output_model)
    def get(self, id: int, buildup_service: IBuildupService = Provide[Container.buildup_service]):
        """Get a buildup by ID"""
        buildup : BuildupResponse_DTO = buildup_service.get_buildup_by_id(id)
        if not buildup:
            buildup_ns.abort(404, "buildup not found")
        return buildup.model_dump()

    @inject
    @buildup_ns.doc('update_buildup')
    @buildup_ns.expect(buildup_input_model)
    @buildup_ns.marshal_with(buildup_output_model)
    def put(self, id: int, buildup_service: IBuildupService = Provide[Container.buildup_service]):
        """Update a buildup"""
        data = buildup_ns.payload
        keys_to_ignore_list = ['date_created', 'date_updated']
        ignored_values_list = [data.pop(key, f"key {key} not present") for key in keys_to_ignore_list ]
        buildup = BuildupUpdate_DTO(**(data))
        
        updated_buildup : BuildupResponse_DTO = buildup_service.update_buildup(id, buildup)
        if not updated_buildup:
            buildup_ns.abort(404, "buildup not found")
        return updated_buildup.model_dump()

    @inject
    @buildup_ns.doc('delete_buildup')
    @buildup_ns.response(204, 'buildup deleted')
    def delete(self, id: int, buildup_service: IBuildupService = Provide[Container.buildup_service]):
        """Delete a buildup"""
        result = buildup_service.delete_buildup(id)
        if not result:
            buildup_ns.abort(404, "buildup not found")
        return '', 204

@buildup_ns.route('/name/<name>')
@buildup_ns.param('name', 'The buildup name')
class buildupItem(Resource):
    @inject
    @buildup_ns.doc('get_buildup')
    @buildup_ns.marshal_with(buildup_output_model)
    def get(self, name: int, buildup_service: IBuildupService = Provide[Container.buildup_service]):
        """Get a buildup by ID"""
        buildup : BuildupResponse_DTO = buildup_service.get_buildup_by_name(name)
        if not buildup:
            buildup_ns.abort(404, "buildup not found")
        return buildup.model_dump()


"""
get all buildups
get all buildups with buildups reference
get all buildups with buildup snapshot
get one buildup
    check that buildups exists if they are referenced
create buildup
    check that all buildups are either references or snapshots
delete buildup
update buildup
    check that all buildups are either references or snapshots

"""