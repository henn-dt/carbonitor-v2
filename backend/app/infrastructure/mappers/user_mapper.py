# app/infrastructure/mappers/user_mapper.py

from app.core.application.dtos.user.create_user_dto import CreateUserDTO
from app.core.application.dtos.user.update_user_dto import UpdatePasswordDTO, UpdateUserDTO, UpdateUserSystemDTO
from app.core.application.dtos.user.user_dto import UserDTO, UserDetailDTO, UserProfileDTO
from app.core.application.mappers.iuser_mapper import IUserMapper
from app.core.application.services.ipassword_service import IPasswordService
from app.core.domain.entities.user import User


class UserMapper(IUserMapper):
    def __init__(self, password_service: IPasswordService):
        self._password_service = password_service
    
    def create_dto_to_entity(self, dto: CreateUserDTO) -> User:
        """Maps CreateUserDTO to User entity"""
        return User(
            email=dto.email.lower(),
            username=dto.username.lower(),
            password_hash=self._password_service.hash_password(dto.password),
            auth_method=dto.auth_method,
            is_active=dto.is_active,
            is_verified=dto.is_verified,
            token_revoked=False,
            last_login_at=None,
            last_token_issued=None
        )

    def update_dto_to_entity(self, user: User, dto: UpdateUserDTO) -> User:
        """Maps UpdateUserDTO to existing User entity"""
        if dto.username is not None:
            user.username = dto.username.lower()
        if dto.email is not None:
            user.email = dto.email.lower()
        return user

    def update_system_dto_to_entity(self, user: User, dto: UpdateUserSystemDTO) -> User:
        """Maps UpdateUserSystemDTO to existing User entity"""
        if dto.is_verified is not None:
            user.is_verified = dto.is_verified
        if dto.is_active is not None:
            user.is_active = dto.is_active
        if dto.auth_method is not None:
            user.auth_method = dto.auth_method
        if dto.last_login_at is not None:
            user.last_login_at = dto.last_login_at
        if dto.token_revoked is not None:
            user.token_revoked = dto.token_revoked
        return user

    def update_password_dto_to_entity(self, user: User, dto: UpdatePasswordDTO) -> User:
        """Maps UpdatePasswordDTO to existing User entity"""
        if not dto.current_password or not dto.new_password:
            raise ValueError("new password or current password string is empty")
        
        if not self._password_service.verify_password(dto.current_password, user.password_hash):
            raise ValueError("Current password is incorrect")
        
        if dto.current_password == dto.new_password:
            raise ValueError("New password must be different from current password")
        
        if len(dto.new_password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        user.password_hash = self._password_service.hash_password(dto.new_password)
        user.token_revoked = True  # Revoke all tokens after password change
        return user

    def entity_to_dto(self, user: User) -> UserDTO:
        """Maps User entity to UserDTO"""
        return UserDTO(
            id=user.id,
            email=user.email,
            username=user.username
        )

    def entity_to_profile_dto(self, user: User) -> UserProfileDTO:
        """Maps User entity to UserProfileDTO"""
        return UserProfileDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            is_verified=user.is_verified,
            is_active=user.is_active
        )

    def entity_to_detail_dto(self, user: User) -> UserDetailDTO:
        """Maps User entity to UserDetailDTO"""
        return UserDetailDTO(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            is_verified=user.is_verified,
            auth_method=user.auth_method,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

