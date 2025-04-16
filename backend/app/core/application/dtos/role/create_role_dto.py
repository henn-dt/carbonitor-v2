# app/core/application/dtos/role/create_role_dto.py
from typing import Optional, List
from pydantic import BaseModel, Field

class CreateRoleDTO(BaseModel):
    """
    Data Transfer Object for creating a new role.
    
    Attributes:
        name: Role name, must be between 1 and 50 characters
        description: Optional role description, must be less than 255 characters
        permissions: Optional list of permissions
    """
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    permissions: Optional[List[str]] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "admin",
                "description": "Administrator role with full access",
                "permissions": ["read", "write", "delete"]
            }
        }