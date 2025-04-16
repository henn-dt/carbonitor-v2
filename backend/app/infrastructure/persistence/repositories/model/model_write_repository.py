# app/infrastructure/persistence/repositories/model/model_write_repository.py
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.core.domain.entities import Model
from app.core.application.repositories.model.imodel_write_repository import IModelWriteRepository
from app.infrastructure.persistence.repositories.base.write_repository import WriteRepository

class ModelWriteRepository(WriteRepository[Model], IModelWriteRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, Model)