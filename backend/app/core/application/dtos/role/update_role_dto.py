# app/core/application/dtos/role/update_role_dto.py
from typing import List, Optional
from pydantic import BaseModel, Field


class UpdateRoleDTO(BaseModel):
    """
    Data Transfer Object for updating an existing role.
    All fields are optional since updates can be partial.
    
    Attributes:
        name: Optional new role name, must be between 1 and 50 characters if provided
        description: Optional new role description, must be less than 255 characters if provided
        permissions: Optional new list of permissions
    """
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    permissions: Optional[List[str]] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "super_admin",
                "description": "Updated administrator role",
                "permissions": ["read", "write", "delete", "manage_users"]
            }
        }