# app/core/application/dtos/category/category_dto.py

import json
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from app.core.domain.enums.category_entity_type import CategoryEntityType
from app.core.domain.enums.category_property_format import \
    CategoryPropertyFormat
from pydantic import BaseModel, ConfigDict, field_validator


class CategoryPropertySchema(BaseModel):
    name: str  # display name, so we can change it without messing with mapping
    description: Optional[str] = None
    format: CategoryPropertyFormat = CategoryPropertyFormat.STRING
    default : Optional[Any] = None
    required: Optional[bool] = False
    enum: Optional[List[Any]] = None # list of allowed values

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, extra='allow' )

class CategoryProperty(CategoryPropertySchema):
    id : str  # make this unique by adding the parent category id to property own id like category_id_property_id

class CategoryDTO(BaseModel):   
    name: str
    type: CategoryEntityType
    user_id_created: Optional[int] = None
    user_id_updated: Optional[int] = None
    status: Optional[str] = None
    description: Optional[str]  = None
    property_schema : Optional[Dict[str, CategoryPropertySchema]]  = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    @field_validator("property_schema", mode="before")
    @classmethod
    def parse_property_schema(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v

# DTO for updating an existing category
class CategoryUpdateDTO(CategoryDTO):
    """DTO for updating an existing category"""
    id: int
    # Allow partial updates
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        extra='ignore',  # Ignore extra fields
    )

class CategoryResponseDTO(CategoryDTO):
    """DTO for returning a category"""
    id: int
    type: str
    property_schema : Optional[Dict[str, Union[Dict, CategoryPropertySchema]]]
    
    # Flat representation of properties for UI consumption    
    @property
    def properties(self) -> List[Dict[str, Any]]:
        """Returns properties in a flat list format for UI consumption"""
        if not self.property_schema:
            return []
            
        result = []
        for id, props in self.property_schema.items():
            try:
                if isinstance(props, dict):
                    props = CategoryPropertySchema(**props)
                result.append(
                {
                    "id" : id,
                    "name": props.name,
                    "format": props.format,
                    "description": props.description,
                    "default": props.default,
                    "required": props.required,
                    "enum" : props.enum  
                })
            except Exception as e:
                # Handle validation errors
                print(f"Error processing property {id}: {str(e)}")
                # Add a minimal representation to avoid breaking the UI
                result.append({
                    "id": id,
                    "name": f"Property {id} (error)",
                    "format": CategoryPropertyFormat.STRING,
                    "description": f"Error: {str(e)}",
                    "default": None,
                    "required": False,
                    "enum": None
                })
        return result

    model_config = ConfigDict(
        from_attributes=True, 
        populate_by_name=True,
        json_encoders={CategoryPropertySchema: lambda v: v.model_dump()}  # Add custom encoder
    )

"""example use

# Creating a category
category_data = {
    "name": "Size",
    "type": "product",
    "description": "Product size options",
    "property_schema": {
        "00000": {
            "name" : "size",
            "format": "string",
            "enum": ["S", "M", "L", "XL"],
            "description": "Size code"
        },
        "000001": {
            "name": "dimensions"
            "type": "object",
            "description": "Physical dimensions"
        }
    }
}

create_dto = CategoryDTO(**category_data)

# Creating from Properties list format
category_data_with_list = {
    "name": "Color",
    "type": "product",
    "property_schema": [
        {   "id" : 00001
            "name": "color",
            "type": "string",
            "enum": ["Red", "Blue", "Green"]
        },
        { property_2...}
    ]
}

create_dto_from_list = CategoryCreate(**category_data_with_list)

# entity mapper are straightforward, because of property names:
category_entity = Category(CategoryDTO.model_dump())
)

# Converting entity to response DTO
response_dto = CategoryResponse.model_validate(category_entity.to_dict())

"""