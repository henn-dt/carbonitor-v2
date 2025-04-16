# app/infrastructure/persistence/repositories/user/user_read_repository.py
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.core.domain.entities import User
from app.core.application.repositories.user.iuser_read_repository import IUserReadRepository
from app.infrastructure.persistence.repositories.base.read_repository import ReadRepository

class UserReadRepository(ReadRepository[User], IUserReadRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, User)