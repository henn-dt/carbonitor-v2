from typing import TypeVar

from app.core.application.dtos.category.category_dto import (
    CategoryDTO, CategoryProperty, CategoryPropertySchema, CategoryResponseDTO,
    CategoryUpdateDTO)
from app.core.application.mappers.icategory_mapper import ICategoryMapper
from app.core.domain.entities.category import Category

T = TypeVar(
    "T", CategoryDTO, CategoryUpdateDTO, CategoryResponseDTO
)  # not useful for this implementation


class CategoryMapper(ICategoryMapper):

    @staticmethod
    def create_entity_from_dto(categoryDTO: CategoryDTO) -> Category:
        return Category(**categoryDTO.model_dump(exclude_unset=True))

    @staticmethod
    def create_entity_from_update_dto(categoryUpdateDTO: CategoryUpdateDTO) -> Category:
        return Category(**categoryUpdateDTO.model_dump(exclude_unset=True))

    @staticmethod
    def create_dto_from_entity(category: Category) -> CategoryResponseDTO:
        try:
            # Get the category data as dict
            category_data = category.to_dict()        
            # Handle property_schema specially
            if "property_schema" in category_data and category_data["property_schema"]:
                # Convert each CategoryPropertySchema to a JSON-serializable dict
                serialized_properties = {}
                for key, prop in category_data["property_schema"].items():
                    # Ensure key is string for JSON compatibility
                    str_key = str(key)

                    # Convert prop to dict if it's not already
                    if isinstance(prop, dict):
                        serialized_properties[str_key] = prop
                    elif hasattr(prop, "model_dump"):
                        serialized_properties[str_key] = prop.model_dump()
                    else:
                        # Try to convert to CategoryPropertySchema first
                        try:
                            prop_schema = CategoryPropertySchema(**prop)
                            serialized_properties[str_key] = prop_schema.model_dump()
                        except Exception:
                            # If conversion fails, use as is
                            serialized_properties[str_key] = prop

                # Replace the property_schema with the serialized version
                category_data["property_schema"] = serialized_properties
        
                # Create and validate the ResponseDTO
            response_dto = CategoryResponseDTO(**category_data)
            return response_dto
        except Exception as e:
            print(f"Error creating Category Response object: {str(e)}")

    @staticmethod
    def create_property_from_schema(
        property_id: str, property_schema=CategoryPropertySchema
    ) -> CategoryProperty:
        property_data = property_schema.model_dump() if hasattr(property_schema, "model_dump") else property_schema
        property_data["id"] = property_id
        try:
            return CategoryProperty.model_validate(CategoryProperty(**property_data))
        except Exception as e:
            print(f"Error creating CategoryProperty object: {str(e)}")
