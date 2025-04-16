# app/infrastructure/persistence/repositories/base/entity_association_write_repository.py
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from app.core.application.repositories.base.iassociation_read_repository import \
    IAssociationReadRepository
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from sqlalchemy import BinaryExpression, Table, and_, select
from sqlalchemy.orm import DeclarativeBase, joinedload

T = TypeVar('T', bound=DeclarativeBase)

class EntityAssociationReadRepository(IAssociationReadRepository[T], Generic[T]):
    def __init__(self, db_context: DBContext, entity_class: Type[T], primary_keys: List[str]):
        self.db = db_context
        self._entity = entity_class
        self._primary_keys = primary_keys

    def _build_key_condition(self, key_values: Dict[str, Any]) -> BinaryExpression:
        conditions = []
        for key in self._primary_keys:
            if hasattr(self._entity, key):
                if isinstance(key_values[key], list):
                    conditions.append(getattr(self._entity, key).in_(key_values[key]))
                else:
                    conditions.append(getattr(self._entity, key) == key_values[key])
        return and_(*conditions)

    def _build_filter_condition(self, key_values: Dict[str, Any]) -> BinaryExpression:
        conditions = []
        for key, value in key_values.items():
            if hasattr(self._entity, key):
                if isinstance(value, list):
                    conditions.append(getattr(self._entity, key).in_(value))
                else:
                    conditions.append(getattr(self._entity, key) == value)
        return and_(*conditions)

    def get_by_id(self, id: int) -> Optional[T]:
        with self.db.session() as session:
            result = session.execute(
                select(self._entity)
                .filter(self._entity.id == id)
            )
            return result.scalar_one_or_none()

    def get_by_keys(self, keys: Dict[str, Any]) -> Optional[T]:
        with self.db.session() as session:
            conditions = self._build_key_condition(keys)
            query = select(self._entity).where(conditions)
            result = session.execute(query)
            return result.scalars().first()

    def get_filtered(self, filters: Dict[str, Any]) -> List[T]:
        with self.db.session() as session:
            conditions = self._build_filter_condition(filters)
            query = select(self._entity).where(conditions)
            result = session.execute(query)
            return list(result.scalars().all())

    def get_related_values(
        self, 
        columns: Union[str, List[str]], 
        filters: Dict[str, Any]
    ) -> List[Union[Any, Dict[str, Any]]]:
        with self.db.session() as session:
            # Handle single or multiple columns
            select_columns = [columns] if isinstance(columns, str) else columns
            selected_cols = [getattr(self._entity, col) for col in select_columns if hasattr(self._entity, col)]
            
            # Build filter conditions
            conditions = self._build_filter_condition(filters)
            
            query = select(*selected_cols).where(conditions)
            result = session.execute(query)
            
            # Return format depends on whether single or multiple columns were requested
            if isinstance(columns, str):
                return list(result.scalars().all())
            return [dict(zip(select_columns, row)) for row in result.all()]
        
# --------------------------------------- USAGE ------------------------------------
# # Single column, single filter
# repo.get_related_values("user_id", {"role_id": 1})
# # Returns: [1, 2, 3]

# # Multiple columns, single filter
# repo.get_related_values(["user_id", "username"], {"role_id": 1})
# # Returns: [{"user_id": 1, "username": "john"}, {"user_id": 2, "username": "jane"}]

# # Multiple columns, multiple filters
# repo.get_related_values(
#     ["user_id", "username"], 
#     {"role_id": 1, "is_active": True}
# )
# # Returns: [{"user_id": 1, "username": "john"}, {"user_id": 2, "username": "jane"}]