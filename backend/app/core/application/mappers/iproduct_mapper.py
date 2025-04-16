# backend/app/core/application/mappers/iproduct_mapper.py
from abc import ABC, abstractmethod

from app.core.application.dtos.product.product_dto import (Product_DTO,
                                                           ProductDensity_DTO,
                                                           ProductHeader_DTO)
from app.core.domain.entities.product import Product


class IProductMapper():
    @abstractmethod
    def dto_to_product_entity(product_dto : ProductHeader_DTO) -> Product:
        pass

    @abstractmethod
    def entity_to_product_dto(product : Product) -> Product_DTO: 
        pass

    @abstractmethod
    def entity_to_product_header_dto(product : Product) -> ProductHeader_DTO:  
        pass
