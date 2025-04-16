from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UpdateUserViewModel(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_-]+$"
    )

class UpdateUserSystemViewModel(BaseModel):
    auth_method: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    last_login_at: Optional[datetime] = None

class UpdatePasswordViewModel(BaseModel):
    current_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)