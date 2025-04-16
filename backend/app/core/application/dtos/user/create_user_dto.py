# app/core/application/dtos/user/create_user_dto.py
from pydantic import BaseModel, EmailStr, Field

class CreateUserDTO(BaseModel):
    email: EmailStr = Field(
        ...,  # required
        description="User's email address"
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="User's password (min 8 characters)"
    )
    auth_method: str = Field(
        default="local",
        pattern="^(local|azure|microsoft)$"
    )
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=True)