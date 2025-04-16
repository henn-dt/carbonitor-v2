# app/infrastructure/persistence/repositories/category_association/category_association_read_repository.py

from typing import Any, Dict, List, Optional

from app.core.application.repositories.category_association.icategory_association_read_repository import \
    ICategoryAssociationReadRepository
from app.core.domain.entities.category import \
    Category  # I need this to read the properties out of the relationship
from app.core.domain.entities.category_association import CategoryAssociation
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.infrastructure.persistence.repositories.base.entity_association_read_repository import \
    EntityAssociationReadRepository
from sqlalchemy import select
from sqlalchemy.orm import defer, joinedload, noload


class CategoryAssociationReadRepository(EntityAssociationReadRepository[CategoryAssociation], ICategoryAssociationReadRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context = db_context, 
                        entity_class = CategoryAssociation, 
                        primary_keys = ["category_id", "entity_id", "entity_type"])

    def get_by_id(self, id: int) -> CategoryAssociation:
        with self.db.session() as session:
            result = session.execute(
                select(self._entity)
                .options(joinedload(self._entity.category))  # eager loading
                .filter(self._entity.id == id)
            )
            return result.scalar_one_or_none()

                        
    def get_by_entity(self, entity_type: str, entity_id: int) -> List[CategoryAssociation]:
        """Get all categories association for a specific entity."""
        filters = {
            "entity_type": entity_type,
            "entity_id": entity_id
        }
        with self.db.session() as session:
            result = session.execute(
                select(self._entity)
                .options(joinedload(self._entity.category))  # eager loading
                .where(self._build_filter_condition(filters))
            )
            return list(result.scalars().all())
    
    def get_by_category(self, category_id: int, entity_type: str) -> List[CategoryAssociation]:
        """Get all associations of a specific type associated with a category."""
        filters = {"category_id": category_id,
                    "entity_type" : entity_type}

        with self.db.session() as session:
            result = session.execute(
                select(self._entity)
                .options(joinedload(self._entity.category))  # eager loading
                .where(self._build_filter_condition(filters))
            )
            return list(result.scalars().all())
    


    def get_values_for_entity(self, entity_type: str, entity_id: int, category_id: Optional[int] = None) -> Dict[int, Dict]:
        """Get the values for a specific entity, optionally filtered by category."""
        filters = {
            "entity_type": entity_type,
            "entity_id": entity_id
        }
        if category_id:
            filters["category_id"] = category_id
            
        with self.db.session() as session:
            query = select(self._entity.category_id, self._entity.values).where(self._build_key_condition(filters))
            result = session.execute(query)
            return {row[0]: row[1] for row in result.all() if row[1] is not None}

    # here we get a bit fancy
    def get_category_properties_for_entity(self, product_id: int, category_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get category properties with entity-specific values for a given entity.
        
        Args:
            product_id: The ID of the product
            category_id: Optional category ID to filter by a specific category. not needed if entity : category mapping is 1:1 as we want
            to implement for products, but maybe we need one day. 
            
        Returns:
            List of dictionaries containing category info and property values, structured as:
            [
                {
                    "category_id": 1,
                    "category_name": "Size",
                    "property_schema": {...},  # The schema from the category
                    "values": {...}            # The specific values for this product
                },
                ...
            ]
        """
        with self.db.session() as session:
            # Build the query to join Category and CategoryAssociation
            query = (
                select(Category, CategoryAssociation.values)
                .join(
                    CategoryAssociation,
                    (Category.id == CategoryAssociation.category_id) &
                    (CategoryAssociation.entity_id == product_id) &
                    (CategoryAssociation.entity_type == 'product')
                )
            )
            
            # Add category filter if provided
            if category_id is not None:
                query = query.where(Category.id == category_id)
            
            result = session.execute(query)
            
            # Format the results
            property_data = []
            for row in result:
                category, values = row
                
                property_data.append({
                    "category_id": category.id,
                    "category_name": category.name,
                    "category_type": category.type,
                    "category_description": category.description,
                    "property_schema": category.property_schema,
                    "values": values
                })
                
            return property_data   

    def get_entity_list_by_category_properties(self, 
                                         category_ids: List[int] = None, # setup to work on multiple categories - if e.g. we have shared properties, like "cost"
                                         filters: Dict[str, Dict[str, Any]] = None) -> Dict[int, Dict[int, Dict]]:
        """
        Find entities that have a specific property value in a category.
        
        Args:
            category_id: The category ID to search in
            filters: Optional dictionary of filters in the format:
                {category_id: {property_name: property_value}}
            
        Returns:
            Dictionary mapping entity IDs to their category values:
            {
                    entity_id: {
                    category_id: {property values},
                    ...
                },
                ...
            }
        """
        with self.db.session() as session:
            query = select(
                CategoryAssociation.entity_id,
                CategoryAssociation.category_id,
                CategoryAssociation.values
            )

            # Apply category filters if provided
            if category_ids:
                query = query.where(CategoryAssociation.category_id.in_(category_ids))

            result = session.execute(query)

            # Group results by entity
            entity_data = {}
            for entity_id, category_id, values in result:
                if entity_id not in entity_data:
                    entity_data[entity_id] = {}
                entity_data[entity_id][category_id] = values

            # Apply property filters if provided
            if filters:
                filtered_entities = {}
                for entity_id, categories in entity_data.items():
                    match = True
                    for category_id, properties in filters.items():
                        if (category_id not in categories or 
                            not all(categories[category_id].get(prop) == value 
                                   for prop, value in properties.items())):
                            match = False
                            break
                    if match:
                        filtered_entities[entity_id] = categories
                return filtered_entities

            return entity_data