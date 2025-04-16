# app/core/application/dtos/role_dto.py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class RoleDTO(BaseModel):
    id: int
    name: str
    permissions: List[str] = []

    class Config:
        from_attributes = True

class RoleDetailDTO(RoleDTO):
    """DTO for role data"""
    description: Optional[str] = Field(None, description="Role description")
    created_at: datetime = Field(..., description="Role creation timestamp")
    updated_at: datetime = Field(..., description="Role last update timestamp")

    class Config:
        from_attributes = True