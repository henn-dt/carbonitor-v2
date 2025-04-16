from pydantic import BaseModel, EmailStr, Field, ValidationInfo, field_validator
from typing import Optional, List

class UserRolesUserDTO(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class UserRolesRoleDTO(BaseModel):
    id: Optional[int] = None
    role_name: Optional[str] = None
    role_permissions: List[str] = Field(default_factory=list)

class UserRolesGetUserRolesDTO(BaseModel):
    user: UserRolesUserDTO
    roles: Optional[List[UserRolesRoleDTO]] = Field(default_factory=list)
    permissions: Optional[List[str]] = Field(default_factory=list)

class UserRolesGetRoleUsersDTO(BaseModel):
    role: UserRolesRoleDTO
    users: Optional[List[UserRolesUserDTO]] = []