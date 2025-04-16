# app/infrastructure/persistence/repositories/buildup/buildup_read_repository.py
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.core.domain.entities import Buildup
from app.core.application.repositories.buildup.ibuildup_read_repository import IBuildupReadRepository
from app.infrastructure.persistence.repositories.base.read_repository import ReadRepository

class BuildupReadRepository(ReadRepository[Buildup], IBuildupReadRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, Buildup)