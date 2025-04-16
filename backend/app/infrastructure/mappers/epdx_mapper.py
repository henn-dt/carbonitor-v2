#backend/app/infrastructure/mappers/epdx_mapper.py

import json
from datetime import datetime
from functools import wraps
from typing import Callable, List, Optional, TypeVar

from app.core.application.dtos.epdx.epdx_dto import (EPD, Conversion,
                                                     ConversionConfig,
                                                     ConversionMetaData,
                                                     ConversionType, Country,
                                                     Source, Standard, SubType,
                                                     Unit)
from app.core.application.dtos.product.product_dto import (Product_DTO,
                                                           ProductDensity_DTO,
                                                           ProductEPD_DTO,
                                                           ProductHeader_DTO)
from app.core.application.mappers.iepdx_mapper import IEpdxMapper


class EpdxMapper(IEpdxMapper):
    ### deserialiser methods
    @staticmethod
    def to_epdx(product: Product_DTO) -> EPD:
        source = (Source(name=product.epd_sourceName, url=product.epd_sourceUrl) if product.epd_sourceName else None)
        # Extract the embedded epdx JSON data first
        try:
            # If epdx is already a dict, use it directly; if it's a JSON string, parse it
            base_epdx = (json.loads(product.epdx) if isinstance(product.epdx, str) else product.epdx)
        except json.JSONDecodeError:
            raise ValueError("Invalid epdx JSON data in product")

        # Create conversion objects for density-related fields
        conversions: List[Conversion] = []
        density_mappings = {
            ConversionType.LINEAR_DENSITY: product.epd_linear_density,
            ConversionType.GROSS_DENSITY: product.epd_gross_density,
            ConversionType.GRAMMAGE: product.epd_grammage,
            ConversionType.LAYER_THICKNESS: product.epd_layer_thickness,
            ConversionType.BULK_DENSITY: product.epd_bulk_density,
        }

        for conv_type, value in density_mappings.items():
            if value is not None:
                config = ConversionConfig.MAPPINGS[conv_type]
                meta_data = ConversionMetaData(
                    name=conv_type.value, unit=config["unit"].value,
                    unit_description=config["unit_description"].value, value=value,
                )
                conversion = Conversion(meta_data=meta_data, to=config["to"], value=value) # The actual conversion value
                conversions.append(conversion)

        # Prepare the main EPD data
        epd_data = {
            "comment": product.epd_comment,
            "conversions": conversions if conversions else None,
            "declaredUnit": Unit(product.epd_declaredUnit),
            "formatVersion": product.epd_formatVersion,
            "id": product.epd_id,
            "impacts": base_epdx.get("impacts", {}),  # Get from embedded epdx
            "location": Country(product.epd_location),
            "metaData": None,  # As specified in the requirements
            "name": product.epd_name,
            "publishedDate": (
                datetime.strptime(product.epd_publishedDate, "%Y-%m-%d").date()
                if product.epd_publishedDate
                else None
            ),
            "referenceServiceLife": base_epdx.get("referenceServiceLife"),
            "source": source,
            "standard": Standard(product.epd_standard),
            "subtype": SubType(product.epd_subtype),
            "validUntil": (
                datetime.strptime(product.epd_validUntil, "%Y-%m-%d").date()
                if product.epd_validUntil
                else None
            ),
            "version": product.epd_version,
        }

        # validation with Pydantic
        try:
            return EPD.model_validate(epd_data)
        except ValueError as e:
            print(f"Error creating EPD object: {str(e)}")

    @staticmethod
    def to_epdx_json(epd: EPD) -> str:
        epdx_dict = {
            "comment": epd.comment,
            "conversions": (
                [
                    {
                        "metaData": {
                            "name": conv.meta_data.name,
                            "unit": conv.meta_data.unit,
                            "unit_description": conv.meta_data.unit_description,
                            "value": conv.meta_data.value,
                        },
                        "to": conv.to.value,
                        "value": conv.value,
                    }
                    for conv in epd.conversions
                ]
                if epd.conversions
                else None
            ),
            "declaredUnit": epd.declared_unit.value,
            "formatVersion": epd.format_version,
            "id": epd.id,
            "impacts": epd.impacts,
            "location": epd.location.value,
            "metaData": epd.meta_data,
            "name": epd.name,
            "publishedDate": epd.published_date.isoformat(),
            "referenceServiceLife": epd.reference_service_life,
            "source": (
                {"name": epd.source.name, "url": epd.source.url} if epd.source else None
            ),
            "standard": epd.standard.value,
            "subtype": epd.subtype.value,
            "validUntil": epd.valid_until.isoformat(),
            "version": epd.version,
        }

        return json.dumps(epdx_dict)

    #### serializer methods
    @staticmethod
    def to_product_header(epd: EPD) -> ProductHeader_DTO:
        return ProductHeader_DTO(
            #id=int(hash(f"{epd.source.name}{epd.id}")),
            epd_name=epd.name,
            status="default",  # Default status or pass as parameter
            epd_id=epd.id,
            epd_version=epd.version,
            epd_publishedDate=(
                epd.published_date.isoformat() if epd.published_date else None
            ),
            epd_validUntil=epd.valid_until.isoformat() if epd.valid_until else None,
            epd_standard=epd.standard.value,
            epd_comment=epd.comment,
            epd_location=epd.location.value,
            epd_formatVersion=epd.format_version,
            epd_sourceName=str(epd.source.name),
            epd_sourceUrl=str(epd.source.url),  # Construct URL as needed
            epd_subtype=epd.subtype.value,
        )

    @staticmethod
    def to_product_stats(epd: EPD) -> ProductDensity_DTO:
        # First get the header data
        header_data = EpdxMapper.to_product_header(epd).model_dump()
        # Get density values from conversions
        density_mappings = {
            ConversionType.LINEAR_DENSITY.value: "epd_linear_density",
            ConversionType.GROSS_DENSITY.value: "epd_gross_density",
            ConversionType.BULK_DENSITY.value: "epd_bulk_density",
            ConversionType.GRAMMAGE.value: "epd_grammage",
            ConversionType.LAYER_THICKNESS.value: "epd_layer_thickness",
        }

        density_values = {}
        if epd.conversions:
            for conversion in epd.conversions:
                name = conversion.meta_data.name
                if name in density_mappings:
                    # Try to convert value to float if it's a string
                    try:
                        value = float(conversion.meta_data.value)
                    except (TypeError, ValueError):
                        value = None
                    density_values[density_mappings[name]] = value

        return ProductDensity_DTO(
            **header_data, epd_declaredUnit=epd.declared_unit.value, **density_values
        )

    @staticmethod
    def to_product_epd(epd: EPD) -> Product_DTO:
        # Get stats data
        stats_data = EpdxMapper.to_product_stats(epd).model_dump()
        # validation with Pydantic
        try:
            return Product_DTO.model_validate(Product_DTO(**stats_data, epdx=json.loads(EpdxMapper.to_epdx_json(epd))))
        except ValueError as e:
            print(f"Error creating Product object from EPD: {str(e)}")