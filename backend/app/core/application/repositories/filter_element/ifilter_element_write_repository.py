# app/core/application/repositories/product/iproduct_write_repository.py
from app.core.application.repositories.base.iwrite_repository import IWriteRepository
from app.core.domain.entities.filter_element import FilterElement

class IFilterElementWriteRepository(IWriteRepository[FilterElement]):
    pass