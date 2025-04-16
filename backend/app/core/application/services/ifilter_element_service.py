# app/core/application/services/iproduct_service.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from app.core.application.dtos.filter_element.filter_element_dto import FilterElementCreateDTO, FilterElementResponseDTO, FilterElementUpdateDTO



class IFilterElementService(ABC):

    @abstractmethod
    def get_filter_element_by_id(self, filter_id: int) -> FilterElementResponseDTO:
        pass

    @abstractmethod
    def get_all_filter_elements(self) -> List[FilterElementResponseDTO]:
        pass
    
    @abstractmethod
    def _create_filter_element(self, filterDTO: FilterElementCreateDTO) -> FilterElementResponseDTO:
        pass

    @abstractmethod
    def create_filter_element_from_dto(
        self, filterDTO: FilterElementCreateDTO, user_id: Optional[int] = None
    ) -> FilterElementResponseDTO:
        pass

    @abstractmethod
    def create_filter_elements_from_dto_list(
        self, filterDTOs: List[FilterElementCreateDTO], user_id: Optional[int] = None
    ) -> List[FilterElementResponseDTO]:
        pass

    @abstractmethod
    def update_filter_elements_from_dto(
        self, filter: FilterElementUpdateDTO, user_id: Optional[int] = None
    ) -> FilterElementResponseDTO:
        pass

    @abstractmethod
    def delete_filter(self, filter_id: int) -> bool:
        pass
