

from abc import ABC, abstractmethod
from typing import List, Optional, Union

from app.core.application.dtos.buildup.buildup_dto import BuildupBase_DTO, BuildupCreate_DTO, BuildupResponse_DTO, BuildupUpdate_DTO, MappedBuildup_DTO

class IBuildupService(ABC):

    @abstractmethod
    def get_impact_from_buildup_dto(self, buildup_dto : Union[BuildupResponse_DTO, MappedBuildup_DTO]):
        pass

    @abstractmethod
    def get_all_buildups(self) -> Optional[List[BuildupResponse_DTO]] :
        pass

    @abstractmethod
    def get_buildup_by_name_status(self, buildup_dto : BuildupBase_DTO) -> Optional[BuildupResponse_DTO]:
        pass       

    @abstractmethod
    def get_buildup_by_name(self, name : str) -> Optional[BuildupResponse_DTO]:
        pass     

    @abstractmethod
    def create_buildup_from_dto(self, buildup_dto : BuildupCreate_DTO, user_id : Optional[int] = None) -> BuildupResponse_DTO:
        pass
   
    @abstractmethod   
    def get_buildup_by_id(self, id: int):
        pass

    @abstractmethod
    def update_buildup(self, id : int, buildup_dto : BuildupUpdate_DTO) -> BuildupResponse_DTO:
        pass
    
    @abstractmethod
    def delete_buildup(self, id : int) -> bool:
        pass