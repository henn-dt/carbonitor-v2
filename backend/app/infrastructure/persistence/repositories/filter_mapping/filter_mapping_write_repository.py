# app/infrastructure/persistence/repositories/filter_mapping/filter_mapping_write_repository.py
from app.infrastructure.persistence.contexts.dbcontext import DBContext

from app.infrastructure.persistence.repositories.base.write_repository import WriteRepository
from app.core.application.repositories.filter_mapping.ifilter_mapping_write_repository import IFilterMappingWriteRepository
from app.core.domain.entities.filter_mapping import FilterMapping

class FilterMappingWriteRepository(WriteRepository[FilterMapping], IFilterMappingWriteRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, FilterMapping)