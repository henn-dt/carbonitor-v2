from datetime import datetime

from app.config import Config

from app.infrastructure.container import Container
from app.core.application.dtos.filter_element.filter_element_dto import FilterElementCreateDTO, FilterElementResponseDTO, FilterElementUpdateDTO
from app.core.application.services.ifilter_element_service import IFilterElementService
from app.core.application.dtos.filter_element.filter_element_dto import FilterElementCreateDTO, FilterElementResponseDTO
from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from flask_restx import Api, Namespace, Resource, fields, marshal

filter_element_blueprint = Blueprint("filters", __name__)
api = Api(
    filter_element_blueprint,
    version="1.0",
    title="Filters API",
    description="API for managing element filters for all desktop applications",
    doc="/docs/filters",
    default_endpoint=None,
    prefix="/filters",
)


filter_element_ns = Namespace("filters", description="Filters operations", path="/")
api.add_namespace(filter_element_ns)


# Custom DateTime field (reusing your existing definition)
class CustomDateTime(fields.Raw):
    def format(self, value):
        if value:
            if isinstance(value, str):
                return value
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return None


# API Models
filter_element_input_model = filter_element_ns.model(
    "FilterElementInput",
    {
        "name": fields.String(required=True, description="filter name"),
        "type": fields.String(required=True, description="filter type"),
        "source": fields.String(required=True, description="filter software source"),
        "source_version": fields.String(required=True, description="Software version"),
        "status": fields.String(required=True, description="filter status"),
        "filter": fields.Raw(
            description="JSON schema for filter properties"
        ),
        "user_id_created": fields.Integer(
            description="ID of user who created the filter"
        ),
        "user_id_updated": fields.Integer(
            description="ID of user who last updated the filter"
        ),
    },
)



filter_element_output_model = filter_element_ns.inherit(
    "FilterElement",
    filter_element_input_model,
    {
        "id": fields.Integer(readonly=True, description="filter identifier")
    },
)


@filter_element_ns.route("/")
class FilterElementList(Resource):
    @inject
    @filter_element_ns.doc("list_filters")
    @filter_element_ns.marshal_list_with(filter_element_output_model)
    def get(
        self, filter_element_service: IFilterElementService = Provide[Container.filter_element_service]
    ):
        """List all model filters"""
        filters = filter_element_service.get_all_filter_elements()
        return [filter_dto for filter_dto in filters]

    @inject
    @filter_element_ns.doc("create_filter")
    @filter_element_ns.expect(filter_element_input_model)
    @filter_element_ns.marshal_with(filter_element_output_model, code=201)
    def post(
        self, filter_element_service: IFilterElementService = Provide[Container.filter_element_service]
    ):
        """Create a new filter"""
        data: dict = filter_element_ns.payload
        keys_to_ignore_list = ["date_created", "date_updated"]
        ignored_values_list = [
            data.pop(key, f"key {key} not present") for key in keys_to_ignore_list
        ]
        filter_element = FilterElementCreateDTO(**data)
        filter_element.status = "active"
        created_filter_element: FilterElementResponseDTO = (
            filter_element_service.create_filter_element_from_dto(filter_element)
        )
        print(created_filter_element)
        return created_filter_element.model_dump(), 201


@filter_element_ns.route("/<int:id>")
@filter_element_ns.response(404, "Model filter not found")
@filter_element_ns.param("id", "The model filter identifier")
class FilterElementItem(Resource):
    @inject
    @filter_element_ns.doc("get_filter_element")
    @filter_element_ns.marshal_with(filter_element_output_model)
    def get(
        self,
        id,
        filter_element_service: IFilterElementService = Provide[Container.filter_element_service],
    ):
        """Get a specific model filter by ID"""
        filter_element = filter_element_service.get_filter_element_by_id(id)
        if filter_element:
            return filter_element
        filter_element_ns.abort(404, f"Model filter {id} not found")

    @inject
    @filter_element_ns.doc("update_filter_element")
    @filter_element_ns.expect(filter_element_input_model)
    @filter_element_ns.marshal_with(filter_element_output_model)
    def put(
        self,
        id,
        filter_element_service: IFilterElementService = Provide[Container.filter_element_service],
    ):
        """Update a model filter"""
        data: dict = filter_element_ns.payload
        data["id"] = id
        keys_to_ignore_list = ["date_created", "date_updated"]
        ignored_values_list = [
            data.pop(key, f"key {key} not present") for key in keys_to_ignore_list
        ]
        existing_filter_element = filter_element_service.get_filter_element_by_id(id)
        if not existing_filter_element:
            filter_element_ns.abort(404, f"Model filter {id} not found")
        filter_element = FilterElementUpdateDTO(**data)
        updated_filter_element = filter_element_service.update_filter_elements_from_dto(filter_element)
        print(updated_filter_element)
        return updated_filter_element

    @inject
    @filter_element_ns.doc("delete_filter_element")
    @filter_element_ns.response(204, "Model filter deleted")
    def delete(
        self,
        id,
        filter_element_service: IFilterElementService = Provide[Container.filter_element_service],
    ):
        """Delete a model filter"""
        success = filter_element_service.delete_filter(id)
        if success:
            return True, 204
        filter_element_ns.abort(404, f"Model filter {id} not found")
