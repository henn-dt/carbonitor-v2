# backend/app/core/application/mappers/ibuildup_mapper.py

from abc import abstractmethod

from app.core.application.dtos.buildup.buildup_dto import BuildupCreate_DTO, BuildupResponse_DTO, BuildupUpdate_DTO, MappedBuildup_DTO
from app.core.domain.entities.buildup import Buildup


class IBuildupMapper():    


    @abstractmethod
    def buildup_entity_from_create_dto(buildup_dto : BuildupCreate_DTO) -> Buildup:
        pass

    @abstractmethod
    def buildup_entity_from_update_dto(buildup_dto : BuildupUpdate_DTO) -> Buildup:
        pass

    @abstractmethod
    def buildup_response_from_entity(buildup : Buildup) -> BuildupResponse_DTO:
        pass

    @abstractmethod
    def mapped_buildup_from_entity(buildup: Buildup) -> MappedBuildup_DTO:
        pass

