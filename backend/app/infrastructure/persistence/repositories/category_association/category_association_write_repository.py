# app/infrastructure/persistence/repositories/user_roles/user_roles_write_repository.py

from typing import Any, Dict, List

from app.core.application.repositories.category_association.icategory_association_write_repository import \
    ICategoryAssociationWriteRepository
from app.core.domain.entities.category_association import CategoryAssociation
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.infrastructure.persistence.repositories.base.entity_association_write_repository import \
    EntityAssociationWriteRepository


class CategoryAssociationWriteRepository(EntityAssociationWriteRepository[CategoryAssociation], ICategoryAssociationWriteRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context=db_context, entity_class= CategoryAssociation, primary_keys = ["category_id", "entity_id", "entity_type"])
        
    def associate_entity_with_category(self, entity_id: int, entity_type: str, category_id: int, values: dict = None) -> CategoryAssociation:
        """Associate an entity with a category and optionally set values"""
        association_data = {
            "entity_type": entity_type,
            "category_id": category_id,
        }
        if isinstance(values, dict):
            association_data["values"] = values
        
        result = self.create_related(column= "entity_id", values=entity_id, base_values= association_data)
        return result[0] if result else None
    
    def update_entity_category_values(self, entity_id: int, entity_type: str, category_id: int, values: dict) -> CategoryAssociation:
        """Update the values for an entity-category association"""
        filters = {
            "entity_id": entity_id,
            "entity_type": entity_type,
            "category_id": category_id
        }
        
        result = self.update_related("values", values, filters)
        return result[0] if result else None
    
    def remove_entity_from_category(self, entity_id: int, entity_type: str, category_id: int) -> bool:
        """Remove an entity from a category"""
        filters = {
            "entity_id": entity_id,
            "entity_type": entity_type,
            "category_id": category_id
        }
        
        deleted_count = self.delete_related(self._primary_keys, [filters])
        return deleted_count > 0
    
    def remove_entity_from_all_categories(self, entity_id: int, entity_type: str) -> int:
        """Remove an entity from all categories"""
        filters = {
            "entity_id": entity_id,
            "entity_type": entity_type
        }
        
        return self.delete_related(list(filters.keys()), [filters])
    
    def batch_associate_entity_with_categories(self, entity_id: int, entity_type: str, category_data: List[Dict[str, Any]]) -> List[CategoryAssociation]:
        """
        Associate an entity with multiple categories at once.
        
        Args:
            entity_id: The entity ID
            entity_type: The entity type
            category_data: List of dictionaries containing category_id and values
                Example: [{"category_id": 1, "values": {...}}, {"category_id": 2, "values": {...}}]
        
        Returns:
            List of created CategoryAssociation objects
        """
        entities = []
        for data in category_data:
            entity_data = {
                "entity_id": entity_id,
                "entity_type": entity_type,
                "category_id": data["category_id"],
                "values": data.get("values", {})
            }
            entities.append(entity_data)
        
        return self.create_related(None, entities, {})
