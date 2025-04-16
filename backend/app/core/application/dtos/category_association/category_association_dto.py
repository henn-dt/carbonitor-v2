from typing import Any, Dict, List, Optional

from app.core.application.dtos.category.category_dto import CategoryResponseDTO
from app.core.domain.enums.category_entity_type import CategoryEntityType
from pydantic import (BaseModel, ConfigDict, EmailStr, Field, ValidationInfo,
                      field_validator)


class AssociationEntityDTO(BaseModel):
    entity_id: int
    entity_type: CategoryEntityType
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class CategoryAssociationDTO(AssociationEntityDTO):
    category_id: int
    values: Optional[Dict[str, Any]]   # property_id : property_value, so that property value can be accessed with entity.values[property_id]

class CategoryAssociationUpdateDTO(CategoryAssociationDTO):
    id : int
    # Allow partial updates
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        extra='ignore',  # Ignore extra fields
    )

class CategoryAssociationResponseDTO(CategoryAssociationDTO):
    id : int

class CategoryAssociationCategoryDTO(CategoryAssociationResponseDTO):
    category : CategoryResponseDTO