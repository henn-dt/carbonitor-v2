# app/core/application/dtos/user/update_user_dto.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Regular profile updates
class UpdateUserDTO(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(
        None, 
        min_length=3, 
        max_length=50
    )
# Admin-only system updates
class UpdateUserSystemDTO(BaseModel):
    auth_method: Optional[str] = None
    password_hash: Optional[str] = None
    token_revoked: Optional[bool] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    last_login_at: Optional[datetime] = None

# Password change (separate flow)
class UpdatePasswordDTO(BaseModel):
    current_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)