import datetime
from itertools import zip_longest
import re
from typing import Any, Collection, Dict, List, Optional, TypeVar, Union

from app.core.application.dtos.category.category_dto import (
    CategoryPropertySchema, CategoryResponseDTO)
from app.core.application.dtos.category_association.category_association_dto import (
    CategoryAssociationDTO, CategoryAssociationResponseDTO)
from app.core.application.mappers.icategory_association_mapper import \
    ICategoryAssociationMapper
from app.core.application.repositories.category_association.icategory_association_read_repository import \
    ICategoryAssociationReadRepository
from app.core.application.repositories.category_association.icategory_association_write_repository import \
    ICategoryAssociationWriteRepository
from app.core.application.services.icategory_association_service import \
    ICategoryAssociationService
from app.core.application.services.icategory_service import ICategoryService
from app.core.domain.enums.category_entity_type import CategoryEntityType
from app.core.domain.enums.category_property_format import \
    CategoryPropertyFormat


class CategoryAssociationService(ICategoryAssociationService):
    def __init__(
        self,
        category_association_read_repository: ICategoryAssociationReadRepository,
        category_association_write_repository: ICategoryAssociationWriteRepository,
        category_association_mapper: ICategoryAssociationMapper,
        category_service= ICategoryService
    ):
        self._read_repo = category_association_read_repository
        self._write_repo = category_association_write_repository
        self._mapper = category_association_mapper
        self._category_service = category_service


    def get_by_id(self, id : int) -> CategoryAssociationResponseDTO:
        category_association = self._read_repo.get_by_id(id)
        print(f"service level association: {category_association}")
        return self._mapper.create_dto_from_association_entity(category_association)

    def get_by_entity_id_and_type(self, entity_id : int, entity_type : CategoryEntityType) -> List[CategoryAssociationResponseDTO]:
        category_association_list = self._read_repo.get_by_entity(entity_id = entity_id, entity_type = entity_type)
        print(f"service level associations: {category_association_list}")
        return [self._mapper.category_dto_from_association_entity(entity) for entity in category_association_list]     

    def get_by_category_id_and_type(self, category_id : int, entity_type : CategoryEntityType) -> List[CategoryAssociationResponseDTO]:
        category_association_list = self._read_repo.get_by_category(category_id = category_id, entity_type = entity_type)
        print(f"service level associations: {category_association_list}")
        return [self._mapper.category_dto_from_association_entity(entity) for entity in category_association_list] 
    
    def get_entities_id_list_by_category(self, category_id : int, entity_type : CategoryEntityType ) -> List[int]:
        category_association_list = self.get_by_category_id_and_type(category_id=category_id, entity_type=entity_type)
        return set([association.entity_id for association  in category_association_list])
                    
    def get_categories_by_entity(self, entity_id : int, entity_type : CategoryEntityType) -> List[CategoryResponseDTO]:
        category_association_dto_list = self.get_by_entity_id_and_type(entity_id= entity_id, entity_type= entity_type)

        unique_categories = {category.id : category for category in [association.category for association in category_association_dto_list]}
        return list(unique_categories.values())

# private methods

    def _verify_property_value(self, category: CategoryResponseDTO, property_id: str, value: Any) -> bool:
        """
        check if property matches the schema

        Args:
            category: The category as DTO
            property_id: The ID of the property
            value: The value to verify

        Returns:
            bool: True if the property value is valid, False otherwise
        """
        try:
            if not category.property_schema or property_id not in category.property_schema:
                return False

            property_schema = category.property_schema[property_id]

            if isinstance(property_schema, dict):
                property_schema = CategoryPropertySchema(**property_schema)

            # Check if the value matches the format
            if property_schema.format == CategoryPropertyFormat.STRING and not isinstance(value, str):
                return False
            elif property_schema.format == CategoryPropertyFormat.NUMBER and not isinstance(value, (int, float)):
                return False
            elif property_schema.format == CategoryPropertyFormat.BOOLEAN and not isinstance(value, bool):
                return False
            elif property_schema.format == CategoryPropertyFormat.DATE:
                if isinstance(value, (datetime.date, datetime.datetime)):
                    return True
                # Case 2: Value is a string that needs to be parsed as a date
                elif isinstance(value, str):
                    # ISO 8601 date format: YYYY-MM-DD
                    iso_date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                    # ISO 8601 datetime format: YYYY-MM-DDThh:mm:ss(Z or ±hh:mm)
                    iso_datetime_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?$'
                    
                    if re.match(iso_date_pattern, value) or re.match(iso_datetime_pattern, value):
                        try:
                            # Try to parse the string as a date
                            if 'T' in value:
                                datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
                            else:
                                datetime.date.fromisoformat(value)
                            return True
                        except ValueError:
                            return False
                    return False
                else:
                    return False


            # Check if enum is defined and value is in the enum
            if property_schema.enum and value not in property_schema.enum:
                return False

            return True
        except Exception as e:
            # Log the error
            print(f"Error verifying property value: {e}")
            return False


    def _assign_property_value(self, association : CategoryAssociationResponseDTO, property_id: str, value: Any) -> bool:
        """
        Assigns a property value to a category association

        Args:
            association_id: The ID of the association
            property_id: The ID of the property
            value: The value to assign

        Returns:
            bool: True if the assignment was successful, False otherwise
        """
        try:
            # Verify the property value
            if not self._verify_property_value(association.category, property_id, value):
                return False

            # Update the values
            values = association.values or {}
            values[property_id] = value

            # Update the association
            self._write_repo.update_entity_category_values(
                entity_id=association.entity_id,
                entity_type=association.entity_type,
                category_id=association.category_id,
                values=values
            )

            return True
        except Exception as e:
            # Log the error
            print(f"Error assigning property value: {e}")
            return False

    def _read_property_value(self, association_id: int, property_id: str) -> Any:
        """
        Reads a property value from a category association

        Args:
            association_id: The ID of the association
            property_id: The ID of the property

        Returns:
            Any: The property value, or None if not found
        """
        try:
            # Get the association
            association = self._read_repo.get_by_id(association_id)
            if not association or not association.values:
                return None

            # Return the property value
            return association.values.get(property_id)
        except Exception as e:
            # Log the error
            print(f"Error reading property value: {e}")
            return None

    def _remove_property_value(self, association: CategoryAssociationResponseDTO, property_id: str) -> bool:
        """
        Removes a property value from a category association

        Args:
            association_id: The ID of the association
            property_id: The ID of the property

        Returns:
            bool: True if the removal was successful, False otherwise
        """
        try:

            # Remove the property value
            values = association.values
            if property_id in values:
                del values[property_id]

                # Update the association
                self._write_repo.update_entity_category_values(
                    entity_id=association.entity_id,
                    entity_type=association.entity_type,
                    category_id=association.category_id,
                    values=values
                )

                return True
            return False
        except Exception as e:
            # Log the error
            print(f"Error removing property value: {e}")
            return False

    def _verify_association(self, entity_id : int, entity_type : CategoryEntityType, category_id : int, property_values: Dict[str, Any] = None) -> bool:
        """
        Call category service to verify category
        Verify if type of entity and category match
        Verify that association doesn't already exist
        If properties are supplied, verify they match the schema
        
        Args:
            entity_id: The ID of the entity
            entity_type: The type of the entity
            category_id: The ID of the category
            values: Optional dictionary of property values
            
        Returns:
            bool: True if the association is valid, False otherwise
        """
        try:


            # Check if association already exists
            existing = self._read_repo.get_by_keys({
                "entity_id" : entity_id,
                "entity_type" : entity_type,
                "category_id" : category_id
                })
            
            if existing:
                return False    

            # Get the category
            category : CategoryResponseDTO = self._category_service.get_category_by_id(category_id)


            # Verify category exists
            if not category:
                return False
                
            # Verify category type matches entity type
            if category.type != entity_type:
                return False
                
            # Verify properties if provided
            if property_values and category.property_schema:
                print("verifying supplied properties values")
                for property_id, value in property_values.items():
                    if property_id not in category.property_schema:
                        return False
            
                    if not self._verify_property_value(category, property_id, value):
                        return False
                        
                # Check if all required properties are provided
                for property_id, schema in category.property_schema.items():
                    if schema.required and property_id not in property_values:
                        # If a default value exists for a required parameter, i assume we will use that
                        if schema.default is None:
                            return False
            
            return True
        except Exception as e:
            # Log the error
            print(f"Error verifying association: {e}")
            return False

    def _create_association(self, association : CategoryAssociationDTO) -> Optional[CategoryAssociationResponseDTO]:
        """
        Verify association then write to repo

        Args:
            entity_id: The ID of the entity
            entity_type: The type of the entity
            category_id: The ID of the category
            values: Optional dictionary of property values

        Returns:
            CategoryAssociationResponseDTO or None: The created association, or None if creation failed
        """

        entity_id = association.entity_id
        entity_type = association.entity_type
        category_id = association.category_id
        property_values = association.values

        try:
            # Verify the association
            if not self._verify_association(entity_id, entity_type, category_id, property_values):
                return None

            category = self._category_service.get_category_by_id(category_id)

            # set default property values if properties are not set
            property_values = self._category_service.ensure_default_property_values(property_values, category)


            # Create the association
            association_entity = self._write_repo.associate_entity_with_category(
                entity_id=entity_id,
                entity_type=entity_type.value if isinstance(entity_type, CategoryEntityType) else str(entity_type),
                category_id=category_id,
                values=property_values
            )

            # Return the DTO
            return self._mapper.create_dto_from_association_entity(association_entity)
        except Exception as e:
            # Log the error
            print(f"Error creating association: {e}")
            return None


# public assign
    def assign_category_to_entity(self, entity_id: int, entity_type: CategoryEntityType, category_id: int, property_values: Dict[str, Any] = None) -> Optional[CategoryAssociationResponseDTO]:
        """
        Base method to assign a category to an entity using the _create_association method

        Args:
            entity_id: The ID of the entity
            entity_type: The type of the entity
            category_id: The ID of the category
            values: Optional dictionary of property values

        Returns:
            CategoryAssociationResponseDTO or None: The created association, or None if creation failed
        """
        try:
            association = CategoryAssociationDTO.model_validate(CategoryAssociationDTO(entity_id=entity_id, entity_type=entity_type,category_id=category_id, values=property_values))
            return self._create_association(association)
        except Exception as e:
            print(f"error parsing association input parameters: {str(e)}")

    def assign_category_to_entity_list(
        self, 
    entity_list : List[int], 
    entity_type_list : Union[ CategoryEntityType, List[CategoryEntityType]], 
    category_id : int,
    property_values_list: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None) -> Optional[List[CategoryAssociationResponseDTO]]:
        """
        Assign a category to multiple entities with their respective property values
        """

        created_associations = []
        failed_associations = []

        # Handle None property_values_list
        if property_values_list is None:
            property_values_list = [None] * len(entity_list)

        # handle singetons for property values, applying values to all entities
        elif not isinstance(property_values_list, Collection):
            property_values_list = property_values_list * len(entity_list)

        # Validate input lengths
        if len(property_values_list) > len(entity_list):
            print(
                f"Property values list ({len(property_values_list)} items) is longer than the entity list ({len(entity_list)} items). Extra values will be ignored."
            )
            property_values_list = property_values_list[:len(entity_list)]

        # Normalize entity_type_list to always be a list
        if not isinstance(entity_type_list, list):
            # Convert single entity type to a list with the same type for all entities
            entity_types = [entity_type_list] * len(entity_list)
        else:
            # We have a list of entity types
            if len(entity_type_list) == 1:
                # Single type provided as a list, apply to all entities
                entity_types = [entity_type_list[0]] * len(entity_list)
            elif len(entity_type_list) != len(entity_list):
                # List lengths mismatch - this is an error
                print(
                    f"Entity type list length ({len(entity_type_list)}) doesn't match entity list length ({len(entity_list)}). Operation aborted."
                )
                return []
            else:
                # Use the provided list as is
                entity_types = entity_type_list
    
        # Process each entity with its type and properties
        for i, (entity_id, entity_type, property_values) in enumerate(
            zip(entity_list, entity_types, property_values_list)
        ):
            try:
                association = self.assign_category_to_entity(
                    entity_id=entity_id,
                    entity_type=entity_type,
                    category_id=category_id,
                    values=property_values
                )
                if association:
                    created_associations.append(association)
                else:
                    failed_associations.append(str(entity_id))
            except Exception as e:
                print(f"Error assigning category {category_id} to entity {entity_id}: {str(e)}")
                failed_associations.append(str(entity_id))

        # Log failures if any
        if failed_associations:
            print(
                f"Failed to create {len(failed_associations)} associations for entities: {', '.join(failed_associations)}"
            )

        return created_associations




    def assign_categories_to_entity(self, entity_id: int, entity_type: CategoryEntityType, category_data: List[Dict[str, Any]]) -> List[CategoryAssociationResponseDTO]:
        """
        Assign multiple categories to an entity

        Args:
            entity_id: The ID of the entity
            entity_type: The type of the entity
            category_data: List of dictionaries containing category_id and optional values

        Returns:
            List[CategoryAssociationResponseDTO]: List of created associations
        """
        result = []

        try:
            # Transform category_data into expected format for batch operation
            formatted_data = []
            for item in category_data:
               
                category_id = item.get('category_id')
                values = item.get('values')

                if category_id and self._verify_association(entity_id, entity_type, category_id, values):
                    formatted_data.append({
                        'category_id': category_id,
                        'values': self._category_service.ensure_default_property_values(values, self._category_service.get_category_by_id(category_id))
                    })

            # Batch associate
            if formatted_data:
                associations = self._write_repo.batch_associate_entity_with_categories(
                    entity_id=entity_id,
                    entity_type=entity_type,
                    category_data=formatted_data
                )

                # Convert to DTOs
                result = [self._mapper.create_dto_from_association_entity(association) for association in associations]
        except Exception as e:
            # Log the error
            print(f"Error assigning multiple categories: {e}")

        return result

    def assign_categories_to_entity_list(self, entity_id_list: int, entity_type: CategoryEntityType, category_data: List[Dict[str, Any]]) -> List[CategoryAssociationResponseDTO]:
        """
        Assign multiple categories to an entity

        Args:
            entity_id_list: List of IDs of the entities
            entity_type: The type of the entity
            category_data: List of dictionaries containing category_id and optional values. The same values will be applied to each entity. 

        Returns:
            List[CategoryAssociationResponseDTO]: List of created associations
        """
        result = []
        try:
            for entity_id in entity_id_list:
                result.append(self.assign_categories_to_entity(entity_id, entity_type, category_data))
        except Exception as e:
            print(f"Error assigning multiple entities to multiple categories: {e}")
        return result



# delete

    def delete_association(self, entity_id: int, entity_type: CategoryEntityType, category_id: int) -> bool:
        """
        Delete an association between an entity and a category

        Args:
            entity_id: The ID of the entity
            entity_type: The type of the entity
            category_id: The ID of the category

        Returns:
            bool: True if the deletion was successful, False otherwise
        """
        try:
            return self._write_repo.remove_entity_from_category(
                entity_id=entity_id,
                entity_type=entity_type,
                category_id=category_id
            )
        except Exception as e:
            # Log the error
            print(f"Error deleting association: {e}")
            return False



# public property operations
    def set_property_value(self, entity_id : int, entity_type : CategoryEntityType, category_id : int, property_id: str, value: Any) -> bool:
        """
        Set a property value for a category association

        Args:
            property_id: The ID of the property
            value: The value to set

        Returns:
            bool: True if the operation was successful, False otherwise
        """
        association = self._read_repo.get_by_keys({'entity_id' : entity_id, 'entity_type' : entity_type,'category_id' : category_id,})

        return self._assign_property_value(association, property_id, value)

    def get_values_by_property(self, property_id: str, category_id : int, entity_type: CategoryEntityType = None) -> Dict[int, Any]:     # if only property ID were unique...
        """
        Get all values for a specific property across all associations

        Args:
            property_id: The ID of the property
            entity_type: Optional filter by entity type

        Returns:
            Dict[int, Any]: Dictionary mapping association IDs to property values
        """
        try:
            # Get all associations
            associations = self._read_repo.get_by_category(category_id=category_id, entity_type=entity_type)

            # Filter associations with the given property
            result = {}
            for association in associations:
                if association.values and property_id in association.values:
                    result[association.id] = association.values[property_id]

            return result
        except Exception as e:
            # Log the error
            print(f"Error getting values by property: {e}")
            return {}

    def delete_property(self, entity_id : int, entity_type : CategoryEntityType, category_id : int, property_id: str) -> bool:
        """
        Delete a property from a category association
        Args:
            property_id: The ID of the property
        Returns:
            bool: True if the deletion was successful, False otherwise
        """
        try:
            association = self._read_repo.get_by_keys({'entity_id' : entity_id, 'entity_type' : entity_type,'category_id' : category_id,})
        except:
            return False
        return self._remove_property_value(association, property_id)

    