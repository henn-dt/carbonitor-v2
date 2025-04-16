# app/core/application/repositories/product/iproduct_read_repository.py
from app.core.domain.entities import Product
from app.core.application.repositories.base.iread_repository import IReadRepository

class IProductReadRepository(IReadRepository[Product]):
    pass