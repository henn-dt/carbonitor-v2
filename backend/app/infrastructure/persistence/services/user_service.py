from typing import List, Optional
from app.core.application.dtos.user.create_user_dto import CreateUserDTO
from app.core.application.dtos.user.update_user_dto import UpdateUserDTO, UpdateUserSystemDTO, UpdatePasswordDTO
from app.core.application.dtos.user.user_dto import UserDTO, UserProfileDTO, UserDetailDTO
from app.core.application.repositories.user.iuser_read_repository import IUserReadRepository
from app.core.application.repositories.user.iuser_write_repository import IUserWriteRepository
from app.core.application.mappers.iuser_mapper import IUserMapper
from app.core.application.services.iuser_service import IUserService

class UserService(IUserService):
    def __init__(
        self,user_read_repository: IUserReadRepository, user_write_repository: IUserWriteRepository, user_mapper: IUserMapper
    ):
        self._read_repo = user_read_repository
        self._write_repo = user_write_repository
        self._mapper = user_mapper

    def _check_unique_constraints(self, email: str = None, username: str = None, current_user = None):
        if email and (not current_user or email.lower() != current_user.email):
            if self._read_repo.filter(email=email.lower()):
                raise ValueError("Email already registered")
        if username and (not current_user or username.lower() != current_user.username):
            if self._read_repo.filter(username=username.lower()):
                raise ValueError("Username already taken")

    def _get_user_or_raise(self, user_id: int):
        user = self._read_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    def create_user(self, dto: CreateUserDTO) -> UserDTO:
        self._check_unique_constraints(dto.email, dto.username)
        user = self._mapper.create_dto_to_entity(dto)
        return self._mapper.entity_to_dto(self._write_repo.create(user))

    def create_user_by_inputs(self, email: str, username: str, password: str, auth_method: str) -> UserDTO:
        return self.create_user(CreateUserDTO(email=email, username=username, password=password, auth_method=auth_method))

    def get_user_by_id(self, user_id: int) -> Optional[UserDTO]:
        user = self._read_repo.get_by_id(user_id)
        return self._mapper.entity_to_dto(user) if user else None

    def get_user_profile(self, user_id: int) -> Optional[UserProfileDTO]:
        user = self._read_repo.get_by_id(user_id)
        return self._mapper.entity_to_profile_dto(user) if user else None

    def get_user_detail(self, user_id: int) -> Optional[UserDetailDTO]:
        user = self._read_repo.get_by_id(user_id)
        return self._mapper.entity_to_detail_dto(user) if user else None

    def get_user_by_field(self, field: str, value: str) -> Optional[UserDTO]:
        users = self._read_repo.filter(**{field: value.lower()})
        return self._mapper.entity_to_dto(users[0]) if users else None

    def get_user_by_email(self, email: str) -> Optional[UserDTO]:
        return self.get_user_by_field('email', email)

    def get_user_by_username(self, username: str) -> Optional[UserDTO]:
        return self.get_user_by_field('username', username)

    def get_all_users(self) -> List[UserDTO]:
        return [self._mapper.entity_to_dto(user) for user in self._read_repo.get_all()]
    
    def get_user_password(self, user_id: int) -> str:
        return self._read_repo.get_by_id(user_id).password_hash

    def update_user(self, user_id: int, dto: UpdateUserDTO) -> UserDTO:
        user = self._get_user_or_raise(user_id)
        self._check_unique_constraints(dto.email, dto.username, user)
        updated_user = self._mapper.update_dto_to_entity(user, dto)
        return self._mapper.entity_to_dto(self._write_repo.update(updated_user))

    def update_user_system(self, user_id: int, dto: UpdateUserSystemDTO) -> UserDetailDTO:
        user = self._get_user_or_raise(user_id)
        updated_user = self._mapper.update_system_dto_to_entity(user, dto)
        return self._mapper.entity_to_detail_dto(self._write_repo.update(updated_user))

    def update_password(self, user_id: int, dto: UpdatePasswordDTO) -> None:
        user = self._get_user_or_raise(user_id)
        self._write_repo.update(self._mapper.update_password_dto_to_entity(user, dto))

    def delete_user(self, user_id: int) -> None:
        self._get_user_or_raise(user_id)
        self._write_repo.delete(user_id)

    def delete_user_by_username(self, username: str) -> None:
        user = self.get_user_by_username(username)
        if not user:
            raise ValueError("User not found")
        self._write_repo.delete(user.id)

    def verify_or_create_user(self, email: str, username: str, password: str, auth_method: str) -> str:
        if self.get_user_by_username(username):
            return f"User {username} already exists."
        self.create_user_by_inputs(email, username, password, auth_method)
        return f"User {username} created."