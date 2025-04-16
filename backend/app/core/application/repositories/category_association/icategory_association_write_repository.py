# app/core/application/repositories/category_association/icategory_association_write_repository.py
from abc import abstractmethod
from typing import Any, Dict, List

from app.core.application.repositories.base.iassociation_write_repository import \
    IAssociationWriteRepository
from app.core.domain.entities.category_association import CategoryAssociation


class ICategoryAssociationWriteRepository(IAssociationWriteRepository[CategoryAssociation]):

    @abstractmethod   
    def associate_entity_with_category(self, entity_id: int, entity_type: str, category_id: int, values: dict = None) -> CategoryAssociation:
        pass
        
    @abstractmethod       
    def update_entity_category_values(self, entity_id: int, entity_type: str, category_id: int, values: dict) -> CategoryAssociation:
        pass

    @abstractmethod    
    def remove_entity_from_category(self, entity_id: int, entity_type: str, category_id: int) -> bool:
        pass

    @abstractmethod
    def remove_entity_from_all_categories(self, entity_id: int, entity_type: str) -> int:
        pass

    @abstractmethod
    def batch_associate_entity_with_categories(self, entity_id: int, entity_type: str, category_data: List[Dict[str, Any]]) -> List[CategoryAssociation]:
        pass
