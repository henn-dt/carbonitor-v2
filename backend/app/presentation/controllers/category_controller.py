from datetime import datetime

from app.config import Config
from app.core.application.dtos.category.category_dto import (
    CategoryDTO, CategoryResponseDTO, CategoryUpdateDTO)
from app.core.application.services.icategory_service import ICategoryService
from app.infrastructure.container import Container
from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from flask_restx import Api, Namespace, Resource, fields, marshal

category_blueprint = Blueprint("category", __name__)
api = Api(
    category_blueprint,
    version="1.0",
    title="Category API",
    description="API for managing categories for all entities",
    doc="/docs/categories",
    default_endpoint=None,
    prefix="/categories",
)


category_ns = Namespace("categories", description="Category operations", path="/")
api.add_namespace(category_ns)


# Custom DateTime field (reusing your existing definition)
class CustomDateTime(fields.Raw):
    def format(self, value):
        if value:
            if isinstance(value, str):
                return value
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return None


# API Models
category_input_model = category_ns.model(
    "CategoryInput",
    {
        "name": fields.String(required=True, description="Category name"),
        "type": fields.String(required=True, description="Category type"),
        "status": fields.String(required=True, description="Category status"),
        "description": fields.String(description="Category description/tooltip"),
        "property_schema": fields.Raw(
            description="JSON schema for category properties"
        ),
        "user_id_created": fields.Integer(
            description="ID of user who created the category"
        ),
        "user_id_updated": fields.Integer(
            description="ID of user who last updated the category"
        ),
    },
)



category_output_model = category_ns.inherit(
    "Category",
    category_input_model,
    {
        "id": fields.Integer(readonly=True, description="Category identifier")
    },
)


@category_ns.route("/")
class CategoryList(Resource):
    @inject
    @category_ns.doc("list_categories")
    @category_ns.marshal_list_with(category_output_model)
    def get(
        self, category_service: ICategoryService = Provide[Container.category_service]
    ):
        """List all categories"""
        categories = category_service.get_all_categories()
        return [category_dto for category_dto in categories]

    @inject
    @category_ns.doc("create_category")
    @category_ns.expect(category_input_model)
    @category_ns.marshal_with(category_output_model, code=201)
    def post(
        self, category_service: ICategoryService = Provide[Container.category_service]
    ):
        """Create a new category"""
        data: dict = category_ns.payload
        keys_to_ignore_list = ["date_created", "date_updated"]
        ignored_values_list = [
            data.pop(key, f"key {key} not present") for key in keys_to_ignore_list
        ]
        category = CategoryDTO(**data)
        category.status = "active"
        created_category: CategoryResponseDTO = (
            category_service.create_category_from_dto(category)
        )
        print(created_category)
        return created_category.model_dump(), 201


@category_ns.route("/<int:id>")
@category_ns.response(404, "Category not found")
@category_ns.param("id", "The category identifier")
class CategoryItem(Resource):
    @inject
    @category_ns.doc("get_category")
    @category_ns.marshal_with(category_output_model)
    def get(
        self,
        id,
        category_service: ICategoryService = Provide[Container.category_service],
    ):
        """Get a specific category by ID"""
        category = category_service.get_category_by_id(id)
        if category:
            return category
        category_ns.abort(404, f"Category {id} not found")

    @inject
    @category_ns.doc("update_category")
    @category_ns.expect(category_input_model)
    @category_ns.marshal_with(category_output_model)
    def put(
        self,
        id,
        category_service: ICategoryService = Provide[Container.category_service],
    ):
        """Update a category"""
        data: dict = category_ns.payload
        data["id"] = id
        keys_to_ignore_list = ["date_created", "date_updated"]
        ignored_values_list = [
            data.pop(key, f"key {key} not present") for key in keys_to_ignore_list
        ]

        existing_category = category_service.get_category_by_id(id)
        if not existing_category:
            category_ns.abort(404, f"Category {id} not found")

        category = CategoryUpdateDTO(**data)
        updated_category = category_service.update_category_from_dto(category)
        print(updated_category)
        return updated_category

    @inject
    @category_ns.doc("delete_category")
    @category_ns.response(204, "Category deleted")
    def delete(
        self,
        id,
        category_service: ICategoryService = Provide[Container.category_service],
    ):
        """Delete a category"""
        success = category_service.delete_category(id)
        if success:
            return True, 204
        category_ns.abort(404, f"Category {id} not found")
