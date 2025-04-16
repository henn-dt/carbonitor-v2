from abc import abstractmethod
from typing import Union

from app.core.domain.entities.filter_mapping import FilterMapping
from app.core.application.dtos.filter_mapping.filter_mapping_dto import FilterMappingCreateDTO, FilterMappingResponseDTO, FilterMappingUpdateDTO


class IFilterMappingMapper:

    @abstractmethod
    def entity_from_dto(filterDTO: Union[FilterMappingCreateDTO, FilterMappingUpdateDTO]) -> FilterMapping:
        pass

    @abstractmethod
    def response_dto_from_entity(filter: FilterMapping) -> FilterMappingResponseDTO:
        pass