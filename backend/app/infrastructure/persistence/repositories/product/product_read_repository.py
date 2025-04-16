# app/infrastructure/persistence/repositories/product/product_read_repository.py
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.core.domain.entities import Product
from app.core.application.repositories.product.iproduct_read_repository import IProductReadRepository
from app.infrastructure.persistence.repositories.base.read_repository import ReadRepository

class ProductReadRepository(ReadRepository[Product], IProductReadRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, Product)