# app/core/application/repositories/role/irole_write_repository.py
from app.core.domain.entities import Role
from app.core.application.repositories.base.iwrite_repository import IWriteRepository

class IRoleWriteRepository(IWriteRepository[Role]):
    pass