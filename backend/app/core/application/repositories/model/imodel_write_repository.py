# app/core/application/repositories/model/imodel_write_repository.py
from app.core.domain.entities import Model
from app.core.application.repositories.base.iwrite_repository import IWriteRepository

class IModelWriteRepository(IWriteRepository[Model]):
    pass