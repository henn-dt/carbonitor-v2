# app/infrastructure/persistence/repositories/product/product_write_repository.py
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.core.domain.entities import Product
from app.core.application.repositories.product.iproduct_write_repository import IProductWriteRepository
from app.infrastructure.persistence.repositories.base.write_repository import WriteRepository

class ProductWriteRepository(WriteRepository[Product], IProductWriteRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, Product)