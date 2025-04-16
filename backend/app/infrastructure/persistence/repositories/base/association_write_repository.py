# app/infrastructure/persistence/repositories/base/association_read_repository.py
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from sqlalchemy import BinaryExpression, Table, and_, delete, insert, select, update, or_
from app.core.application.repositories.base.iassociation_write_repository import IAssociationWriteRepository
from app.infrastructure.persistence.contexts.dbcontext import DBContext
T = TypeVar('T')

class AssociationWriteRepository(IAssociationWriteRepository[T], Generic[T]):
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

    def create_related(
        self,
        column: Union[str, List[str]],
        values: Union[Any, List[Dict[str, Any]]],
        base_values: Dict[str, Any]
    ) -> List[T]:
        
        with self.db.session() as session:
            entities = []
            if isinstance(column, str):
                for value in values if isinstance(values, list) else [values]:
                    entity = base_values.copy()
                    entity[column] = value
                    entities.append(entity)
            else:
                for value_dict in values:
                    entity = base_values.copy()
                    entity.update(value_dict)
                    entities.append(entity)
            stmt = insert(self._table).values(entities)
            session.execute(stmt)
            session.commit()
            conditions = []
            for entity in entities:
                conditions.append(self._build_key_condition(entity))
            query = select(self._table).where(or_(*conditions))
            created = session.execute(query).all()
            return [dict(row._mapping) for row in created]

    def update_related(
        self,
        column: Union[str, List[str]],
        values: Union[Any, List[Dict[str, Any]]],
        filters: Dict[str, Any]
    ) -> List[T]:
        
        with self.db.session() as session:
            filter_conditions = []
            for col, value in filters.items():
                filter_conditions.append(getattr(self._table.c, col) == value)
            if isinstance(column, str):
                update_values = {column: values}
            else:
                update_values = values
            stmt = (
                update(self._table)
                .where(and_(*filter_conditions))
                .values(**update_values)
            )
            session.execute(stmt)
            query = select(self._table).where(and_(*filter_conditions))
            updated = session.execute(query).all()
            updated_records = [dict(row._mapping) for row in updated]
            session.commit()
            return updated_records

    def delete_related(
        self,
        column: Union[str, List[str]],
        values: Union[Any, List[Any]],
        additional_filters: Optional[Dict[str, Any]] = None
    ) -> int:
        
        with self.db.session() as session:
            conditions = []
            if isinstance(column, str):
                if isinstance(values, list):
                    conditions.append(getattr(self._table.c, column).in_(values))
                else:
                    conditions.append(getattr(self._table.c, column) == values)
            else:
                for value_dict in values if isinstance(values, list) else [values]:
                    column_conditions = []
                    for col in column:
                        if col in value_dict:
                            column_conditions.append(
                                getattr(self._table.c, col) == value_dict[col]
                            )
                    conditions.append(and_(*column_conditions))
            if additional_filters:
                for col, value in additional_filters.items():
                    conditions.append(getattr(self._table.c, col) == value)
            stmt = delete(self._table).where(or_(*conditions))
            result = session.execute(stmt)
            session.commit()
            return result.rowcount
        
# ---------------------------------- USAGE ------------------------------------------------
# # Single column operations
# # Create roles for a user
# repo.create_related(
#     column="role_id",
#     values=[456, 457, 458],
#     base_values={
#         "user_id": 123,
#         "organization_id": 789
#     }
# )

# # Update role status
# repo.update_related(
#     column="is_active",
#     values=False,
#     filters={
#         "user_id": 123,
#         "organization_id": 789
#     }
# )

# # Delete specific roles
# repo.delete_related(
#     column="role_id",
#     values=[456, 457],
#     additional_filters={"organization_id": 789}
# )

# # Multiple column operations
# # Create multiple role assignments with different attributes
# repo.create_related(
#     column=["role_id", "is_active", "assigned_by"],
#     values=[
#         {"role_id": 456, "is_active": True, "assigned_by": "admin"},
#         {"role_id": 457, "is_active": False, "assigned_by": "system"}
#     ],
#     base_values={"user_id": 123, "organization_id": 789}
# )

# # Update multiple columns
# repo.update_related(
#     column=["is_active", "updated_at"],
#     values={"is_active": False, "updated_at": datetime.now()},
#     filters={"organization_id": 789}
# )

# # Delete based on multiple columns
# repo.delete_related(
#     column=["role_id", "organization_id"],
#     values=[
#         {"role_id": 456, "organization_id": 789},
#         {"role_id": 457, "organization_id": 790}
#     ]
# )