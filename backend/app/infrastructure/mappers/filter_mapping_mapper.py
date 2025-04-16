from typing import TypeVar, Union

from app.core.application.mappers.ifilter_mapping_mapper import IFilterMappingMapper
from app.core.application.dtos.filter_mapping.filter_mapping_dto import FilterMappingCreateDTO, FilterMappingResponseDTO, FilterMappingUpdateDTO
from app.core.domain.entities.filter_mapping import FilterMapping


class FilterMappingMapper(IFilterMappingMapper):

    @staticmethod
    def entity_from_dto(filter_dto: Union[FilterMappingCreateDTO, FilterMappingUpdateDTO]) -> FilterMapping:            
        return FilterMapping(**filter_dto.model_dump(exclude_unset=True))
    

    @staticmethod
    def response_dto_from_entity(filter_entity: FilterMapping) -> FilterMappingResponseDTO:
        try:
            # Get the filter data as dict
            filter_data = filter_entity.to_dict()            
            # Create and validate the ResponseDTO
            response_dto = FilterMappingResponseDTO(**filter_data)
            return response_dto
        except Exception as e:
            print(f"Error creating filter mapping Response object: {str(e)}")