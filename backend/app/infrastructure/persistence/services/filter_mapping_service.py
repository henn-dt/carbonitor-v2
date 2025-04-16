from typing import Any, Collection, Dict, List, Optional, Union

from app.core.application.mappers.ifilter_mapping_mapper import IFilterMappingMapper
from app.core.application.repositories.filter_mapping.ifilter_mapping_read_repository import IFilterMappingReadRepository
from app.core.application.repositories.filter_mapping.ifilter_mapping_write_repository import IFilterMappingWriteRepository
from app.core.application.dtos.filter_mapping.filter_mapping_dto import FilterMappingCreateDTO, FilterMappingResponseDTO, FilterMappingUpdateDTO
from app.core.application.services.ifilter_mapping_service import IFilterMappingService



class FilterMappingService(IFilterMappingService):
    def __init__(
        self,
        filter_mapping_read_repository: IFilterMappingReadRepository,
        filter_mapping_write_repository: IFilterMappingWriteRepository,
        filter_mapping_mapper: IFilterMappingMapper,
    ):
        self._read_repo = filter_mapping_read_repository
        self._write_repo = filter_mapping_write_repository
        self._mapper = filter_mapping_mapper

    def _maps_content_matches(self, maps1: dict, maps2: dict) -> bool:
        """
        Compare two maps dictionaries to check if their content matches,
        ignoring potential differences in IDs.
        
        This is a simplified example - only returns True for a perfect match.
        For better validation we need to clear what are "matches". And could be that it all happens in plugin validation anyway. 
        """

        # Handle None values
        if maps1 is None and maps2 is None:
            return True
        if maps1 is None or maps2 is None:
            return False

        # If they're exactly the same, return True immediately
        if maps1 == maps2:
            return True
        
        # If they have different numbers of elements, they can't match
        if len(maps1) != len(maps2):
            return False

        # match their values regardless of IDs
        values1 = sorted([value for key, value in maps1.items()])   
        values2 = sorted([value for key, value in maps2.items()])

        return values1 == values2        

    def get_filter_mapping_by_id(self, mapping_id: int) -> Optional[FilterMappingResponseDTO]:
        mapping_entity = self._read_repo.get_by_id(id=mapping_id)
        if not mapping_entity:
            return None
        return self._mapper.response_dto_from_entity(mapping_entity)

    def get_all_filter_mappings(self) -> List[FilterMappingResponseDTO]:
        filter_mapping_entity_list = self._read_repo.get_all()
        return [
            self._mapper.response_dto_from_entity(filter_entity)
            for filter_entity in filter_mapping_entity_list
        ]

    def _create_filter_mapping(self, mappingDTO: FilterMappingCreateDTO) -> FilterMappingResponseDTO:
        mapping_entity = self._mapper.entity_from_dto(mappingDTO)
        created_mapping = self._write_repo.create(mapping_entity)
        return self._mapper.response_dto_from_entity(created_mapping)

    def create_filter_mapping_from_dto(self, 
        mappingDTO: FilterMappingCreateDTO, user_id: Optional[int] = None, 
        match_against : Optional[List[FilterMappingResponseDTO]] = None
        ) -> FilterMappingResponseDTO:

        if user_id:
            mappingDTO.user_id_created = user_id
            mappingDTO.user_id_updated = user_id
        existing_name = ""
        existing_message = f"Mapping with same conditions exists already in database ({existing_name})"

        existing_mappings = match_against if match_against else self._read_repo.get_all()

        if len(existing_mappings) != 0:
            for mapping in existing_mappings:
                if self._maps_content_matches(maps1=mapping.maps, maps2=mappingDTO.maps ):
                    existing_name = mapping.name
                    return existing_message
        try:
            return self._create_filter_mapping(mappingDTO)
        except Exception as e:
            print(f"error creating filter mapping: {str(e)}")
            raise

    def create_filter_mappings_from_dto_list(
        self, mapping_dtos: List[FilterMappingCreateDTO], user_id: Optional[int] = None
    ) -> Optional[List[FilterMappingResponseDTO]]:
        mapping_list = []
        match_against = self._read_repo.get_all()
        existing_mapping_list = []
        failed_mapping_list = []

        for mapping_dto in mapping_dtos:
            try:
                if user_id:
                    mapping_dto.user_id_created = user_id
                    mapping_dto.user_id_updated = user_id

                result = self.create_filter_mapping_from_dto(mapping_dto, match_against=match_against)

                if isinstance(result, FilterMappingResponseDTO):
                    mapping_list.append(result)
                    # Add the new mapping to match_against to prevent duplicates within the batch
                    match_against.append(result)
                else:
                    existing_mapping_list.append(mapping_dto)
            except Exception as e:
                print(f"Error creating mapping: {str(e)}")
                failed_mapping_list.append(mapping_dto)
  
        print(f"Attempting to write {len(mapping_dtos)} mappings to database")
        print(f"Successfully added {len(mapping_list)} new mappings")
        print(f"{len(existing_mapping_list)} mappings already in database that were not updated")
        print(f"{len(failed_mapping_list)} mappings generated an error")
        
        return mapping_list


    def update_filter_mappings_from_dto(
        self, mapping_dto: FilterMappingUpdateDTO, user_id: Optional[int] = None
    ) -> Union[FilterMappingResponseDTO, bool]:

        missing_message = f"mapping does not exists in database: {mapping_dto}"

        if not hasattr(mapping_dto, "id") or mapping_dto.id is None:
            print("Cannot find mapping in database, need the id")
            return False


        existing_mapping = self._read_repo.get_by_id(mapping_dto.id)
        if not existing_mapping:
            print(missing_message)
            return False

        if user_id:
            mapping_dto.user_id_updated = user_id
        try:
            updated_mapping = self._write_repo.update(self._mapper.entity_from_dto(mapping_dto))
            return self._mapper.response_dto_from_entity(updated_mapping)
        except Exception as e:
            print(f"Error updating mapping: {str(e)}")
            return False


    def delete_filter_mapping(self, mapping_id: int) -> bool:
        existing_filter = self.get_filter_mapping_by_id(mapping_id)
        if not existing_filter:
            print(f"mapping {mapping_id} does not exist")
            return False
        try:
            self._write_repo.delete(mapping_id)
            return True
        except:
            return False
