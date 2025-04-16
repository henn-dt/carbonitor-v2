from datetime import datetime

from app.config import Config
from app.core.application.dtos.category.category_dto import (
    CategoryDTO, CategoryResponseDTO, CategoryUpdateDTO)
from app.core.application.dtos.category_association.category_association_dto import (
    CategoryAssociationDTO, CategoryAssociationResponseDTO)
from app.core.application.services.icategory_association_service import \
    ICategoryAssociationService
from app.core.application.services.icategory_service import ICategoryService
from app.infrastructure.container import Container
from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from flask_restx import Api, Namespace, Resource, fields, marshal

category_association_blueprint = Blueprint("category-association", __name__)
api = Api(
    category_association_blueprint,
    version="1.0",
    title="Category Association API",
    description="API for managing category association, entity-agnostic",
    doc="/docs/category-associations",
    default_endpoint=None,
    prefix="/category-association",
)


category_association_ns = Namespace("category-association", description="Category Association operations", path="/")
api.add_namespace(category_association_ns)


# Custom DateTime field (reusing your existing definition)
class CustomDateTime(fields.Raw):
    def format(self, value):
        if value:
            if isinstance(value, str):
                return value
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return None


# API Models

category_association_model = category_association_ns.model(
    "CategoryAssociationBase",
    {
        "category_id": fields.Integer(required=True, description="Category identifier"),
        "entity_id": fields.Integer(required=True, description="Entity identifier"),
        "entity_type": fields.String(required=True, description="Entity type"),
    },
)


category_association_input_model = category_association_ns.model(
    "CategoryAssociationInput",
    {
        "category_id": fields.Integer(required=True, description="Category identifier"),
        "entity_id": fields.Integer(required=True, description="Entity identifier"),
        "entity_type": fields.String(required=True, description="Entity type"),
        "values": fields.Raw(
            description="JSON schema for entity category property values"
        ),
        "user_id_created": fields.Integer(
            description="ID of user who created the category"
        ),
        "user_id_updated": fields.Integer(
            description="ID of user who last updated the category"
        ),
    },
)

category_association_output_model = category_association_ns.inherit(
    "CategoryAssociationOutput",
    category_association_input_model,
    {
        "id": fields.Integer(readonly=True, description="Category association identifier")
    },
)

entity_input_model = category_association_ns.model(
    "EntityInput",
    {
        "entity_id":fields.Integer(required=True, description="Category identifier"),
        "entity_type": fields.String(required=True, description="Entity type"),
        "values": fields.Raw(
            description="JSON schema for entity category property values"
        ),
        "user_id_created": fields.Integer(
            description="ID of user who created the category"
        ),
        "user_id_updated": fields.Integer(
            description="ID of user who last updated the category"
        ),
    }
)

entity_by_category_output_model = category_association_ns.model("GetEntityByCategoryOutput",
    {
        "ids" : fields.List(fields.Integer(description="Id of associated entitites"))
    },
)

category_input_model = category_association_ns.model("CategoryInput",
    {
        "category_id": fields.Integer(required=True, description="Category identifier"),
        "entity_type": fields.String(required=True, description="Entity type"),
        "user_id_created": fields.Integer(
            description="ID of user who created the category"
        ),
        "user_id_updated": fields.Integer(
            description="ID of user who last updated the category"
        ),
    },
)

category_output_model = category_association_ns.model("CategoryOutput",
    {
        "id": fields.Integer(readonly=True, description="Category identifier"),
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



category_data_model = category_association_ns.model(
    "CategoryData",
    {
        "category_id": fields.Integer(required=True, description="Category identifier"),
        "values": fields.Raw(description="Optional property values")
    }
)

entity_list_model = category_association_ns.model(
    "EntityListInput",
    {
        "entity_list": fields.List(fields.Integer, required=True, description="List of entity IDs"),
        "entity_type_list": fields.List(fields.String, required=True, description="List of entity types"),
        "category_id": fields.Integer(required=True, description="Category identifier"),
        "property_values_list": fields.List(fields.Raw, description="List of property values for each entity")
    }
)

categories_list_model = category_association_ns.model(
    "CategoriesListInput",
    {
        "category_data": fields.List(fields.Nested(category_data_model), required=True, 
                                    description="List of categories with values to assign")
    }
)


property_base_model = category_association_ns.model(
    "PropertyData",
    {
        "category_id": fields.Integer(required=True, description="Category identifier"),
        "property_id" : fields.Integer(required=True, description="Property identifier"),
    }
)


property_association_model = category_association_ns.inherit(
    "PropertyAssociationData",
    property_base_model,
    {
        "entity_id": fields.Integer(required=True, description="Entity identifier"),
        "entity_type": fields.String(required=True, description="Entity type"),
    }
)

property_value_input_model = category_association_ns.inherit(
    "PropertyValueInput",
    property_association_model,
    {
        "value": fields.Raw(required=True, description="Property value to set")
    }
)



@category_association_ns.route("/<int:id>")
@category_association_ns.response(404, "Category association not found")
@category_association_ns.param("id", "The category association identifier")
class CategoryItem(Resource):
    @inject
    @category_association_ns.doc("get_category_association")
    @category_association_ns.marshal_with(category_association_output_model)
    def get(
        self,
        id,
        category_association_service: ICategoryAssociationService = Provide[Container.category_association_service],
    ):
        """Get a specific category association by ID"""
        association = category_association_service.get_by_id(id)
        if association:
            return association
        category_association_ns.abort(404, f"Category Association {id} not found")



@category_association_ns.route("/type/<entity_type>/entity/<int:entity_id>/association")
@category_association_ns.response(404, "No association found")
@category_association_ns.param("entity_type", "The entity type")
@category_association_ns.param("entity_id", "The entity identifier")
class CategoryItem(Resource):
    @inject
    @category_association_ns.doc("get_association_properties")
    @category_association_ns.marshal_with(category_association_output_model)
    def get(
        self,
        entity_id,
        entity_type,
        category_association_service: ICategoryAssociationService = Provide[Container.category_association_service],
    ):
        """Get associations from entity type and id"""
        associations = category_association_service.get_by_entity_id_and_type(entity_id = entity_id, entity_type = entity_type)
        if associations:
            return associations
        category_association_ns.abort(404, f"No associations for entity {entity_id} ({entity_type}) found")

@category_association_ns.route("/type/<entity_type>/category/<int:category_id>/association")
@category_association_ns.response(404, "No association found")
@category_association_ns.param("entity_type", "The entity type")
@category_association_ns.param("category_id", "The category identifier")
class CategoryItem(Resource):
    @inject
    @category_association_ns.doc("get_association_properties")
    @category_association_ns.marshal_with(category_association_output_model)
    def get(
        self,
        category_id,
        entity_type,
        category_association_service: ICategoryAssociationService = Provide[Container.category_association_service],
    ):
        """Get associations from category type and id"""
        associations = category_association_service.get_by_category_id_and_type(category_id = category_id, entity_type = entity_type)
        if associations:
            return associations
        category_association_ns.abort(404, f"No associations for category {category_id} ({entity_type}) found")



@category_association_ns.route("/type/<entity_type>/entity/<int:entity_id>/categories")
@category_association_ns.response(404, "No associated category found")
@category_association_ns.param("entity_type", "The entity type")
@category_association_ns.param("entity_id", "The entity identifier")
class CategoryItem(Resource):
    @inject
    @category_association_ns.doc("get_associated_categories")
    @category_association_ns.marshal_with(category_output_model)
    def get(
        self,
        entity_id,
        entity_type,
        category_association_service: ICategoryAssociationService = Provide[Container.category_association_service],
    ):
        """Get associated categories from entity type and id"""
        categories = category_association_service.get_categories_by_entity(entity_id = entity_id, entity_type = entity_type)
        if categories:
            return categories
        category_association_ns.abort(404, f"No associated category with entity {entity_id} ({entity_type}) found")

@category_association_ns.route("/type/<entity_type>/category/<int:category_id>/entities")
@category_association_ns.response(404, "No associated entity found")
@category_association_ns.param("entity_type", "The entity type")
@category_association_ns.param("category_id", "The category identifier")
class EntityItem(Resource):
    @inject
    @category_association_ns.doc("get_associated_entities")
    @category_association_ns.marshal_with(entity_by_category_output_model)
    def get(
        self,
        entity_type,
        category_id,
        category_association_service: ICategoryAssociationService = Provide[Container.category_association_service],
    ):
        """Get associated entities from category type and id"""
        entities = category_association_service.get_entities_id_list_by_category(category_id = category_id, entity_type = entity_type)
        print(f"controller level entities: {entities}")
        if entities:
            return {"ids": entities}
        category_association_ns.abort(404, f"No associated entities found with Category {category_id} not found")


@category_association_ns.route("/")
class CategoryAssignment(Resource):
    @inject
    @category_association_ns.doc("assign_category_to_entity")
    @category_association_ns.expect(category_association_input_model, validate=True)
    @category_association_ns.marshal_with(category_association_output_model)
    @category_association_ns.response(201, "Category successfully assigned")
    @category_association_ns.response(400, "Invalid input")
    def post(
        self,
        category_association_service: ICategoryAssociationService = Provide[Container.category_association_service],
    ):
        """Assign a category to an entity"""
        data : dict = category_association_ns.payload
        property_values=data.get('values')
        
        result = category_association_service.assign_category_to_entity(
            entity_id=data.get('entity_id'),
            entity_type=data.get('entity_type'),
            category_id=data.get('category_id'),
            property_values=property_values
        )       
        if result:
            return result, 201       
        category_association_ns.abort(400, "Failed to assign category to entity")


    @inject
    @category_association_ns.doc("delete_association")
    @category_association_ns.expect(category_association_model, validate=True)
    @category_association_ns.response(204, "Association successfully deleted")
    @category_association_ns.response(404, "Association not found")
    def delete(
        self,
        category_association_service: ICategoryAssociationService = Provide[Container.category_association_service],
    ):

        data : dict = category_association_ns.payload
        entity_id = data.get('entity_id')
        entity_type = data.get('entity_type')
        category_id = data.get('category_id')

        """Delete an association between an entity and a category"""
        success = category_association_service.delete_association(
            entity_id=entity_id,
            entity_type=entity_type,
            category_id=category_id
        )       
        if success:
            return '', 204        
        category_association_ns.abort(404, "Association not found")



    

@category_association_ns.route("/bulk-entity-assign")
class BulkEntityAssignment(Resource):
    @inject
    @category_association_ns.doc("assign_category_to_entity_list")
    @category_association_ns.expect(entity_list_model, validate=True)
    @category_association_ns.marshal_list_with(category_association_output_model)
    @category_association_ns.response(201, "Categories successfully assigned to entities")
    @category_association_ns.response(400, "Invalid input")
    def post(
        self,
        category_association_service: ICategoryAssociationService = Provide[Container.category_association_service],
    ):
        """Assign a category to multiple entities"""
        data : dict = category_association_ns.payload
        entity_list = data.get('entity_list')
        entity_type_list = data.get('entity_type_list')
        category_id = data.get('category_id')
        property_values_list = data.get('property_values_list')
        
        result = category_association_service.assign_category_to_entity_list(
            entity_list=entity_list,
            entity_type_list=entity_type_list,
            category_id=category_id,
            property_values_list=property_values_list
        )
        
        if result:
            return result, 201
        
        category_association_ns.abort(400, "Failed to assign category to entities")


@category_association_ns.route("/type/<entity_type>/entity/<int:entity_id>/categories")
@category_association_ns.param("entity_type", "The entity type")
@category_association_ns.param("entity_id", "The entity identifier")
class MultiCategoryAssignment(Resource):
    @inject
    @category_association_ns.doc("assign_categories_to_entity")
    @category_association_ns.expect(categories_list_model, validate=True)
    @category_association_ns.marshal_list_with(category_association_output_model)
    @category_association_ns.response(201, "Categories successfully assigned")
    @category_association_ns.response(400, "Invalid input")
    def post(
        self,
        entity_id,
        entity_type,
        category_association_service: ICategoryAssociationService = Provide[Container.category_association_service],
    ):
        """Assign multiple categories to an entity"""
        data : dict = category_association_ns.payload
        category_data = data.get('category_data')
        
        result = category_association_service.assign_categories_to_entity(
            entity_id=entity_id,
            entity_type=entity_type,
            category_data=category_data
        )
        
        if result:
            return result, 201
        
        category_association_ns.abort(400, "Failed to assign categories to entity")

@category_association_ns.route("/property")
class CategoryAssignment(Resource):
    @inject
    @category_association_ns.doc("get_values_by_property")
    @category_association_ns.expect(property_base_model, validate=True)
    @category_association_ns.response(200, "Property values retrieved")
    def get(
        self,
        category_association_service: ICategoryAssociationService = Provide[Container.category_association_service],
    ):
        data : dict = category_association_ns.payload
        """Get all values for a specific property across all associations"""
        data : dict = category_association_ns.payload
        entity_type = data.get('entity_type')
        category_id = data.get('category_id')
        property_id = data.get('property_id')
   
        values = category_association_service.get_values_by_property(
            property_id=property_id,
            category_id=category_id,
            entity_type=entity_type
        )
        
        return values, 200


    @inject
    @category_association_ns.doc("set_property_value")
    @category_association_ns.expect(property_value_input_model, validate=False)  # we validate at service level
    @category_association_ns.response(200, "Property value successfully set")
    @category_association_ns.response(400, "Invalid input")
    @category_association_ns.response(404, "Association not found")
    def put(
        self,
        category_association_service: ICategoryAssociationService = Provide[Container.category_association_service],
    ):
        """Set a property value for a category association"""
        data : dict = category_association_ns.payload
        entity_id = data.get('entity_id')
        entity_type = data.get('entity_type')
        category_id = data.get('category_id')
        property_id = data.get('property_id')
        value = data.get('value')
        
        success = category_association_service.set_property_value(
            entity_id = entity_id,
            entity_type=entity_type,
            category_id=category_id,
            property_id=property_id,
            value=value
        )
        
        if success:
            return {"message": "Property value successfully set"}, 200
        
        category_association_ns.abort(404, "Association or property not found")
    
    @inject
    @category_association_ns.doc("delete_property")
    @category_association_ns.expect(property_association_model, validate=True) 
    @category_association_ns.response(204, "Property successfully deleted")
    @category_association_ns.response(404, "Association or property not found")
    def delete(
        self,
        category_association_service: ICategoryAssociationService = Provide[Container.category_association_service],
    ):
        """Delete a property from a category association"""
        data : dict = category_association_ns.payload
        entity_id = data.get('entity_id')
        entity_type = data.get('entity_type')
        category_id = data.get('category_id')
        property_id = data.get('property_id')


        success = category_association_service.delete_property(
            entity_id = entity_id,
            entity_type=entity_type,
            category_id=category_id,
            property_id=property_id,
        )
        
        if success:
            return '', 204
        
        category_association_ns.abort(404, "Association or property not found")