# app/core/application/dtos/auth/auth_response_dto.py

from datetime import datetime
from pydantic import BaseModel
from typing import List

class AuthResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    access_token_expires: datetime
    refresh_token_expires: datetime
    user_id: int
    username: str
    email: str
    permissions: List[str]