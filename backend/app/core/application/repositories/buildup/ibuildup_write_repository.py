# app/core/application/repositories/buildup/ibuildup_write_repository.py
from app.core.domain.entities import Buildup
from app.core.application.repositories.base.iwrite_repository import IWriteRepository

class IBuildupWriteRepository(IWriteRepository[Buildup]):
    pass