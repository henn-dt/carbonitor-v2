# app/core/application/repositories/icategory_read_repository.py
from abc import abstractmethod
from typing import Optional

from app.core.application.repositories.base.iread_repository import \
    IReadRepository
from app.core.domain.entities import Category


class ICategoryReadRepository(IReadRepository[Category]):

    @abstractmethod
    def get_by_name_and_type(self, name: str, type: str) -> Optional[Category]:
        pass

    @abstractmethod
    def exists_by_name_and_type(self, name: str, type: str) -> bool:
        pass