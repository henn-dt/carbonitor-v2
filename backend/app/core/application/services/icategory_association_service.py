from abc import ABC, abstractmethod
from typing import Any, Collection, Dict, List, Optional, TypeVar, Union

from app.core.application.dtos.category.category_dto import (
    CategoryDTO, CategoryResponseDTO)
from app.core.application.dtos.category_association.category_association_dto import (
    CategoryAssociationCategoryDTO, CategoryAssociationResponseDTO)
from app.core.domain.enums.category_entity_type import CategoryEntityType


class ICategoryAssociationService(ABC):

    @abstractmethod    
    def get_by_id(self, id : int) -> CategoryAssociationResponseDTO:
        pass

    @abstractmethod    
    def get_by_entity_id_and_type(self, entity_id : int, entity_type : CategoryEntityType) -> List[CategoryAssociationResponseDTO]:
        pass

    @abstractmethod    
    def get_by_category_id_and_type(self, category_id : int, entity_type : CategoryEntityType) -> List[CategoryAssociationResponseDTO]:
        pass

    @abstractmethod        
    def get_entities_id_list_by_category(self, category_id : int, entity_type : CategoryEntityType ) -> List[int]:
        pass

    @abstractmethod                    
    def get_categories_by_entity(self, entity_id : int, entity_type : CategoryEntityType) -> List[CategoryResponseDTO]:
        pass


    @abstractmethod
    def assign_category_to_entity(self, entity_id: int, entity_type: CategoryEntityType, category_id: int, property_values: Dict[str, Any] = None) -> Optional[CategoryAssociationResponseDTO]:
        pass

    @abstractmethod
    def assign_category_to_entity_list(
        self, 
    entity_list : List[int], 
    entity_type_list : Union[ CategoryEntityType, List[CategoryEntityType]], 
    category_id : int,
    property_values_list: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None) -> Optional[List[CategoryAssociationResponseDTO]]:
        pass


    @abstractmethod
    def assign_categories_to_entity(self, entity_id: int, entity_type: CategoryEntityType, category_data: List[Dict[str, Any]]) -> List[CategoryAssociationResponseDTO]:
        pass

    @abstractmethod
    def assign_categories_to_entity_list(self, entity_id_list: int, entity_type: CategoryEntityType, category_data: List[Dict[str, Any]]) -> List[CategoryAssociationResponseDTO]:
        pass


# delete
    @abstractmethod
    def delete_association(self, entity_id: int, entity_type: CategoryEntityType, category_id: int) -> bool:
        pass



# public property operations
    @abstractmethod
    def set_property_value(self, entity_id : int, entity_type : CategoryEntityType, category_id : int, property_id: str, value: Any) -> bool:
        pass

    @abstractmethod
    def get_values_by_property(self, property_id: str, category_id : int, entity_type: CategoryEntityType = None) -> Dict[int, Any]:     # if only property ID were unique...
        pass

    @abstractmethod
    def delete_property(self, entity_id : int, entity_type : CategoryEntityType, category_id : int, property_id: str) -> bool:
        pass