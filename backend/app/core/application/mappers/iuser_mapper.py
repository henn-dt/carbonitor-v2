# app/core/application/mappers/dto_entitiy_mappers/iuser_mapper.py
from abc import ABC, abstractmethod

from app.core.application.dtos.user.create_user_dto import CreateUserDTO
from app.core.application.dtos.user.update_user_dto import UpdatePasswordDTO, UpdateUserDTO, UpdateUserSystemDTO
from app.core.application.dtos.user.user_dto import UserDTO, UserDetailDTO, UserProfileDTO
from app.core.domain.entities.user import User

class IUserMapper(ABC):
    @abstractmethod
    def create_dto_to_entity(self, dto: CreateUserDTO) -> User:
        pass

    @abstractmethod
    def update_dto_to_entity(self, user: User, dto: UpdateUserDTO) -> User:
        pass

    @abstractmethod
    def update_system_dto_to_entity(self, user: User, dto: UpdateUserSystemDTO) -> User:
        pass

    @abstractmethod
    def update_password_dto_to_entity(self, user: User, dto: UpdatePasswordDTO) -> User:
        pass

    @abstractmethod
    def entity_to_dto(self, user: User) -> UserDTO:
        pass

    @abstractmethod
    def entity_to_profile_dto(self, user: User) -> UserProfileDTO:
        pass

    @abstractmethod
    def entity_to_detail_dto(self, user: User) -> UserDetailDTO:
        pass