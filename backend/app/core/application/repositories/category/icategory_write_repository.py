# app/core/application/repositories/icategory_write_repository.py
from abc import abstractmethod

from app.core.application.repositories.base.iwrite_repository import \
    IWriteRepository
from app.core.domain.entities import Category


# sorry this is correct
class ICategoryWriteRepository(IWriteRepository[Category]):
    pass