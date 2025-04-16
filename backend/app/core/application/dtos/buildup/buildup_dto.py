#backend/app/core/application/dtos/buildup/buildup_dto.py

from typing import Any, Dict, List, Optional, Union
from app.core.application.dtos.epdx.epdx_dto import EPD, Classification, ReferenceSourceForAssembly1, ReferenceSourceForProduct1, ReferenceSourceForProduct2, Type2, Type4, Type6, Unit

from pydantic import BaseModel, ConfigDict, Field

# i replicated the basemodels here for ease of reference. Can be swapped forthe reference and made syntetic. overriden properties are listed first and marked

class ActualSourceForImpactData(EPD):  #this is ReferenceSourceForImpactDataSource1
    model_config = ConfigDict(
        populate_by_name=True,
    )
    type: Type4   # means actual



class ReferenceSourceForImpactData(BaseModel):  # this is ReferenceSourceForImpactDataSource3
    model_config = ConfigDict(
        populate_by_name=True,
    )
    format: Optional[str] = None
    overrides: Optional[Dict[str, Any]] = None
    type: Type6    # means reference
    uri: str       # id of the references product: guid + source
    version: Optional[str] = None

class ReferenceSourceForProduct(ReferenceSourceForProduct2):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    # impact_data: Union[ActualSourceForImpactData, ReferenceSourceForImpactData] = Field(..., alias="impactData")    #changed from original base model for easier naming

class ActualSourceForProduct():
    model_config = ConfigDict(
    populate_by_name=True,
    )

class BuildupBase_DTO(ReferenceSourceForAssembly1):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    user_id_created: Optional[int] = None
    user_id_updated: Optional[int] = None
    status: Optional[str] = None
    id: int
    products: Dict[str, Union[ReferenceSourceForProduct, ActualSourceForImpactData]]   #changed from original base model for easier naming



class BuildupCreate_DTO(BuildupBase_DTO):
    model_config = ConfigDict(
        populate_by_name=True
    )
    id : None = None


class BuildupUpdate_DTO(BuildupBase_DTO):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        extra='ignore',  # Ignore extra fields
    )
    id: int
    classification: Optional[List[Classification]] = None
    comment: Optional[str] = None
    description: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = Field(None, alias="metaData")     # we store mapping id in meta_data, "mapping_name" : "str", "mapping_id" : "str"
    name: Optional[str]
    products: Optional[Dict[str, Union[ReferenceSourceForProduct, ActualSourceForImpactData]]]
    quantity: Optional[float]
    results: Optional[Dict[str, Any]] = None   #here come the impacts values
    type: Optional[Type2] = Type2.actual
    unit: Optional[Unit]


class BuildupResponse_DTO(BuildupBase_DTO):
    model_config = ConfigDict(
        populate_by_name=True
    )
    classification: Optional[List[Dict]] = None
    products: Dict[str, Dict]  
    type: str = "actual"
    unit: str


class MappedBuildup_DTO(BaseModel):   # base implementation for use in model mappings
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id : int
    name: str
    status: str
    products: Dict[str, Dict]
    quantity: float

# todo:
# def product_to_sourceForImpactData (actual or reference)
# def filter_to_ReferenceSourceForProduct
# def mapping_to_Buildup