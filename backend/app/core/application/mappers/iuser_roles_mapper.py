# app/infrastructure/mappers/dto_dto_mappers/iuser_roles_mapper.py

from abc import ABC, abstractmethod
from app.core.application.dtos.user.user_dto import UserDTO
from app.core.application.dtos.user_roles.user_roles_dto import UserRolesRoleDTO, UserRolesUserDTO
from app.core.application.dtos.role.role_dto import RoleDTO

class IUserRolesMapper(ABC):
    @abstractmethod
    def user_service_user_to_user_roles_user(self, user_service_dto: UserDTO) -> UserRolesUserDTO:
        pass

    @abstractmethod
    def role_service_role_to_user_roles_role(self, role_service_dto: RoleDTO) -> UserRolesRoleDTO:
        pass