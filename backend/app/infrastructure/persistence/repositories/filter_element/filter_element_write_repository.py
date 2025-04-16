# app/infrastructure/persistence/repositories/filter_element/filter_element_write_repository.py
from app.infrastructure.persistence.contexts.dbcontext import DBContext

from app.infrastructure.persistence.repositories.base.write_repository import WriteRepository
from app.core.application.repositories.filter_element.ifilter_element_write_repository import IFilterElementWriteRepository
from app.core.domain.entities.filter_element import FilterElement

class FilterElementWriteRepository(WriteRepository[FilterElement], IFilterElementWriteRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, FilterElement)