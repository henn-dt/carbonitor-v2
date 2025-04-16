#backend/app/infrastructure/persistence/services/buildup_service.py

from typing import Collection, List, Optional, TypeVar, Union

from app.core.application.dtos.buildup.buildup_dto import BuildupCreate_DTO, BuildupResponse_DTO, BuildupUpdate_DTO, MappedBuildup_DTO
from app.core.application.mappers.ibuildup_mapper import IBuildupMapper
from app.core.application.repositories.buildup.ibuildup_read_repository import IBuildupReadRepository
from app.core.application.repositories.buildup.ibuildup_write_repository import IBuildupWriteRepository
from app.core.application.services.ibuildup_service import IBuildupService
from app.core.application.services.iproduct_service import IProductService


T = TypeVar ('T', BuildupResponse_DTO, BuildupCreate_DTO, BuildupUpdate_DTO, MappedBuildup_DTO)

class BuildupService(IBuildupService):
    def __init__(
        self,
        buildup_read_repository: IBuildupReadRepository,
        buildup_write_repository: IBuildupWriteRepository,
        buildup_mapper : IBuildupMapper,
        product_service : IProductService
    ):
        self._read_repo = buildup_read_repository
        self._write_repo = buildup_write_repository
        self._mapper = buildup_mapper
        self._product_service = product_service

    def _validate_buildup(self, buildup_dto : Union[BuildupCreate_DTO, BuildupUpdate_DTO]):
        # insert buildup validation logic here

        # validate products
        if not hasattr(buildup_dto, "products"):
            # no products to validate
            return True
        if isinstance(buildup_dto.products, Collection) and len(buildup_dto.products) == 0:
            return True

        #products_reference_sources = set(value for key, value in buildup_dto.products.items())
        # get products, depending if they are references or actuals

        # all products should have same standard

        # all products should have valid epdx

        # all products should have valid date
        return True

    def get_impact_from_buildup_dto(self, buildup_dto : Union[BuildupResponse_DTO, MappedBuildup_DTO]):
        pass

    def get_all_buildups(self) -> Optional[List[BuildupResponse_DTO]] :
        entity_list= self._read_repo.get_all()
        return [self._mapper.buildup_response_from_entity(entity) for entity in entity_list]

    def get_buildup_by_name(self, name : str) -> Optional[BuildupResponse_DTO]:
        entities = self._read_repo.filter(name=name)
        if entities:           
            return [self._mapper.buildup_response_from_entity(entity) for entity in entities]
        else:
            return None     

    def get_buildup_by_name_status(self, buildup_dto : T) -> Optional[BuildupResponse_DTO]:
        error = "buildup is not formatted as expected - should have name and status properties"
        if not buildup_dto.name or not buildup_dto.status:
            print(error)
            return None
        try:
            name = buildup_dto.name
            status = buildup_dto.status
        except ValueError:
            # Handle the case where the buildup doesn´t have the values
            print(error)
            return None

        entities = self._read_repo.filter(name=name, status=status)
        # Since the combination is unique, we expect at most one result
        if entities:
            entity = entities[0]
            return self._mapper.buildup_response_from_entity(entity)
        else:
            return None        

    def _create_buildup(self, buildup_dto : BuildupCreate_DTO):
        if not self._validate_buildup(buildup_dto):
            return None
        entity = self._write_repo.create(self._mapper.buildup_entity_from_create_dto(buildup_dto))
        return self._mapper.buildup_response_from_entity(entity)

    def create_buildup_from_dto(self, buildup_dto : BuildupCreate_DTO, user_id : Optional[int] = None) -> BuildupResponse_DTO:
        if user_id:
            buildup_dto.user_id_created = user_id
            buildup_dto.user_id_updated = user_id
        existing_message= "Buildup exists already in database"
        existing_buildup = self.get_buildup_by_name_status(buildup_dto)
        if existing_buildup:
            return existing_message
        if isinstance(existing_buildup, Collection) and len(existing_buildup) > 0:  # this shouldn´t be necessary but the response from Filter trips the truthy / falsy condition somehow
            return existing_message
        try:
            return self._create_buildup(buildup_dto)
        except Exception as e:
            print(f"error creating buildup {buildup_dto.name}: {str(e)}")
   
    def get_buildup_by_id(self, id: int):
        entity = self._read_repo.get_by_id(id)
        return self._mapper.buildup_response_from_entity(entity)

    def update_buildup(self, id : int, buildup_dto : BuildupUpdate_DTO) -> BuildupResponse_DTO:
        existing_buildup = self._read_repo.get_by_id(id)
        if not existing_buildup:
            return None           

        if not self._validate_buildup(buildup_dto):
            return None
        buildup_dto.id = id  # Ensure ID matches
        entity = self._write_repo.update(self._mapper.buildup_entity_from_update_dto(buildup_dto))
        return self._mapper.buildup_response_from_entity(entity)
    

    def delete_buildup(self, id : int) -> bool:
        existing_buildup = self._read_repo.get_by_id(id)
        if not existing_buildup:
            return False           
        return self._write_repo.delete(id)

