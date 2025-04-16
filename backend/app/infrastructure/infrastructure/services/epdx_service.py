# app/infrastructure/infrastructure/okobau_service.py
import time
from typing import List, Union

from app.core.application.dtos.epdx.epdx_dto import EPD, Conversion, ConversionUnit, ImpactCategoryKey, LifeCycleStage, Unit
from app.core.application.dtos.product.product_dto import (Product_DTO,
                                                           ProductDensity_DTO, ProductEPD_DTO,
                                                           ProductHeader_DTO)
from app.core.application.mappers.iepdx_mapper import IEpdxMapper
from app.core.application.services.iepdx_service import IEpdxService


class EpdxService(IEpdxService):
    def __init__(self, mapper = IEpdxMapper):
        self._mapper = mapper

    def validate_epdx(self, dict) -> bool:
        try:
            EPD.model_validate(EPD(**dict))
            return True
        except Exception as e:
            print(str(e))
            return False

    def get_impact_value_from_EPD(self, 
    product_epd : EPD, 
    impact : ImpactCategoryKey, 
    life_cycle_stages : List[LifeCycleStage] = None,
    conversion : Conversion = None,
    conversion_factor : float = 1,    #give the option to just provide a factor, if available. 
    normalize_to : float = 1   # the buildup or model will pass this along. 
     ) -> float:

        if not hasattr(product_epd.impacts, impact.value):
            print(f"epd has no impact {impact}")
            return None

        result = 0
        impact_indicator = product_epd.impacts[impact.value]

        # If specific life cycle stages are provided, filter the impacts
        if life_cycle_stages:
            filtered_impacts = {stage: impact_indicator.get(stage, {}) for stage in life_cycle_stages}
        else:
            filtered_impacts = impact_indicator
        
        impact_value = sum(value for key, value in filtered_impacts)

        if impact_value is None:
            return result

        # Apply conversion if needed
        if conversion:
            # Assuming a conversion method exists to convert the value
            declared_unit = product_epd.declared_unit
            impact_value = self._convert_impact_value(impact_value, declared_unit, conversion)
        
        # Apply conversion factor:
        impact_value = impact_value * conversion_factor
        # Normalize the value
        impact_value = impact_value / normalize_to
        # Set to result
        result = impact_value

        return result

    def _convert_impact_value(self, value: float, declared_unit : Unit, conversion: Conversion) -> float:
        """
        Convert a value from one unit to another based on the conversion configuration.
    
        Args:
            value: The value to convert
            declared_unit: The original unit of the value
            convert_to: The conversion configuration containing target unit and metadata
    
         Returns:
             float: The converted value
         """
        if value == 0 or conversion.value == 0:
            return 0.0
        try:
            # If units are the same, no conversion needed
            if declared_unit == conversion.to and conversion.value == 1:
                return value

            # Handle specific unit conversions
            if declared_unit == Unit.tones and conversion.to == Unit.kg:
                value = value * 1000  # 1 tonne = 1000 kg

            elif declared_unit == Unit.km and conversion.to == Unit.m:
                value = value * 1000

            elif conversion.meta_data:
                if conversion.meta_data.unit == ConversionUnit.KG_PER_M3.value:
                    if declared_unit == Unit.kg and conversion.to == Unit.m3:
                        return value / float(conversion.value)
                    if declared_unit == Unit.m3 and conversion.to == Unit.kg:
                        return value * float(conversion.value)

                elif conversion.meta_data.unit == ConversionUnit.KG_PER_M2.value:
                    if declared_unit == Unit.kg and conversion.to == Unit.m2:
                        return value / float(conversion.value)
                    if declared_unit == Unit.m2 and conversion.to == Unit.kg:
                        return value * float(conversion.value)

                elif conversion.meta_data.unit == ConversionUnit.KG_PER_M.value:
                    if declared_unit == Unit.kg and conversion.to == Unit.m:
                        return value / float(conversion.value)
                    if declared_unit == Unit.m and conversion.to == Unit.kg:
                        return value * float(conversion.value)
                
                elif conversion.meta_data.unit == ConversionUnit.M.value:
                    if declared_unit == Unit.m2 and conversion.to == Unit.m:
                        return value / float(conversion.value)
                    if declared_unit == Unit.m and conversion.to == Unit.m2:
                        return value * float(conversion.value)

                elif conversion.meta_data.unit == ConversionUnit.KG.value:
                    if declared_unit == Unit.pcs and conversion.to == Unit.kg:
                        return value / float(conversion.value)
                    if declared_unit == Unit.kg and conversion.to == Unit.pcs:
                        return value * float(conversion.value)
            else:
                raise ValueError(f"Unsupported conversion from {declared_unit} to {conversion.to}")

        except Exception as e:
            raise ValueError(f"Error converting from {declared_unit} to {conversion.to}: {str(e)}")



    # epdx to product
    def from_epdx_to_product(self, epdx: EPD) -> Product_DTO:
        return self._mapper.to_product_epd(epdx)
  
    def from_epdx_to_product_list(self, epdx: list[EPD]) -> list[Product_DTO]:
        product_list = []
        invalid_epd_list = []
        start_time = time.perf_counter()
        for index, epd in enumerate(epdx):
            try:
                product_list.append(self._mapper.to_product_epd(epd))
            except Exception as e:
                invalid_epd_list.append(index)
                print(f"Error converting EPD to Product: {str(e)}")

        end_time = time.perf_counter()
        time_diff = end_time - start_time
        minutes = int(time_diff // 60)
        seconds = int(time_diff % 60)
        print(
            f"convert all valid retrieved data to products list took: {minutes} minutes and {seconds} seconds"
        )
        print(f"successfully converted epds: {len(product_list)}")
        print(f"failed to convert epds: {len(invalid_epd_list)}")
        print(f"failed epds: \n {invalid_epd_list}")
        return product_list

    def from_epdx_product_header(self, epdx: EPD) -> ProductHeader_DTO:
        return self._mapper.to_product_header(epdx)

    def from_epdx_product_stats(self, epdx: EPD) -> ProductDensity_DTO:
        return self._mapper.to_product_stats(epdx)

    # product to epdx
    def from_product_to_epdx(self, product: Product_DTO) -> EPD:
        return self._mapper.to_epdx(product)

    def from_product_to_epdx_json(self, product: Product_DTO) -> dict:
        return self._mapper.to_epdx_json(self._mapper.to_epdx(product))
