# app/infrastructure/persistence/repositories/user/user_write_repository.py
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.core.domain.entities import User
from app.core.application.repositories.user.iuser_write_repository import IUserWriteRepository
from app.infrastructure.persistence.repositories.base.write_repository import WriteRepository

class UserWriteRepository(WriteRepository[User], IUserWriteRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, User)