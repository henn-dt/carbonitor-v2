# app/core/application/repositories/user/iuser_read_repository.py
from app.core.domain.entities import User
from app.core.application.repositories.base.iread_repository import IReadRepository

class IUserReadRepository(IReadRepository[User]):
    pass