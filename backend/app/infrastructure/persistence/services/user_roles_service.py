# app/core/application/services/user_roles_service.py

from dataclasses import dataclass
from typing import List, Optional
from app.core.application.services.iuser_roles_service import IUserRolesService
from app.core.application.repositories.user_roles.iuser_roles_read_repository import IUserRolesReadRepository
from app.core.application.repositories.user_roles.iuser_roles_write_repository import IUserRolesWriteRepository
from app.core.application.services.iuser_service import IUserService
from app.core.application.dtos.user_roles.user_roles_dto import UserRolesGetRoleUsersDTO, UserRolesGetUserRolesDTO, UserRolesRoleDTO, UserRolesUserDTO
from app.core.application.dtos.user_roles.create_user_roles_dto import AssignRoleToUserDTO, AssignRolesToUserDTO, AssignUserToRoleDTO, AssignUsersToRoleDTO
from app.core.application.mappers.iuser_roles_mapper import IUserRolesMapper
from app.core.application.services.irole_service import IRoleService

@dataclass
class UserRoleError:
    USER_NOT_FOUND = "User does not exist"
    ROLE_NOT_FOUND = "Role does not exist"
    ROLE_ALREADY_ASSIGNED = "This role is already assigned to the user"
    USER_ALREADY_ASSIGNED = "The user is already assigned this role"

class UserRolesService(IUserRolesService):
    def __init__(
        self,
        user_roles_read_repository: IUserRolesReadRepository,
        user_roles_write_repository: IUserRolesWriteRepository,
        user_service: IUserService,
        role_service: IRoleService,
        user_roles_mapper: IUserRolesMapper,
    ):
        self._user_roles_read = user_roles_read_repository
        self._user_roles_write = user_roles_write_repository
        self._user_service = user_service
        self._role_service = role_service
        self._user_roles_mapper = user_roles_mapper

    # PRIVATE GETTERS
    def _get_user_ids_by_role_id(self, role_id: int) -> List[int]:
        return self._user_roles_read.get_related_values("user_id", {"role_id": role_id})

    def _get_role_ids_by_user_id(self, user_id: int) -> List[int]:
        return self._user_roles_read.get_related_values("role_id", {"user_id": user_id})
        
    def _get_role_by_id(self, role_id: int) -> Optional[UserRolesRoleDTO]:
        role_dto = self._role_service.get_role(role_id)
        return self._user_roles_mapper.role_service_role_to_user_roles_role(role_dto) if role_dto else None

    # PUBLIC GETTERS
    def get_roles_by_user(self, user_dto: UserRolesUserDTO) -> UserRolesGetUserRolesDTO:
        user = self._validate_and_get_user(user_dto)
        role_ids = self._get_role_ids_by_user_id(user.id)
        roles = [self._get_role_from_role_service(UserRolesUserDTO(id=role_id)) for role_id in role_ids]
        # First collect all permissions
        all_permissions = set()
        for role in roles:
            all_permissions.update(role.role_permissions)
        # Optimize permissions by removing specific operations if "all" exists
        optimized_permissions = set()
        resource_all_permissions = {perm.split(':')[0] for perm in all_permissions if perm.endswith(':all')}
        for permission in all_permissions:
            resource, operation = permission.split(':')
            # Only add the permission if:
            # 1. It's an "all" operation, or
            # 2. The resource doesn't have an "all" permission
            if operation == 'all' or resource not in resource_all_permissions:
                optimized_permissions.add(permission)
        return UserRolesGetUserRolesDTO(user=user, roles=roles, permissions=optimized_permissions)

    def get_users_by_role(self, role_dto: UserRolesRoleDTO) -> UserRolesGetRoleUsersDTO:
        role = self._validate_and_get_role(role_dto)
        user_ids = self._get_user_ids_by_role_id(role.id)
        users = [self._get_user_from_user_service(UserRolesRoleDTO(id=user_id)) for user_id in user_ids]
        return UserRolesGetRoleUsersDTO(role=role, users=users)

    # PRIVATE ASSIGN
    def _assign_role_ids_to_user_id(self, user_id: int, role_ids: List[int]) -> None:
        if role_ids:
            self._user_roles_write.create_related(column="role_id", values=role_ids, base_values={"user_id": user_id})

    def _assign_user_ids_to_role_id(self, role_id: int, user_ids: List[int]) -> None:
        if user_ids:
            self._user_roles_write.create_related(column="user_id", values=user_ids, base_values={"role_id": role_id})

    # PUBLIC ASSIGN
    def assign_role_to_user(
            self, assign_dto: AssignRoleToUserDTO,
            raise_error: bool = True, returnNone: bool = False
        ) -> Optional[UserRolesGetUserRolesDTO]:

        user = self._validate_and_get_user(assign_dto.user)
        role = self._validate_and_get_role(assign_dto.role)
        if self._user_roles_read.get_by_keys({"user_id": user.id, "role_id": role.id}):
            if raise_error:
                raise ValueError(UserRoleError.ROLE_ALREADY_ASSIGNED)
            else:
                if returnNone:
                    return None
                return self.get_roles_by_user(user)
        self._assign_role_ids_to_user_id(user.id, [role.id])
        return self.get_roles_by_user(user)

    def verify_or_assign_role_to_user_by_names(self, role_name: str, username: str) -> str:
        user = UserRolesUserDTO(username=username)
        role = UserRolesRoleDTO(role_name=role_name)
        assign_dto = AssignRoleToUserDTO(user=user, role=role)
        if self.assign_role_to_user(assign_dto, False, True):
            return f"User {user.username} is successfully assigned to role {role.role_name}"
        return f"User {user.username} is already assigned to role {role.role_name}"
        

    def assign_roles_to_user(self, assign_dto: AssignRolesToUserDTO) -> UserRolesGetUserRolesDTO:
        user = self._validate_and_get_user(assign_dto.user)
        role_ids = [self._validate_and_get_role(role_dto).id for role_dto in assign_dto.roles]
        existing_role_ids = self._get_role_ids_by_user_id(user.id)
        if existing_role_ids != role_ids:
            self._delete_all_roles_from_user_id(user.id)
            if role_ids:
                self._assign_role_ids_to_user_id(user.id, role_ids)
        return self.get_roles_by_user(user)

    def assign_user_to_role(self, assign_dto: AssignUserToRoleDTO) -> UserRolesGetRoleUsersDTO:
        role = self._validate_and_get_role(assign_dto.role)
        user = self._validate_and_get_user(assign_dto.user)
        if self._user_roles_read.get_by_keys({"role_id": role.id, "user_id": user.id}):
            raise ValueError(UserRoleError.USER_ALREADY_ASSIGNED)
        self._assign_user_ids_to_role_id(role.id, [user.id])
        return self.get_users_by_role(role)

    def assign_users_to_role(self, assign_dto: AssignUsersToRoleDTO) -> UserRolesGetRoleUsersDTO:
        role = self._validate_and_get_role(assign_dto.role)
        user_ids = [self._validate_and_get_user(user_dto).id for user_dto in assign_dto.users]
        existing_user_ids = self._get_user_ids_by_role_id(role.id)
        if existing_user_ids != user_ids:
            self._delete_all_users_from_role_id(role.id)
            if user_ids:
                self._assign_user_ids_to_role_id(role.id, user_ids)
        return self.get_users_by_role(role)

    # DELETE OPERATIONS
    def _delete_all_roles_from_user_id(self, user_id: int) -> int:
        return self._user_roles_write.delete_related(column="user_id", values=user_id)

    def _delete_all_users_from_role_id(self, role_id: int) -> int:
        return self._user_roles_write.delete_related(column="role_id", values=role_id)

    # VALIDATION AND RETRIEVAL
    def _validate_and_get_user(self, user_dto: UserRolesUserDTO) -> UserRolesUserDTO:
        user = self._get_user_from_user_service(user_dto)
        if user is None:
            raise ValueError(UserRoleError.USER_NOT_FOUND)
        return user

    def _validate_and_get_role(self, role_dto: UserRolesRoleDTO) -> UserRolesRoleDTO:
        role = self._get_role_from_role_service(role_dto)
        if role is None:
            raise ValueError(UserRoleError.ROLE_NOT_FOUND)
        return role

    def _get_user_from_user_service(self, user_dto: UserRolesUserDTO) -> Optional[UserRolesUserDTO]:
        if user_dto.id is not None:
            user_dto = self._user_service.get_user_by_id(user_dto.id)
            return self._user_roles_mapper.user_service_user_to_user_roles_user(user_dto)
        if user_dto.username is not None:
            user_dto = self._user_service.get_user_by_username(user_dto.username)
            return self._user_roles_mapper.user_service_user_to_user_roles_user(user_dto)
        if user_dto.email is not None:
            user_dto = self._user_service.get_user_by_email(user_dto.email)
            return self._user_roles_mapper.user_service_user_to_user_roles_user(user_dto)
        return None

    def _get_role_from_role_service(self, role_dto: UserRolesRoleDTO) -> Optional[UserRolesRoleDTO]:
        if role_dto.id is not None:
            return self._get_role_by_id(role_dto.id)
        if role_dto.role_name is not None:
            role_dto = self._role_service.get_role_by_name(role_dto.role_name)
            return self._user_roles_mapper.role_service_role_to_user_roles_role(role_dto)
        return None

    # CHECKER METHODS
    def has_role(self, user_id: int) -> bool:
        return bool(self._user_roles_read.get_related_values("role_id", {"user_id": user_id}))

    def has_user(self, role_id: int) -> bool:
        return bool(self._user_roles_read.get_related_values("user_id", {"role_id": role_id}))