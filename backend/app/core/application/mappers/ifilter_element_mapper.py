from abc import abstractmethod

from app.core.domain.entities.filter_element import FilterElement
from app.core.application.dtos.filter_element.filter_element_dto import FilterElementCreateDTO, FilterElementResponseDTO, FilterElementUpdateDTO


class IFilterElementMapper:

    @abstractmethod
    def entity_from_create_dto(filterDTO: FilterElementCreateDTO) -> FilterElement:
        pass

    @abstractmethod
    def entity_from_update_dto(filterDTO: FilterElementUpdateDTO) -> FilterElement:
        pass

    @abstractmethod
    def response_dto_from_entity(filter: FilterElement) -> FilterElementResponseDTO:
        pass