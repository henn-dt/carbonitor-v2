# app/core/application/services/iuser_roles_service.py
from abc import ABC, abstractmethod
from app.core.application.dtos.user_roles.user_roles_dto import UserRolesGetRoleUsersDTO, UserRolesGetUserRolesDTO, UserRolesRoleDTO, UserRolesUserDTO
from app.core.application.dtos.user_roles.create_user_roles_dto import AssignRoleToUserDTO, AssignRolesToUserDTO, AssignUserToRoleDTO, AssignUsersToRoleDTO

class IUserRolesService(ABC):
    @abstractmethod
    def get_roles_by_user(self, user_dto: UserRolesUserDTO) -> UserRolesGetUserRolesDTO:
        pass

    @abstractmethod        
    def get_users_by_role(self, role_dto: UserRolesRoleDTO) -> UserRolesGetRoleUsersDTO:
        pass

    @abstractmethod
    def assign_role_to_user(self, assign_dto: AssignRoleToUserDTO, raise_error: bool = True, returnNone: bool = False) -> UserRolesGetUserRolesDTO:
        pass

    @abstractmethod
    def verify_or_assign_role_to_user_by_names(self, role_name: str, username: str) -> str:
        pass
    
    @abstractmethod
    def assign_roles_to_user(self, assign_dto: AssignRolesToUserDTO) -> UserRolesGetUserRolesDTO:
        pass

    @abstractmethod
    def assign_user_to_role(self, assign_dto: AssignUserToRoleDTO) -> UserRolesGetRoleUsersDTO:
        pass

    @abstractmethod
    def assign_users_to_role(self, assign_dto: AssignUsersToRoleDTO) -> UserRolesGetRoleUsersDTO:
        pass

    @abstractmethod
    def has_role(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def has_user(self, role_id: int) -> bool:
        pass