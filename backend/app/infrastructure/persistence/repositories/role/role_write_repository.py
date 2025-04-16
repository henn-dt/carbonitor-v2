# app/infrastructure/persistence/repositories/role/role_write_repository.py
from app.core.application.repositories.role.irole_write_repository import IRoleWriteRepository
from app.core.domain.entities.role import Role
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.infrastructure.persistence.repositories.base.write_repository import WriteRepository

class RoleWriteRepository(WriteRepository[Role], IRoleWriteRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, Role)