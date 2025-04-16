# app/core/application/services/ipassword_service.py
from abc import ABC, abstractmethod

class IPasswordService(ABC):
    @abstractmethod
    def hash_password(self, plain_password: str) -> str:
        """Hash a plain text password"""
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain text password against a hash"""
        pass