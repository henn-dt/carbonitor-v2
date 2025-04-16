# app/core/application/repositories/filter_element/ifilter_element_read_repository.py
from abc import abstractmethod
from typing import List, Optional
from app.core.application.repositories.base.iread_repository import IReadRepository
from app.core.domain.entities.filter_element import FilterElement

class IFilterElementReadRepository(IReadRepository[FilterElement]):
    
    @abstractmethod
    def get_by_filter_conditions(self, conditions : dict) -> Optional[List[FilterElement]]:
        pass
     