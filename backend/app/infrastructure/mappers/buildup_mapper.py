# backend/app/infrastructure/mappers/buildup_mapper.py



from typing import TypeVar, Union
from app.core.application.dtos.buildup.buildup_dto import ActualSourceForImpactData, BuildupBase_DTO, BuildupCreate_DTO, BuildupResponse_DTO, BuildupUpdate_DTO, MappedBuildup_DTO, ReferenceSourceForImpactData, ReferenceSourceForProduct

from app.core.application.mappers.ibuildup_mapper import IBuildupMapper
from app.core.domain.entities.buildup import Buildup
from app.core.application.services.iproduct_service import IProductService

T = TypeVar ('T', ActualSourceForImpactData, ReferenceSourceForImpactData )

R = TypeVar('R', MappedBuildup_DTO, BuildupResponse_DTO)   # valid responses

class BuildupMapper(IBuildupMapper): 
    def __init__(self, product_service : IProductService):
        self._product_service = product_service   

    def _entity_to_dto(buildup : Buildup, output_dto_type : R) -> Union[R]:
        buildup_data = buildup.to_dict()
        try:          
            return output_dto_type.model_validate(output_dto_type(**buildup_data))
        except Exception as e:
            print(f"Error creating {type(output_dto_type).__name__} object: {str(e)}")
        

    @staticmethod
    def transform_products_in_dto(buildup_dto : BuildupBase_DTO) -> BuildupBase_DTO:
        if not buildup_dto.products:
            return buildup_dto
        
        transformed_products= {}
        for key, product in buildup_dto.products.items():
            if getattr(product, 'type', None) == 'reference' and hasattr(product, 'uri'):
                # Check if impact_data is missing or improperly formatted
                if not hasattr(product, 'impactData') or not product.impactData:
                    # Create proper impactData structure
                    impact_data = {
                        "type": "reference",
                        "uri": product.uri,
                        "overrides": getattr(product, 'overrides', {}),
                        "version": getattr(product, 'version', '1.0')
                    }
                    
                    # Create a new dict for the product with proper structure
                    transformed_product = product.model_dump() if hasattr(product, 'model_dump') else dict(product)
                    transformed_product['impactData'] = impact_data
                    
                    # Create a valid ReferenceSourceForProduct instance
                    transformed_products[key] = ReferenceSourceForProduct.model_validate(transformed_product)
                else:
                    transformed_products[key] = product
            else:
                transformed_products[key] = product   
        buildup_dto.products = transformed_products
        return buildup_dto         


    @staticmethod
    def buildup_entity_from_create_dto(buildup_dto : BuildupCreate_DTO) -> Buildup:

        return Buildup(**buildup_dto.model_dump(exclude_unset=True))

    @staticmethod
    def buildup_entity_from_update_dto(buildup_dto : BuildupUpdate_DTO) -> Buildup:

        return Buildup(**buildup_dto.model_dump(exclude_unset=True))

    @staticmethod
    def buildup_response_from_entity(buildup : Buildup) -> BuildupResponse_DTO:
        return BuildupMapper._entity_to_dto(buildup, BuildupResponse_DTO)

    @staticmethod
    def mapped_buildup_from_entity(buildup: Buildup) -> MappedBuildup_DTO:
        return BuildupMapper._entity_to_dto(buildup, MappedBuildup_DTO)


# def mapping_to_Buildup

