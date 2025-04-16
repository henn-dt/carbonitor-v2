# backend/app/core/application/dtos/product/product_dto.py

from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict


# for minimal use (make list of products, check identity, etc)
class ProductHeader_DTO(BaseModel):
    epd_name: str
    id: Optional[int] = None # if set, the product has been taken from the db
    user_id_created: Optional[int] = None
    user_id_updated: Optional[int] = None
    status: Optional[str] = None
    epd_id: Optional[str] = None
    epd_version: Optional[str] = None
    epd_publishedDate: Optional[str] = None
    epd_validUntil: Optional[str] = None
    epd_standard: Optional[str] = None
    epd_comment: Optional[str] = None
    epd_location: Optional[str] = None
    epd_formatVersion: Optional[str] = None
    epd_sourceName: Optional[str] = None
    epd_sourceUrl: Optional[str] = None
    epd_subtype: Optional[str] = None
    epd_description: Optional[str] = None

    class Config:
        from_attributes = True


# for operations with a product´s physical properties
class ProductDensity_DTO(ProductHeader_DTO):
    epd_declaredUnit: str
    epd_linear_density: Optional[float] = None
    epd_gross_density: Optional[float] = None
    epd_bulk_density: Optional[float] = None
    epd_grammage: Optional[float] = None
    epd_layer_thickness: Optional[float] = None


# to calculate a product´s environmental impact
class Product_DTO(ProductDensity_DTO):
    epdx: Dict


# minimal implementation used by filter mappings
class ProductEPD_DTO(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id : int
    epd_id: str
    epd_sourceName: str
    epd_version: str
    epdx: Dict
    impacts: Dict[str, Dict]
    """
    sample use:
    impacts = {"gwp_fos" : {"a1a3" : 100}}
    """
