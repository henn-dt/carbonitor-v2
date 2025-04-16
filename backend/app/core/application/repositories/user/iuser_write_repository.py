# app/core/application/repositories/user/iuser_write_repository.py
from app.core.domain.entities import User
from app.core.application.repositories.base.iwrite_repository import IWriteRepository

class IUserWriteRepository(IWriteRepository[User]):
    pass