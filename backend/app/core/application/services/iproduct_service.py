# app/core/application/services/iproduct_service.py
from abc import ABC, abstractmethod
from typing import List, Optional, Union

from app.core.application.dtos.product.product_dto import (Product_DTO, ProductEPD_DTO,
                                                           ProductHeader_DTO)
from app.core.domain.entities import Product
from app.core.application.dtos.epdx.epdx_dto import Conversion, ImpactCategoryKey, LifeCycleStage


class IProductService(ABC):
    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass
    
    @abstractmethod
    def get_product_by_id(self, id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def get_product_by_uri(self, uri : str) -> Optional[Product]:
        pass

    @abstractmethod    
    def get_impact_from_product_dto(self, 
    impact : ImpactCategoryKey, 
    product_dto : Union[Product_DTO, ProductEPD_DTO], 
    life_cycle_stages : List[LifeCycleStage],
    conversion : Conversion,
    conversion_factor : float,    
    normalize_to : float) -> float:
        pass

    @abstractmethod
    def create_product(self, product: Product) -> Product:
        pass
    

    @abstractmethod
    def create_product_from_dto(self, product_dto : ProductHeader_DTO, user_id: Optional[int] = None) -> Product:
        pass
    
    @abstractmethod
    def create_product_from_dto_list(self, product_dtos : list[ProductHeader_DTO], user_id: Optional[int] = None) -> list[Product]:
        pass

    @abstractmethod
    def update_product(self, id: int, product: Product) -> Optional[Product]:
        pass
    
    @abstractmethod
    def delete_product(self, id: int) -> bool:
        pass