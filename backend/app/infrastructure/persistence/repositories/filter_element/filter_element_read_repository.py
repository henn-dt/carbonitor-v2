# app/infrastructure/persistence/repositories/filter_element/filter_element_read_repository.py
from typing import List, Optional
from app.infrastructure.persistence.contexts.dbcontext import DBContext

from app.infrastructure.persistence.repositories.base.read_repository import ReadRepository
from app.core.application.repositories.filter_element.ifilter_element_read_repository import IFilterElementReadRepository
from app.core.domain.entities.filter_element import FilterElement
from sqlalchemy import select

class FilterElementReadRepository(ReadRepository[FilterElement], IFilterElementReadRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, FilterElement)

    def get_by_filter_conditions(self, conditions : dict) -> Optional[List[FilterElement]]:
         with self.db.session() as session:
            result = session.execute(
                select(FilterElement).filter(
                    FilterElement.filter == conditions
                )
            )
            return result.scalar_one_or_none()      