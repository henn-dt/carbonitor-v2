# app/core/application/services/iproduct_service.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from app.core.application.dtos.filter_mapping.filter_mapping_dto import FilterMappingCreateDTO, FilterMappingResponseDTO, FilterMappingUpdateDTO



class IFilterMappingService(ABC):

    @abstractmethod
    def get_filter_mapping_by_id(self, mapping_id: int) -> Optional[FilterMappingResponseDTO]:
        pass

    @abstractmethod
    def get_all_filter_mappings(self) -> List[FilterMappingResponseDTO]:
        pass
    

    @abstractmethod
    def create_filter_mapping_from_dto(self, 
        mappingDTO: FilterMappingCreateDTO, user_id: Optional[int] = None, 
        match_against : Optional[List[FilterMappingResponseDTO]] = None
        ) -> FilterMappingResponseDTO:
        pass

    @abstractmethod
    def create_filter_mappings_from_dto_list(
        self, mapping_dtos: List[FilterMappingCreateDTO], user_id: Optional[int] = None
    ) -> Optional[List[FilterMappingResponseDTO]]:
        pass

    @abstractmethod
    def update_filter_mappings_from_dto(
        self, mapping_dto: FilterMappingUpdateDTO, user_id: Optional[int] = None
    ) -> Union[FilterMappingResponseDTO, bool]:
        pass

    @abstractmethod
    def delete_filter_mapping(self, mapping_id: int) -> bool:
        pass
