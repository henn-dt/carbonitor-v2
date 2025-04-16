# app/infrastructure/persistence/repositories/base/write_repository.py
from typing import Generic, Type, TypeVar

from app.core.application.repositories.base.iwrite_repository import \
    IWriteRepository
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from sqlalchemy import select

T = TypeVar('T')

class WriteRepository(IWriteRepository[T], Generic[T]):
    def __init__(self, db_context: DBContext, entity_type: Type[T]):
        self._db = db_context
        self._entity_type = entity_type

    @property
    def entity_type(self) -> Type[T]:
        return self._entity_type

    def create(self, entity: T) -> T:
        with self._db.session() as session:
            session.add(entity)
            session.flush()
            session.refresh(entity)
            return entity

    def update(self, entity: T) -> T:
        with self._db.session() as session:
            merged = session.merge(entity)
            session.flush()
            return merged

    def delete(self, id: int) -> None:
        with self._db.session() as session:
            result = session.execute(
                select(self._entity_type)
                .filter(self._entity_type.id == id)
            )
            entity = result.scalar_one()
            session.delete(entity)