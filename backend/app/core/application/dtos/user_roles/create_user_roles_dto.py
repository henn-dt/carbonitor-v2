# app/core/application/dtos/user_roles/create_user_roles_dto.py

from typing import List
from pydantic import BaseModel
from app.core.application.dtos.user_roles.user_roles_dto import UserRolesRoleDTO, UserRolesUserDTO

class AssignRoleToUserDTO(BaseModel):
    user: UserRolesUserDTO
    role: UserRolesRoleDTO

class AssignRolesToUserDTO(BaseModel):
    user: UserRolesUserDTO
    roles: List[UserRolesRoleDTO]

class AssignUserToRoleDTO(BaseModel):
    role: UserRolesRoleDTO
    user: UserRolesUserDTO

class AssignUsersToRoleDTO(BaseModel):
    role: UserRolesRoleDTO
    users: List[UserRolesUserDTO]