# app/infrastructure/mappers/user_roles_mapper.py

from app.core.application.dtos.user.user_dto import UserDTO
from app.core.application.dtos.user_roles.user_roles_dto import UserRolesRoleDTO, UserRolesUserDTO
from app.core.application.dtos.role.role_dto import RoleDTO
from app.core.application.mappers.iuser_roles_mapper import IUserRolesMapper

class UserRolesMapper(IUserRolesMapper):
    def user_service_user_to_user_roles_user(self, user_service_dto: UserDTO) -> UserRolesUserDTO:
        return UserRolesUserDTO(
            id = user_service_dto.id,
            username = user_service_dto.username,
            email= user_service_dto.email
        )
    
    def role_service_role_to_user_roles_role(self, role_service_dto: RoleDTO) -> UserRolesRoleDTO:
        return UserRolesRoleDTO(
            id = role_service_dto.id,
            role_name = role_service_dto.name,
            role_permissions = role_service_dto.permissions
        )