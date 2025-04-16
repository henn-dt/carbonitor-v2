# app/core/application/repositories/category_association/icategory_association_read_repository.py
from abc import abstractmethod
from typing import Any, Dict, List, Optional

from app.core.application.repositories.base.iassociation_read_repository import \
    IAssociationReadRepository
from app.core.domain.entities.category_association import CategoryAssociation


class ICategoryAssociationReadRepository(IAssociationReadRepository[CategoryAssociation]):

    @abstractmethod
    def get_by_id(self, association_id: int) -> CategoryAssociation:
        pass

    @abstractmethod
    def get_by_entity(self, entity_type: str, entity_id: int) -> List[CategoryAssociation]:
        pass
    
    @abstractmethod
    def get_by_category(self, category_id: int, entity_type: Optional[str] = None) -> List[CategoryAssociation]:
        pass
    
    @abstractmethod
    def get_values_for_entity(self, entity_type: str, entity_id: int, category_id: Optional[int] = None) -> Dict[int, Dict]:
        pass
    
    @abstractmethod
    def get_category_properties_for_entity(self, product_id: int, category_id: Optional[int] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_entity_list_by_category_properties(self, category_ids: List[int] = None, filters: Dict[str, Dict[str, Any]] = None) -> Dict[int, Dict[int, Dict]]:
        pass