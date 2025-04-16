# app/core/application/repositories/product/iproduct_write_repository.py
from app.core.application.repositories.base.iwrite_repository import IWriteRepository
from app.core.domain.entities.filter_mapping import FilterMapping

class IFilterMappingWriteRepository(IWriteRepository[FilterMapping]):
    pass