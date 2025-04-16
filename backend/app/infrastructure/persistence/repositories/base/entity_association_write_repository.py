# app/infrastructure/persistence/repositories/base/entity_association_read_repository.py
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from app.core.application.repositories.base.iassociation_write_repository import \
    IAssociationWriteRepository
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from sqlalchemy import (BinaryExpression, Table, and_, delete, insert, or_,
                        select, update)
from sqlalchemy.orm import DeclarativeBase

T = TypeVar('T', bound=DeclarativeBase)

class EntityAssociationWriteRepository(IAssociationWriteRepository[T], Generic[T]):
    def __init__(self, db_context: DBContext, entity_class: Type[T], primary_keys: List[str]):
        self.db = db_context
        self._entity = entity_class
        self._primary_keys = primary_keys

    def _build_key_condition(self, key_values: Dict[str, Any]) -> BinaryExpression:
        conditions = []
        for key in key_values:
            if hasattr(self._entity, key):
                if isinstance(key_values[key], list):
                    conditions.append(getattr(self._entity, key).in_(key_values[key]))
                else:
                    conditions.append(getattr(self._entity, key) == key_values[key])
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
                    entity_data = base_values.copy()
                    entity_data[column] = value
                    entity = self._entity(**entity_data)
                    entities.append(entity)
            else:
                for value_dict in values:
                    entity_data = base_values.copy()
                    entity_data.update(value_dict)
                    entity = self._entity(**entity_data)
                    entities.append(entity)

            # Add all entities to the session
            for entity in entities:
                session.add(entity)
            
            # Flush to generate IDs and ensure entities are in the session
            session.flush()
            
            # Refresh entities to ensure all fields are loaded
            for entity in entities:
                session.refresh(entity)
                
            # Commit the transaction
            session.commit()
            
            return entities

    def update_related(
        self,
        column: Union[str, List[str]],
        values: Union[Any, List[Dict[str, Any]]],
        filters: Dict[str, Any]
    ) -> List[T]:
        
        with self.db.session() as session:
            filter_conditions = self._build_key_condition(filters)

            # Fetch entities to update
            query = select(self._entity).where(filter_conditions)
            result = session.execute(query)
            entities = list(result.scalars().all())

            # Apply updates
            for entity in entities:
                if isinstance(column, str):
                    # Single column update
                    setattr(entity, column, values)
                else:
                    # Multi-column update (assuming values is a dict)
                    for col, value in values.items():
                        if hasattr(entity, col):
                            setattr(entity, col, value)

            # Flush changes
            session.flush()
            
            # Commit the transaction
            session.commit()
            
            return entities

    def delete_related(
        self,
        column: Union[str, List[str]],
        values: Union[Any, List[Any]],
        additional_filters: Optional[Dict[str, Any]] = None
    ) -> int:
        
        with self.db.session() as session:
            conditions = []
            # Build conditions based on columns and values
            if isinstance(column, str):
                # Single column scenario
                if isinstance(values, list):
                    conditions.append(getattr(self._entity, column).in_(values))
                else:
                    conditions.append(getattr(self._entity, column) == values)
            else:
                # Multi-column scenario
                for value_dict in values if isinstance(values, list) else [values]:
                    column_conditions = []
                    for col in column:
                        if col in value_dict:
                            column_conditions.append(getattr(self._entity, col) == value_dict[col])
                    if column_conditions:
                        conditions.append(and_(*column_conditions))
            
            # Add additional filters if provided
            if additional_filters:
                for col, value in additional_filters.items():
                    if hasattr(self._entity, col):
                        conditions.append(getattr(self._entity, col) == value)
            
            # Create query with all conditions
            if conditions:
                filter_condition = or_(*conditions)
                
                # Find entities to delete
                query = select(self._entity).where(filter_condition)
                result = session.execute(query)
                entities = list(result.scalars().all())
                
                # Count entities to return deleted count
                count = len(entities)
                
                # Delete entities
                for entity in entities:
                    session.delete(entity)
                
                # Commit the transaction
                session.commit()
                
                return count
            
            return 0
        
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