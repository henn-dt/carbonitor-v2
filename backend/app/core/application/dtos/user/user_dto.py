# app/core/application/dtos/user/user_dto.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# For minimal user info (most common usage)
class UserDTO(BaseModel):
    id: int
    email: EmailStr
    username: str
    class Config:
        from_attributes = True

# For profile/settings pages
class UserProfileDTO(UserDTO):
    is_verified: bool
    is_active: bool

# For admin views or detailed user info
class UserDetailDTO(UserProfileDTO):
    auth_method: str
    last_login_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime