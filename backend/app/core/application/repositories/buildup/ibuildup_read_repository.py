# app/core/application/repositories/buildup/ibuildup_read_repository.py
from app.core.domain.entities import Buildup
from app.core.application.repositories.base.iread_repository import IReadRepository

class IBuildupReadRepository(IReadRepository[Buildup]):
    pass