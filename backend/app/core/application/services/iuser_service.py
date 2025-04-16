# app/core/application/services/iuser_service.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.application.dtos.user.create_user_dto import CreateUserDTO
from app.core.application.dtos.user.update_user_dto import UpdateUserDTO, UpdateUserSystemDTO, UpdatePasswordDTO
from app.core.application.dtos.user.user_dto import UserDTO, UserProfileDTO, UserDetailDTO

class IUserService(ABC):
    @abstractmethod
    def create_user(self, dto: CreateUserDTO) -> UserDTO:
        """Create a new user from DTO"""
        pass

    @abstractmethod
    def create_user_by_inputs(self, email: str, username: str, password: str, auth_method: str) -> UserDTO:
        """Create a new user from raw inputs"""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[UserDTO]:
        """Get user by ID"""
        pass

    @abstractmethod
    def get_user_profile(self, user_id: int) -> Optional[UserProfileDTO]:
        """Get user profile by ID"""
        pass

    @abstractmethod
    def get_user_detail(self, user_id: int) -> Optional[UserDetailDTO]:
        """Get detailed user information by ID"""
        pass

    @abstractmethod
    def get_user_by_field(self, field: str, value: str) -> Optional[UserDTO]:
        """Get user by a specific field"""
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[UserDTO]:
        """Get user by email"""
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[UserDTO]:
        """Get user by username"""
        pass

    @abstractmethod
    def get_all_users(self) -> List[UserDTO]:
        """Get all users"""
        pass

    @abstractmethod
    def get_user_password(self, user_id: int) -> str:
        pass

    @abstractmethod
    def update_user(self, user_id: int, dto: UpdateUserDTO) -> UserDTO:
        """Update user information"""
        pass

    @abstractmethod
    def update_user_system(self, user_id: int, dto: UpdateUserSystemDTO) -> UserDetailDTO:
        """Update user system information"""
        pass

    @abstractmethod
    def update_password(self, user_id: int, dto: UpdatePasswordDTO) -> None:
        """Update user password"""
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        """Delete user by ID"""
        pass

    @abstractmethod
    def delete_user_by_username(self, username: str) -> None:
        """Delete user by username"""
        pass

    @abstractmethod
    def verify_or_create_user(self, email: str, username: str, password: str, auth_method: str) -> str:
        """Verify if user exists or create new user"""
        pass