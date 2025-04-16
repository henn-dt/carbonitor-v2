# app/core/application/repositories/product/iproduct_write_repository.py
from app.core.domain.entities import Product
from app.core.application.repositories.base.iwrite_repository import IWriteRepository

class IProductWriteRepository(IWriteRepository[Product]):
    pass