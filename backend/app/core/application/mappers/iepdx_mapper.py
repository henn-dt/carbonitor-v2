#backend/app/core/application/mappers/iepdx_mapper.py

from abc import ABC, abstractmethod

from app.core.application.dtos.epdx.epdx_dto import EPD
from app.core.application.dtos.product.product_dto import (Product_DTO,
                                                           ProductDensity_DTO,
                                                           ProductHeader_DTO)


class IEpdxMapper:
    ### deserialiser methods
    @abstractmethod
    def to_epdx(product: Product_DTO) -> EPD:
        pass
 
    @abstractmethod
    def to_epdx_json(epd: EPD) -> str:
        pass

    #### serializer methods
    @abstractmethod
    def to_product_header(epd: EPD) -> ProductHeader_DTO:
       pass

    @abstractmethod
    def to_product_stats(epd: EPD) -> ProductDensity_DTO:
        pass
      
    @abstractmethod
    def to_product_epd(epd: EPD) -> Product_DTO:
        pass