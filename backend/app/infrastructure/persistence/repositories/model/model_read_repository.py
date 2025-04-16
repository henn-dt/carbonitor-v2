# app/infrastructure/persistence/repositories/model/model_read_repository.py
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.core.domain.entities import Model
from app.core.application.repositories.model.imodel_read_repository import IModelReadRepository
from app.infrastructure.persistence.repositories.base.read_repository import ReadRepository

class ModelReadRepository(ReadRepository[Model], IModelReadRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, Model)