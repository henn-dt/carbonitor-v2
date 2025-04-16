from typing import Any, Collection, Dict, List, Optional

from app.core.application.dtos.category.category_dto import (
    CategoryDTO, CategoryProperty, CategoryPropertySchema, CategoryResponseDTO,
    CategoryUpdateDTO)
from app.core.application.mappers.icategory_mapper import ICategoryMapper
from app.core.application.repositories.category.icategory_read_repository import \
    ICategoryReadRepository
from app.core.application.repositories.category.icategory_write_repository import \
    ICategoryWriteRepository
from app.core.application.services.icategory_service import ICategoryService


class CategoryService(ICategoryService):
    def __init__(
        self,
        category_read_repository: ICategoryReadRepository,
        category_write_repository: ICategoryWriteRepository,
        category_mapper: ICategoryMapper,
    ):
        self._read_repo = category_read_repository
        self._write_repo = category_write_repository
        self._category_mapper = category_mapper

# helpers
    def get_default_property_values(self, category: CategoryResponseDTO) -> Optional[Dict[str, Any]]:
        """
        Gets default property values based on association category

        Args:
            association : the category association dto

        Returns:
            default value as id : value dictionary.
        """

        category_properties = category.properties
        return {str(prop['id']) : prop['default'] for prop in category_properties}

    def ensure_default_property_values(self, property_values : Dict[str, Any], category : CategoryResponseDTO) -> Optional[Dict[str, Any]]:
        """
        Injects default property values in values dictionary, based on association category

        Args:
            association : the category association dto

        Returns:
            original values dictionary but with added default values if missing.
        """

        default_values : Dict[str, Any] = self.get_default_property_values(category)

        if not property_values or property_values == {}:
            return default_values 
        for key, value in default_values.items():
            if property_values[key]:
                continue
            property_values[key] = value
        return property_values

    def get_category_by_dto(self, categoryDTO: CategoryDTO) -> CategoryResponseDTO:
        category_entity = self._read_repo.get_by_name_and_type(name=categoryDTO.name, type=categoryDTO.type)
        return self._category_mapper.create_dto_from_entity(category_entity)

    def get_all_categories_by_type(
        self, category_type: str
    ) -> List[CategoryResponseDTO]:
        category_entity_list = self._read_repo.filter({"category_type": category_type})
        return [self._category_mapper.create_dto_from_entity(category_entity) for category_entity in category_entity_list ]

    def get_category_by_id(self, category_id: int) -> CategoryResponseDTO:
        category_entity = self._read_repo.get_by_id(id=category_id)
        return self._category_mapper.create_dto_from_entity(category_entity)

    def get_all_categories(self) -> List[CategoryResponseDTO]:
        category_entity_list = self._read_repo.get_all()
        return [
            self._category_mapper.create_dto_from_entity(category_entity)
            for category_entity in category_entity_list
        ]

    def get_category_property_by_id(
        self, categoryResponseDTO: CategoryResponseDTO, property_id: int
    ) -> CategoryProperty:
        return self._category_mapper.create_property_from_schema(
            property_id, categoryResponseDTO.property_schema[property_id]
        )

    def _create_category(self, categoryDTO: CategoryDTO) -> CategoryResponseDTO:
        created_category = self._write_repo.create(
            self._category_mapper.create_entity_from_dto(categoryDTO)
        )
        print(f"created category: {created_category}")
        return self._category_mapper.create_dto_from_entity(created_category)

    def create_category_from_dto(
        self, categoryDTO: CategoryDTO, user_id: Optional[int] = None
    ) -> CategoryResponseDTO:
        if user_id:
            categoryDTO.user_id_created = user_id
            categoryDTO.user_id_updated = user_id
        existing_message = "Category exists already in database"

        if self._read_repo.exists_by_name_and_type(categoryDTO.name, categoryDTO.type):
            return existing_message
        try:
            return self._create_category(categoryDTO)
        except Exception as e:
            print(
                f"error creating category {categoryDTO.name} ({categoryDTO.type}): {str(e)}"
            )

    def create_category_from_dto_list(
        self, categoryDTOs: List[CategoryDTO], user_id: Optional[int] = None
    ) -> List[CategoryResponseDTO]:
        category_list = []
        existing_category_list = []
        failed_category_list = []
        for categoryDTO in categoryDTOs:
            try:
                if user_id:
                    categoryDTO.user_id_created = user_id
                    categoryDTO.user_id_updated = user_id
                    created_category = self.create_category_from_dto(categoryDTO)
                else:
                    created_category = self.create_category_from_dto(categoryDTO)
                if created_category:
                    category_list.append(created_category)
                else:
                    existing_category_list.append(categoryDTO)
            except Exception as e:
                print(
                    f"error creating category {categoryDTO.name} ({categoryDTO.type}): {str(e)}"
                )
                failed_category_list.append(categoryDTO)

        print(f"attempting to write {len(categoryDTOs)} categories to database")
        print(f"successfully added new categories: {len(category_list)}")
        print(
            f"categories already in database that were not updated: {len(existing_category_list)}"
        )
        print(f"categories that generated an error: {len(failed_category_list)}")
        print(
            f"failed categories: \n {[ f'{categoryDTO.name} ({categoryDTO.type})' for categoryDTO in failed_category_list]}"
        )

    def update_category_from_dto(
        self, categoryDTO: CategoryUpdateDTO, user_id: Optional[int] = None
    ) -> CategoryResponseDTO:
        missing_message = f"category does not exists in database: {categoryDTO}"
        if hasattr(categoryDTO, "id"):
            existing_category = self._read_repo.get_by_id(categoryDTO.id)
        elif hasattr(categoryDTO, "name") and hasattr(categoryDTO, "type"):
            existing_category = self._read_repo.get_by_name_and_type(
                name=categoryDTO.name, type=categoryDTO.type
            )
        else:
            print("cannot find category in database, need either id or name and type")
            return False
        if not existing_category:
            print(missing_message)
            return False
        if user_id:
            categoryDTO.user_id_updated = user_id
        updated_category = self._write_repo.update(
            self._category_mapper.create_entity_from_update_dto(categoryDTO)
        )
        return self._category_mapper.create_dto_from_entity(updated_category)

    def create_category_property(
        self, category_id: int, property: CategoryPropertySchema
    ):
        existing_category = self.get_category_by_id(category_id)
        if not existing_category:
            return print(f"category {category_id} not found in database")
        try:
            category_data = CategoryUpdateDTO.model_validate(
                CategoryUpdateDTO(**existing_category.model_dump())
            )
            # Generate a new string ID for the property
            # Convert existing keys to integers, find max, add 1, then back to string
            existing_keys = category_data.property_schema.keys() if category_data.property_schema else []
            numeric_keys = [int(k) for k in existing_keys if k.isdigit()]
            new_id = str(max(numeric_keys, default=0) + 1)
            category_data.property_schema[new_id] = property
            updated_category = self.update_category_from_dto(category_data)
            return self._category_mapper.create_dto_from_entity(updated_category)
        except Exception as e:
            print(f"error creating category {category_id}): {str(e)}")

    def update_category_property(
        self, category_id: int, property: CategoryProperty
    ) -> CategoryProperty:
        existing_category = self.get_category_by_id(category_id)
        if not existing_category:
            return print(f"category {category_id} not found in database")
        try:
            category_data = CategoryUpdateDTO.model_validate(
                CategoryUpdateDTO(**existing_category.model_dump())
            )
            property_schema = CategoryPropertySchema.model_validate(
                CategoryPropertySchema(**{k: v for k, v in property.model_dump().items() if k != "id"})
            )
            # Ensure property.id is a string
            property_id = str(property.id)
            category_data.property_schema[property_id] = property_schema
            updated_category = self.update_category_from_dto(category_data)
            return self._category_mapper.create_dto_from_entity(updated_category)
        except Exception as e:
            print(f"error creating category {category_id}): {str(e)}")

    def delete_category(self, category_id: int) -> bool:
        existing_category = self.get_category_by_id(category_id)
        if not existing_category:
            print(f"category {category_id} does not exist")
            return False
        try:
            self._write_repo.delete(category_id)
            return True
        except:
            return False

    def delete_category_property(self, category_id: int, property_id: str) -> bool:
        existing_category = self.get_category_by_id(category_id)
        if not existing_category:
            return False
        existing_property = existing_category.property_schema[property_id]
        if not existing_property:
            return False
        if existing_category.property_schema.pop(property_id):
            return True
        return False
