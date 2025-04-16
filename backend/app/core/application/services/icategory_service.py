# app/core/application/services/iproduct_service.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from app.core.application.dtos.category.category_dto import (
    CategoryDTO, CategoryProperty, CategoryPropertySchema, CategoryResponseDTO,
    CategoryUpdateDTO)


class ICategoryService(ABC):

    @abstractmethod
    def get_default_property_values(self, category: CategoryResponseDTO) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def ensure_default_property_values(self, property_values : Dict[str, Any], category : CategoryResponseDTO) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_category_by_dto(self, categoryDTO : CategoryDTO) -> CategoryResponseDTO:
        pass

    @abstractmethod
    def get_all_categories_by_type(self, category_type : str) -> List[CategoryResponseDTO]:
        pass

    @abstractmethod
    def get_category_by_id(self, category_id : int) -> CategoryResponseDTO:
        pass

    @abstractmethod
    def get_all_categories(self) -> List[CategoryResponseDTO]:
        pass

    @abstractmethod
    def get_category_property_by_id(self, categoryResponseDTO: CategoryResponseDTO, property_id : int) -> CategoryProperty:
        pass

    @abstractmethod
    def create_category_from_dto(self, categoryDTO : CategoryDTO, user_id : Optional[int] = None) -> CategoryResponseDTO:
        pass

    @abstractmethod
    def create_category_from_dto_list(self, categoryDTOs : List[CategoryDTO], user_id : Optional[int] = None) -> List[CategoryResponseDTO]:
        pass

    @abstractmethod
    def create_category_property(self, category_id : int, property : CategoryPropertySchema):
        pass

    @abstractmethod
    def update_category_from_dto(self, categoryDTO : CategoryUpdateDTO) -> CategoryResponseDTO:
        pass

    @abstractmethod
    def update_category_property(self, category_id : int, property : CategoryProperty) -> CategoryProperty:
        pass

    @abstractmethod
    def delete_category(self, category_id : int) -> bool:
        pass

    @abstractmethod
    def delete_category_property(self, category_id : int, property_id : int) -> bool:
        pass
