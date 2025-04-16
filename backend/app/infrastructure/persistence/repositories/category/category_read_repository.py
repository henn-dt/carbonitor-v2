# app/infrastructure/persistence/repositories/category/category_read_repository.py
from typing import List, Optional

from app.core.application.repositories.category.icategory_read_repository import \
    ICategoryReadRepository
from app.core.domain.entities import Category
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.infrastructure.persistence.repositories.base.read_repository import \
    ReadRepository
from sqlalchemy import select


class CategoryReadRepository(ReadRepository[Category], ICategoryReadRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, Category)

    def get_by_name_and_type(self, name: str, type: str) -> Optional[Category]:
        """Get a category by its name and type."""        
        with self.db.session() as session:
            result = session.execute(
                select(Category).filter(
                    Category.name == name,
                    Category.type == type
                )
            )
            return result.scalar_one_or_none()


    def exists_by_name_and_type(self, name: str, type: str) -> bool:
        """Check if a category with the given name and type exists."""
        with self.db.session() as session:
            result = session.execute(
                select(Category).filter(
                    Category.name == name,
                    Category.type == type
                )
            )
            return result.scalar_one_or_none() is not None