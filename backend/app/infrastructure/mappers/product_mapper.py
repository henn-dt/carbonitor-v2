# backend/app/infrastructure/mappers/product_mapper.py

import json
from typing import TypeVar, Union

from app.core.application.dtos.epdx.epdx_dto import EPD
from app.core.application.dtos.product.product_dto import (Product_DTO,
                                                           ProductDensity_DTO,
                                                           ProductEPD_DTO,
                                                           ProductHeader_DTO)
from app.core.application.mappers.iproduct_mapper import IProductMapper
from app.core.domain.entities.product import Product
from app.core.domain.enums.default_impacts import DefaultImpacts

T = TypeVar ('T', Product_DTO, ProductEPD_DTO, ProductHeader_DTO, ProductDensity_DTO)
# perfect!
class ProductMapper(IProductMapper):

    def _create_dto_from_entity(product : Product, output_dto_type : T) -> T:
        product_data = product.to_dict()

        if output_dto_type == ProductEPD_DTO:    #leave the logic or create custom mapper? 
            product_data["impacts"] = {impact_key: product_data['epdx']['impacts'].get(impact_key) 
                              for impact_key in DefaultImpacts 
                              if impact_key in product_data['epdx']['impacts']}
        try:          
            return output_dto_type.model_validate(output_dto_type(**product_data))
        except Exception as e:
            print(f"Error creating {type(output_dto_type).__name__} object: {str(e)}")


    @staticmethod
    def dto_to_product_entity(product_dto : ProductHeader_DTO) -> Product:
        return Product(**product_dto.model_dump(exclude_unset=True))

    @staticmethod
    def entity_to_product_dto(product : Product) -> Product_DTO:  
        return ProductMapper._create_dto_from_entity(product, Product_DTO)

    @staticmethod
    def entity_to_product_header_dto(product : Product) -> ProductHeader_DTO:  
        return ProductMapper._create_dto_from_entity(product, ProductHeader_DTO)

    @staticmethod
    def entity_to_product_density_dto(product : Product) -> ProductDensity_DTO:  
        return ProductMapper._create_dto_from_entity(product, ProductDensity_DTO)

    @staticmethod
    def entity_to_product_epdx_dto(product : Product) -> ProductEPD_DTO:  
        return ProductMapper._create_dto_from_entity(product, ProductEPD_DTO)