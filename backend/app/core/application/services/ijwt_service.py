# app/core/application/services/ijwt_service.py
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Optional, Tuple

class IJWTService(ABC):
    @abstractmethod
    def create_access_token(self, user_id: int, permissions: list[str], additional_claims: Dict = None) -> Tuple[str, datetime]:
        pass

    @abstractmethod
    def create_refresh_token(self, user_id: int, token_id: str) -> Tuple[str, datetime]:
        pass

    @abstractmethod
    def validate_token(self, token: str, verify_type: Optional[str] = None) -> Dict:
        pass

    @abstractmethod
    def validate_access_token(self, token: str) -> Dict:
        pass

    @abstractmethod
    def validate_refresh_token(self, token: str) -> Dict:
        pass

    @abstractmethod
    def get_token_expiration(self, token: str) -> datetime:
        pass

    @abstractmethod
    def get_user_id_from_token(self, token: str) -> int:
        pass

    @abstractmethod
    def get_token_id(self, token: str) -> Optional[str]:
        pass
    
    @abstractmethod
    def get_permissions_from_token(self, token: str) -> list[str]:
        pass