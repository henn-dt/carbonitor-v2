# app/infrastructure/persistence/repositories/buildup/buildup_write_repository.py
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.core.domain.entities import Buildup
from app.core.application.repositories.buildup.ibuildup_write_repository import IBuildupWriteRepository
from app.infrastructure.persistence.repositories.base.write_repository import WriteRepository

class BuildupWriteRepository(WriteRepository[Buildup], IBuildupWriteRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, Buildup)