# app/infrastructure/persistence/repositories/role/role_read_repository.py
from app.core.application.repositories.role.irole_read_repository import IRoleReadRepository
from app.core.domain.entities.role import Role
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.infrastructure.persistence.repositories.base.read_repository import ReadRepository

class RoleReadRepository(ReadRepository[Role], IRoleReadRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, Role)