# app/core/application/dtos/auth/register_dto.py

from pydantic import BaseModel, EmailStr, Field

class RegisterDTO(BaseModel):
    email: EmailStr
    username: str = Field(
        min_length=3,
        max_length=50
    )
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)