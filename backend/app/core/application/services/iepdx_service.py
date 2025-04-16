from abc import ABC, abstractmethod
from typing import List, Union

from app.core.application.dtos.epdx.epdx_dto import EPD, Conversion, ImpactCategoryKey, LifeCycleStage
from app.core.application.dtos.product.product_dto import Product_DTO


class IEpdxService(ABC):
    
    @abstractmethod
    def get_impact_value_from_EPD(self, 
    product_epd : EPD, 
    impact : ImpactCategoryKey, 
    life_cycle_stages : List[LifeCycleStage] = None,
    conversion : Conversion = None,
    conversion_factor : float = 1,    #give the option to just provide a factor, if available. 
    normalize_to : float = 1   # the buildup or model will pass this along. 
     ) -> float:
        pass

    @abstractmethod
    def validate_epdx(self, dict) -> bool:
        pass

    # epdx to product
    @abstractmethod
    def from_epdx_to_product(self, epdx: EPD) -> Product_DTO:
        pass

    @abstractmethod
    def from_epdx_to_product_list(self, epdx: list[EPD]) -> list[Product_DTO]:
        pass

    # product to epdx
    @abstractmethod
    def from_product_to_epdx(self, product: Product_DTO) -> EPD:
        pass

    @abstractmethod
    def from_product_to_epdx_json(self, product: Product_DTO) -> dict:
        pass
