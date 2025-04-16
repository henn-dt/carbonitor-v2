# app/infrastructure/persistence/repositories/filter_mapping/filter_mapping_read_repository.py
from app.infrastructure.persistence.contexts.dbcontext import DBContext

from app.infrastructure.persistence.repositories.base.read_repository import ReadRepository
from app.core.application.repositories.filter_mapping.ifilter_mapping_read_repository import IFilterMappingReadRepository
from app.core.domain.entities.filter_mapping import FilterMapping

class FilterMappingReadRepository(ReadRepository[FilterMapping], IFilterMappingReadRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, FilterMapping)