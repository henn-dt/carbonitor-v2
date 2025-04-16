# app/infrastructure/persistence/repositories/category/category_write_repository.py
from app.core.application.repositories.category.icategory_write_repository import \
    ICategoryWriteRepository
from app.core.domain.entities import Category
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.infrastructure.persistence.repositories.base.write_repository import \
    WriteRepository


class CategoryWriteRepository(WriteRepository[Category], ICategoryWriteRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, Category)