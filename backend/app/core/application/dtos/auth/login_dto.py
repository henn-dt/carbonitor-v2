# app/core/application/dtos/auth/login_dto.py

from typing import Optional
from pydantic import BaseModel, EmailStr

class LoginDTO(BaseModel):
    email_or_username: Optional[str]
    password: str