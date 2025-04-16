from datetime import datetime

from app.config import Config

from app.infrastructure.container import Container
from app.core.application.dtos.filter_mapping.filter_mapping_dto import FilterMappingCreateDTO, FilterMappingResponseDTO, FilterMappingUpdateDTO
from app.core.application.services.ifilter_mapping_service import IFilterMappingService
from app.core.application.dtos.filter_mapping.filter_mapping_dto import FilterMappingCreateDTO, FilterMappingResponseDTO
from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from flask_restx import Api, Namespace, Resource, fields, marshal

filter_mapping_blueprint = Blueprint("mappings", __name__)
api = Api(
    filter_mapping_blueprint,
    version="1.0",
    title="mappings API",
    description="API for managing filter mappings for all desktop applications",
    doc="/docs/mappings",
    default_endpoint=None,
    prefix="/mappings",
)


filter_mapping_ns = Namespace("mappings", description="mappings operations", path="/")
api.add_namespace(filter_mapping_ns)


# Custom DateTime field (reusing your existing definition)
class CustomDateTime(fields.Raw):
    def format(self, value):
        if value:
            if isinstance(value, str):
                return value
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return None


# API Models
filter_mapping_input_model = filter_mapping_ns.model(
    "FilterMappingInput",
    {
        "name": fields.String(required=True, description="mapping name"),
        "type": fields.String(required=True, description="mapping type"),
        "source": fields.String(required=True, description="mapping software source"),
        "source_version": fields.String(required=True, description="Software version"),
        "status": fields.String(required=True, description="mapping status"),
        "mapping": fields.Raw(
            description="JSON schema for mapping elements"
        ),
        "user_id_created": fields.Integer(
            description="ID of user who created the filter"
        ),
        "user_id_updated": fields.Integer(
            description="ID of user who last updated the filter"
        ),
    },
)



filter_mapping_output_model = filter_mapping_ns.inherit(
    "FilterMapping",
    filter_mapping_input_model,
    {
        "id": fields.Integer(readonly=True, description="filter identifier")
    },
)


@filter_mapping_ns.route("/")
class FilterMappingList(Resource):
    @inject
    @filter_mapping_ns.doc("list_mappings")
    @filter_mapping_ns.marshal_list_with(filter_mapping_output_model)
    def get(
        self, filter_mapping_service: IFilterMappingService = Provide[Container.filter_mapping_service]
    ):
        """List all model mappings"""
        mappings = filter_mapping_service.get_all_filter_mappings()
        return [filter_dto for filter_dto in mappings]

    @inject
    @filter_mapping_ns.doc("create_mapping")
    @filter_mapping_ns.expect(filter_mapping_input_model)
    @filter_mapping_ns.marshal_with(filter_mapping_output_model, code=201)
    def post(
        self, filter_mapping_service: IFilterMappingService = Provide[Container.filter_mapping_service]
    ):
        """Create a new filter mapping"""
        data: dict = filter_mapping_ns.payload
        keys_to_ignore_list = ["date_created", "date_updated"]
        ignored_values_list = [
            data.pop(key, f"key {key} not present") for key in keys_to_ignore_list
        ]
        filter_mapping = FilterMappingCreateDTO(**data)
        filter_mapping.status = "active"
        created_filter_mapping: FilterMappingResponseDTO = (
            filter_mapping_service.create_filter_mapping_from_dto(filter_mapping)
        )
        print(created_filter_mapping)
        return created_filter_mapping.model_dump(), 201


@filter_mapping_ns.route("/<int:id>")
@filter_mapping_ns.response(404, "Filter Mapping not found")
@filter_mapping_ns.param("id", "The filter mapping identifier")
class FilterMappingItem(Resource):
    @inject
    @filter_mapping_ns.doc("get_filter_mapping")
    @filter_mapping_ns.marshal_with(filter_mapping_output_model)
    def get(
        self,
        id,
        filter_mapping_service: IFilterMappingService = Provide[Container.filter_mapping_service],
    ):
        """Get a specific filter mapping by ID"""
        filter_mapping = filter_mapping_service.get_filter_mapping_by_id(id)
        if filter_mapping:
            return filter_mapping
        filter_mapping_ns.abort(404, f"Mapping {id} not found")

    @inject
    @filter_mapping_ns.doc("update_filter_mapping")
    @filter_mapping_ns.expect(filter_mapping_input_model)
    @filter_mapping_ns.marshal_with(filter_mapping_output_model)
    def put(
        self,
        id,
        filter_mapping_service: IFilterMappingService = Provide[Container.filter_mapping_service],
    ):
        """Update a filter mapping"""
        data: dict = filter_mapping_ns.payload
        data["id"] = id
        keys_to_ignore_list = ["date_created", "date_updated"]
        ignored_values_list = [
            data.pop(key, f"key {key} not present") for key in keys_to_ignore_list
        ]
        existing_filter_mapping = filter_mapping_service.get_filter_mapping_by_id(id)
        if not existing_filter_mapping:
            filter_mapping_ns.abort(404, f"Model filter {id} not found")
        filter_mapping = FilterMappingUpdateDTO(**data)
        updated_filter_mapping = filter_mapping_service.update_filter_mappings_from_dto(filter_mapping)
        print(updated_filter_mapping)
        return updated_filter_mapping

    @inject
    @filter_mapping_ns.doc("delete_filter_mapping")
    @filter_mapping_ns.response(204, "Mapping deleted")
    def delete(
        self,
        id,
        filter_mapping_service: IFilterMappingService = Provide[Container.filter_mapping_service],
    ):
        """Delete a filter mapping"""
        success = filter_mapping_service.delete_filter_mapping(id)
        if success:
            return True, 204
        filter_mapping_ns.abort(404, f"Filter mapping {id} not found")
