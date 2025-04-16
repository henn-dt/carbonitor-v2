# backend/app/core/application/dtos/product/product_dto.py

from typing import Dict, Optional

from app.core.domain.enums.filter_element_type import FilterElementType
from pydantic import BaseModel, ConfigDict

# for use within a mapping element
class FilterElement(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    Items: dict

"""
{
  "Name": "New Filter",
  "Id": "94c9922c-12a8-4e89-9c11-b442dd695cf9",
  "Items": [
    {
      "PropertyID": "autodesk.revit.parameter:elemCategoryParam",
      "PropertyCaption": "Category",
      "ValueType": "Text",
      "Condition": "Is",
      "FilterValues": [
        {
          "Text": "autodesk.revit.category.local:walls",
          "Caption": "Walls",
          "ValueType": 1
        }
      ]
    },
    {
      "PropertyID": "autodesk.revit.parameter:structuralMaterialParam",
      "PropertyCaption": "Structural Material (Type)",
      "ValueType": "Text",
      "Condition": "BeginsWith",
      "FilterValues": [
        {
          "Text": "STB",
          "Caption": "STB",
          "ValueType": 1
        }
      ]
    }
  ]
}
"""

# for minimal use (make list of products, check identity, etc)
class FilterElementCreateDTO(BaseModel):
    user_id_created: int
    user_id_updated: int
    status: Optional[str] = None
    name: Optional[str] = None
    source: Optional[str] = None
    source_version: Optional[str] = None
    type: Optional[FilterElementType] = None
    filter: dict

    class Config:
        from_attributes = True

class FilterElementResponseDTO(BaseModel):
    id: int
    user_id_created: int
    user_id_updated: int
    status: str
    name: str
    source: str
    source_version: str
    type: str
    filter: dict

    class Config:
        from_attributes = True

class FilterElementUpdateDTO(BaseModel):
    id: int
    user_id_created: Optional[int]
    user_id_updated: int
    status: Optional[str] = None
    name: Optional[str] = None
    source: Optional[str] = None
    source_version: Optional[str] = None
    type: Optional[FilterElementType] = None
    filter: Optional[dict]

    class Config:
        from_attributes = True