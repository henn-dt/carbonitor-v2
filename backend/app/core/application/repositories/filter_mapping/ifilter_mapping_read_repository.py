# app/core/application/repositories/filter_mapping/ifilter_mapping_read_repository.py
from abc import abstractmethod
from typing import List, Optional
from app.core.application.repositories.base.iread_repository import IReadRepository
from app.core.domain.entities.filter_mapping import FilterMapping

class IFilterMappingReadRepository(IReadRepository[FilterMapping]):
    pass
     