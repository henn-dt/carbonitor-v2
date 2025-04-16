# app/infrastructure/persistence/repositories/base/association_write_repository.py
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from sqlalchemy import BinaryExpression, Table, and_, select
from app.core.application.repositories.base.iassociation_read_repository import IAssociationReadRepository
from app.infrastructure.persistence.contexts.dbcontext import DBContext


T = TypeVar('T')

class AssociationReadRepository(IAssociationReadRepository[T], Generic[T]):
    def __init__(self, db_context: DBContext, association_table: Table, primary_keys: List[str]):
        self.db = db_context
        self._table = association_table
        self._primary_keys = primary_keys

    def _build_key_condition(self, key_values: Dict[str, Any]) -> BinaryExpression:
        conditions = []
        for key in self._primary_keys:
            if key in key_values:
                conditions.append(getattr(self._table.c, key) == key_values[key])
        return and_(*conditions)

    def get_by_keys(self, keys: Dict[str, Any]) -> Optional[T]:
        with self.db.session() as session:
            query = select(self._table).where(self._build_key_condition(keys))
            result = session.execute(query)
            row = result.first()
            return dict(row._mapping) if row else None

    def get_filtered(self, filters: Dict[str, Any]) -> List[T]:
        with self.db.session() as session:
            query = select(self._table).where(self._build_key_condition(filters))
            result = session.execute(query)
            return [dict(row._mapping) for row in result.all()]

    def get_related_values(
        self, 
        columns: Union[str, List[str]], 
        filters: Dict[str, Any]
    ) -> List[Union[Any, Dict[str, Any]]]:
        with self.db.session() as session:
            # Handle single or multiple columns
            select_columns = [columns] if isinstance(columns, str) else columns
            selected_cols = [getattr(self._table.c, col) for col in select_columns]
            
            # Build filter conditions
            conditions = []
            for col, value in filters.items():
                conditions.append(getattr(self._table.c, col) == value)
            
            query = select(*selected_cols).where(and_(*conditions))
            result = session.execute(query)
            
            # Return format depends on whether single or multiple columns were requested
            if isinstance(columns, str):
                return [row[0] for row in result.all()]
            return [dict(zip(select_columns, row)) for row in result.all()]
        
    def get_by_id(self, id: int) -> Optional[T]:
        with self.db.session() as session:
            result = session.execute(
                select(self._entity)
                .filter(self._entity.id == id)
            )
            return result.scalar_one_or_none()
        
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