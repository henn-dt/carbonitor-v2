# app/infrastructure/persistence/repositories/base/read_repository.py
from typing import List, Optional, TypeVar, Generic, Type
from sqlalchemy import select
from app.core.application.repositories.base.iread_repository import IReadRepository
from app.infrastructure.persistence.contexts.dbcontext import DBContext

T = TypeVar('T')

class ReadRepository(IReadRepository[T], Generic[T]):
    def __init__(self, db_context: DBContext, entity_type: Type[T]):
        self.db = db_context
        self._entity_type = entity_type

    def get_by_id(self, id: int) -> Optional[T]:
        with self.db.session() as session:
            result = session.execute(
                select(self._entity_type)
                .filter(self._entity_type.id == id)
            )
            return result.scalar_one_or_none()

    def get_all(self) -> List[T]:
        with self.db.session() as session:
            result = session.execute(select(self._entity_type))
            return list(result.scalars().all())

    def filter(self, **kwargs) -> List[T]:
        with self.db.session() as session:
            query = select(self._entity_type)
            for key, value in kwargs.items():
                query = query.filter(getattr(self._entity_type, key) == value)
            result = session.execute(query)
            return list(result.scalars().all())