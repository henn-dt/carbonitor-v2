# backend/app/core/application/dtos/model_mapping.py/model_mapping.py

from typing import Dict, List, Optional, Union

from app.core.domain.enums.filter_element_type import FilterElementType
from app.core.application.dtos.filter_element.filter_element_dto import FilterElement
from app.core.application.dtos.product.product_dto import ProductEPD_DTO
from app.core.application.dtos.buildup.buildup_dto import MappedBuildup_DTO
from pydantic import BaseModel, ConfigDict

class MappedProduct(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    uri: str    # source.epd_id    
    quantity: float
    impact_data: ProductEPD_DTO


class FilterElementToProduct(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    id: str    # id of this mapping element
    name: str   # name of this mapping element
    filter: FilterElement # serialized filter from the plugin
    impact_data : List[MappedProduct] 


class MappedBuildup(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    id: str
    quantity: float
    impact_data: MappedBuildup_DTO

class FilterElementToBuildup(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: str
    name : str   # name of this mapping element
    filter: FilterElement # serialized filter from the plugin with all its properties, including id and name
    impact_data : List[MappedBuildup]

class FilterMappingCreateDTO(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    user_id_created: int
    user_id_updated: int
    status: str
    name: str
    source: str
    source_version: str
    type: FilterElementType
    maps: Optional[Dict[str, Union[FilterElementToProduct, FilterElementToBuildup]]] = None

class FilterMappingUpdateDTO(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    id: int
    user_id_created: Optional[int]
    user_id_updated: int
    status: Optional[str]
    name: Optional[str]
    source: Optional[str]
    source_version: Optional[str]
    type: Optional[FilterElementType]
    maps: Optional[Dict[str, Union[FilterElementToProduct, FilterElementToBuildup]]] = None


class FilterMappingResponseDTO(FilterMappingCreateDTO):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: int
    user_id_created: Optional[int]
    user_id_updated: int
    status: Optional[str]
    name: Optional[str]
    source: Optional[str]
    source_version: Optional[str]
    type: str
    maps: Optional[Dict[str, Union[FilterElementToProduct, FilterElementToBuildup]]] = None