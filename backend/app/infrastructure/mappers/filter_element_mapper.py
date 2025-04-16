from typing import TypeVar

from app.core.application.mappers.ifilter_element_mapper import IFilterElementMapper
from app.core.application.dtos.filter_element.filter_element_dto import FilterElementCreateDTO, FilterElementResponseDTO, FilterElementUpdateDTO
from app.core.domain.entities.filter_element import FilterElement


class FilterElementMapper(IFilterElementMapper):

    @staticmethod
    def entity_from_create_dto(filterDTO: FilterElementCreateDTO) -> FilterElement:
        return FilterElement(**filterDTO.model_dump(exclude_unset=True))

    @staticmethod
    def entity_from_update_dto(filterDTO: FilterElementUpdateDTO) -> FilterElement:
        return FilterElement(**filterDTO.model_dump(exclude_unset=True))

    @staticmethod
    def response_dto_from_entity(filter: FilterElement) -> FilterElementResponseDTO:
        try:
            # Get the filter data as dict
            filter_data = filter.to_dict()            
            # Create and validate the ResponseDTO
            response_dto = FilterElementResponseDTO(**filter_data)
            return response_dto
        except Exception as e:
            print(f"Error creating filter Response object: {str(e)}")
            raise
