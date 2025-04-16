# app/core/application/repositories/role/irole_read_repository.py
from app.core.domain.entities import Role
from app.core.application.repositories.base.iread_repository import IReadRepository

class IRoleReadRepository(IReadRepository[Role]):
    pass