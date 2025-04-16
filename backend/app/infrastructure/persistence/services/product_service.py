# app/infrastructure/persistence/services/product_service.py
import json
import time
from typing import Collection, List, Optional, Union

from app.core.application.dtos.epdx.epdx_dto import EPD, Conversion, ConversionUnit, ImpactCategoryKey, LifeCycleStage
from app.core.application.dtos.product.product_dto import (Product_DTO,
                                                           ProductDensity_DTO,
                                                           ProductEPD_DTO,
                                                           ProductHeader_DTO)
from app.core.application.mappers.iproduct_mapper import IProductMapper
from app.core.application.repositories.product.iproduct_read_repository import \
    IProductReadRepository
from app.core.application.repositories.product.iproduct_write_repository import \
    IProductWriteRepository
from app.core.application.services.iepdx_service import IEpdxService
from app.core.application.services.iproduct_service import IProductService


class ProductService(IProductService):
    def __init__(
        self,
        product_read_repository: IProductReadRepository,
        product_write_repository: IProductWriteRepository,
        product_mapper : IProductMapper,
        epdx_service: IEpdxService
    ):
        self._read_repo = product_read_repository
        self._write_repo = product_write_repository
        self._product_mapper = product_mapper
        self._epdx_service = epdx_service
        
    

    def _validate_product_dto(self, product_dto : Union[Product_DTO, ProductEPD_DTO]) -> bool: 
        if not hasattr(product_dto, 'epdx'):
            print(f"product dto {product_dto.epd_id} has no attribute epdx")
            return False
        # check if epdx property has valid format
        epdx_data = None
        if isinstance(product_dto.epdx, dict):
            epdx_data = product_dto.epdx
        else:
            print(f"product {product_dto.epd_id} has epdx but is not a dict")
            return False
        # validate epdx data 
        if not self._epdx_service.validate_epdx(epdx_data):
            return False
        # add other validations here
        return True

    def get_impact_from_product_dto(self, 
    impact : ImpactCategoryKey, 
    product_dto : Union[Product_DTO, ProductEPD_DTO], 
    life_cycle_stages : List[LifeCycleStage] = None,
    conversion : Conversion = None,
    conversion_factor : float = 1,    #give the option to just provide a factor, if available. 
    normalize_to : float = 1 ) -> float:
        epd = EPD.model_validate(EPD(**product_dto.epdx))
        return self._epdx_service.get_impact_value_from_EPD(epd, impact, life_cycle_stages, conversion, conversion_factor, normalize_to)


    def get_product_by_dto(self, product_dto : ProductHeader_DTO) ->  Optional[Product_DTO]:
        existing_product_list = self._read_repo.filter(epd_sourceName = product_dto.epd_sourceName, epd_id = product_dto.epd_id, epd_version = product_dto.epd_version)
        if len(existing_product_list) > 0:
            return [self._product_mapper.entity_to_product_dto(existing_product) for existing_product in existing_product_list]
    
    def get_all_products(self) -> List[Product_DTO]:
        entity_list= self._read_repo.get_all()
        return [self._product_mapper.entity_to_product_dto(entity) for entity in entity_list]
    
    def get_product_by_id(self, id: int) -> Optional[Product_DTO]:
        entity = self._read_repo.get_by_id(id)
        return self._product_mapper.entity_to_product_dto(entity)

    def get_product_by_uri(self, uri : str) -> Optional[Product_DTO]:    
        try:
            epd_sourceName, epd_id = uri.split('.')
        except ValueError:
            # Handle the case where the URI is not in the expected format
            print("uri is not formatted as expected - should be <epd_sourceName>.<epd_id>")
            return None

        # Use the filter method to find the product by epd_sourceName and epd_id
        entities = self._read_repo.filter(epd_sourceName=epd_sourceName, epd_id=epd_id)

        # Since the combination is unique, we expect at most one result
        if entities:
            entity = entities[0]
            return self._product_mapper.entity_to_product_dto(entity)
        else:
            return None
    
    def create_product(self, product_dto: Product_DTO) -> Product_DTO:
        if not self._validate_product_dto(product_dto):
            return None
        entity = self._write_repo.create(self._product_mapper.dto_to_product_entity(product_dto))
        return self._product_mapper.entity_to_product_dto(entity)
    

    def create_product_from_dto(self, product_dto : Product_DTO, user_id: Optional[int] = None) -> Product_DTO:
        if user_id:
            product_dto.user_id_created = user_id
            product_dto.user_id_updated = user_id
        existing_message= "Product exists already in database"
        existing_product = self.get_product_by_dto(product_dto)
        if existing_product:
            return existing_message
        if isinstance(existing_product, Collection) and len(existing_product) > 0:  # this shouldn´t be necessary but the response from Filter trips the truthy / falsy condition somehow
            return existing_message
        try:
            return self.create_product(product_dto)
        except Exception as e:
            print(f"error creating product {product_dto.epd_id}: {str(e)}")


    def create_product_from_dto_list(self, product_dtos : list[Product_DTO], user_id: Optional[int] = None) -> list[Product_DTO]:
        start_time = time.perf_counter()
        product_list = []
        existing_product_list = []
        failed_product_list = []
        for dto in product_dtos:
            try:
                if user_id:
                    product = self.create_product_from_dto(dto, user_id)
                else:
                    product = self.create_product_from_dto(dto)
                if product:
                    product_list.append(product)
                else:
                    existing_product_list.append(dto)
            except Exception as e:
                print(f"error creating Product {dto.epd_id} : {e} ")
                failed_product_list.append(dto)
        end_time = time.perf_counter()
        time_diff = end_time - start_time
        minutes = int(time_diff // 60)
        seconds = int(time_diff % 60)
        print(
            f"attempting to write {len(product_dtos)} to database took: {minutes} minutes and {seconds} seconds"
        )
        print(f"successfully added new products: {len(product_list)}")
        print(f"products already in database that were not updated: {len(existing_product_list)}")
        print(f"products that generated an error: {len(failed_product_list)}")
        print(f"failed products: \n {[product.epd_id for product in failed_product_list]}")
    
    def update_product(self, id: int, product_dto: Product_DTO) -> Optional[Product_DTO]:

        existing_product = self._read_repo.get_by_id(id)
        if not existing_product:
            return None           

        if not self._validate_product_dto(product_dto):
            return None
        product_dto.id = id  # Ensure ID matches
        entity = self._write_repo.update(self._product_mapper.dto_to_product_entity(product_dto))
        return self._product_mapper.entity_to_product_dto(entity)
    
    def delete_product(self, id: int) -> bool:
        existing_product = self._read_repo.get_by_id(id)
        if not existing_product:
            return False           
        return self._write_repo.delete(id)