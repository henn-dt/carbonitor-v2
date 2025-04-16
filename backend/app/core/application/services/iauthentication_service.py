# app/core/application/services/iauthentication_service.py

from abc import ABC, abstractmethod
from typing import Optional, Tuple
from datetime import datetime
from app.core.application.dtos.auth.login_dto import LoginDTO
from app.core.application.dtos.auth.register_dto import RegisterDTO
from app.core.application.dtos.auth.auth_response_dto import AuthResponseDTO

class IAuthenticationService(ABC):
    @abstractmethod
    def register(self, dto: RegisterDTO) -> AuthResponseDTO:
        pass
    
    @abstractmethod
    def login(self, dto: LoginDTO) -> AuthResponseDTO:
        pass
    
    @abstractmethod
    def refresh_token(self, refresh_token: str) -> AuthResponseDTO:
        pass
    
    @abstractmethod
    def logout(self, user_id: int) -> None:
        pass