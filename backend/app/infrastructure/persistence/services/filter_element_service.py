from typing import Any, Collection, Dict, List, Optional

from app.core.application.mappers.ifilter_element_mapper import IFilterElementMapper
from app.core.application.repositories.filter_element.ifilter_element_read_repository import IFilterElementReadRepository
from app.core.application.repositories.filter_element.ifilter_element_write_repository import IFilterElementWriteRepository
from app.core.application.dtos.filter_element.filter_element_dto import FilterElementCreateDTO, FilterElementResponseDTO, FilterElementUpdateDTO
from app.core.application.services.ifilter_element_service import IFilterElementService



class FilterElementService(IFilterElementService):
    def __init__(
        self,
        filter_element_read_repository: IFilterElementReadRepository,
        filter_element_write_repository: IFilterElementWriteRepository,
        filter_element_mapper: IFilterElementMapper,
    ):
        self._read_repo = filter_element_read_repository
        self._write_repo = filter_element_write_repository
        self._mapper = filter_element_mapper


    def get_filter_element_by_id(self, filter_id: int) -> FilterElementResponseDTO:
        filter_entity = self._read_repo.get_by_id(id=filter_id)
        return self._mapper.response_dto_from_entity(filter_entity)

    def get_all_filter_elements(self) -> List[FilterElementResponseDTO]:
        filter_element_entity_list = self._read_repo.get_all()
        return [
            self._mapper.response_dto_from_entity(filter_entity)
            for filter_entity in filter_element_entity_list
        ]

    def _create_filter_element(self, filterDTO: FilterElementCreateDTO) -> FilterElementResponseDTO:
        filter_entity = self._mapper.entity_from_create_dto(filterDTO)
        created_filter = self._write_repo.create(filter_entity)
        return self._mapper.response_dto_from_entity(created_filter)

    def create_filter_element_from_dto(
        self, filterDTO: FilterElementCreateDTO, user_id: Optional[int] = None
    ) -> FilterElementResponseDTO:
        if user_id:
            filterDTO.user_id_created = user_id
            filterDTO.user_id_updated = user_id
        existing_name = ""
        existing_message = f"Filter exists already in database ({existing_name})"
        existing_filters = self._read_repo.get_by_filter_conditions(filterDTO.filter)

        if len(existing_filters) != 0:
            existing_name = ",".join([filter.name for filter in existing_filters])
            return existing_message
        try:
            return self._create_filter_element(filterDTO)
        except Exception as e:
            print(
                f"error creating model filter: {str(e)}"
            )

    def create_filter_elements_from_dto_list(
        self, filterDTOs: List[FilterElementCreateDTO], user_id: Optional[int] = None
    ) -> List[FilterElementResponseDTO]:
        filter_list = []
        existing_filter_list = []
        failed_filter_list = []
        for filter in filterDTOs:
            try:
                if user_id:
                    filter.user_id_created = user_id
                    filter.user_id_updated = user_id
                    created_filter = self.create_filter_element_from_dto(filter)
                else:
                    created_filter = self.create_filter_element_from_dto(filter)
                if created_filter:
                    filter_list.append(created_filter)
                else:
                    existing_filter_list.append(filter)
            except Exception as e:
                print(
                    f"error creating filter: {str(e)}"
                )
                failed_filter_list.append(filter)

        print(f"attempting to write {len(filterDTOs)} filters to database")
        print(f"successfully added new filters: {len(filter_list)}")
        print(
            f"filters already in database that were not updated: {len(existing_filter_list)}"
        )
        print(f"filters that generated an error: {len(failed_filter_list)}")


    def update_filter_elements_from_dto(
        self, filter: FilterElementUpdateDTO, user_id: Optional[int] = None
    ) -> FilterElementResponseDTO:
        missing_message = f"category does not exists in database: {filter}"
        if hasattr(filter, "id"):
            existing_filter = self._read_repo.get_by_id(filter.id)
        else:
            print("cannot find filter in database, need the id")
            return False
        if not existing_filter:
            print(missing_message)
            return False
        if user_id:
            filter.user_id_updated = user_id
        updated_filter = self._write_repo.update(
            self._mapper.entity_from_update_dto(filter)
        )
        return self._mapper.response_dto_from_entity(updated_filter)


    def delete_filter(self, filter_id: int) -> bool:
        existing_filter = self.get_filter_element_by_id(filter_id)
        if not existing_filter:
            print(f"filter {filter_id} does not exist")
            return False
        try:
            self._write_repo.delete(filter_id)
            return True
        except:
            return False
