# app/core/application/repositories/model/imodel_read_repository.py
from app.core.domain.entities import Model
from app.core.application.repositories.base.iread_repository import IReadRepository

class IModelReadRepository(IReadRepository[Model]):
    pass