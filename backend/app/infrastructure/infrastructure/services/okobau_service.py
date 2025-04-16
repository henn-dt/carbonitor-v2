# app/infrastructure/infrastructure/okobau_service.py
import sys

sys.path.append("/home/admin/carbonitor-v2/backend")  # Your project root path
import json
import time
from collections import Counter

import lcax
import requests
from app.config import Config
from app.core.application.dtos.epdx.epdx_dto import EPD
from app.core.application.dtos.okobau.okobau_dto import EPDResponse
from app.core.application.mappers.iexternal_product_mapper import IOkobauMapper
from app.core.application.services.iokobau_service import IOkobauService
from app.core.domain.entities.product import Product


class OkobauService(IOkobauService):
    def __init__(self,
        mapper = IOkobauMapper
    ):
        self._mapper = mapper

    def get_epds(self) -> dict:
        response = requests.get(Config.EXTERNAL_RESOURCES.OKOBAU.FULL_LIST_URL)
        response.raise_for_status()
        data = response.json()
        return data

    def get_ilcd_from_uuid(self, uuid: str) -> dict:
        base_url = f"{Config.EXTERNAL_RESOURCES.OKOBAU.SINGLE_ITEM_URL}{uuid}"
        response = requests.get(f"{base_url}?format=json&view=extended")
        response.raise_for_status()
        data = response.json()
        return data

    def get_epds_list(self) -> list:
        return self.get_epds().get("data", [])

    def get_epdx_from_uuid(self, uuid: str) -> EPD:
        try:
            return self._mapper.uuid_to_epdx(uuid)
        except Exception as e:
                print(
                    f"Invalid EPD - UUID: {uuid}, Error: {str(e)}"
                )


    def get_epd_response_list(self) -> list[EPDResponse]:
        raw_epds = self.get_epds_list()
        valid_epds: list[EPDResponse] = []
        invalid_count = 0

        for epd_data in raw_epds:
            try:
                # Direct conversion using dict unpacking
                epd_response = EPDResponse(**epd_data)
                valid_epds.append(epd_response)
            except Exception as e:
                invalid_count += 1
                print(
                    f"Invalid EPD - UUID: {epd_data.get('uuid', 'No UUID')}, Error: {str(e)}"
                )
                continue
        return valid_epds

    def get_epdx(self, epd_response: EPDResponse) -> EPD:
        try:
            return self._mapper.epd_to_epdx(epd_response)
        except Exception as e:
            print(f"error getting epdx: {e}")

    def get_epdx_list(self) -> list[EPD]:
        epds = self.get_epd_response_list()
        epdx_list: list[EPD] = []
        invalid_epd_list: list[EPDResponse] = []
        start_time = time.perf_counter()

        for i, epd in enumerate(epds):
            try:
                epdx_list.append(self._mapper.epd_to_epdx(epd))
            except Exception as e:
                invalid_epd_list.append(i)
                print(str(e))

        end_time = time.perf_counter()
        time_diff = end_time - start_time
        minutes = int(time_diff // 60)
        seconds = int(time_diff % 60)
        print(
            f"Retrieving all data from okobau and convert them to epdx list takes: {minutes} minutes and {seconds} seconds"
        )
        print(f"successfully converted responses: {len(epdx_list)}")
        print(f"failed to convert responses: {len(invalid_epd_list)}")
        print(f"failed responses: \n {invalid_epd_list}")
        return epdx_list

    def get_language_statistics(self):
        epd_list = self.get_epd_response_list()
        # Get all languages using map and flatten
        languages = [
            lang for langs in map(lambda epd: epd.languages, epd_list) for lang in langs
        ]

        # Get unique languages (set)
        unique_languages = set(languages)

        # Get occurrences using Counter
        language_counts = Counter(languages)

        print("\nUnique languages:", sorted(unique_languages))
        print("\nLanguage occurrences:")
        for lang, count in language_counts.items():
            print(f"{lang}: {count}")

        return unique_languages, language_counts

    # Or more detailed version:
    def analyze_languages(self):
        epd_list = self.get_epd_response_list()
        languages = [
            lang for langs in map(lambda epd: epd.languages, epd_list) for lang in langs
        ]

        # Statistics
        language_counts = Counter(languages)
        total_epds = len(epd_list)

        print(f"\nLanguage Analysis:")
        print(f"Total EPDs: {total_epds}")
        print(f"Unique languages: {sorted(set(languages))}")
        print(f"\nOccurrences:")

        for lang, count in sorted(language_counts.items()):
            percentage = (count / total_epds) * 100
            print(f"{lang}: {count} EPDs ({percentage:.1f}%)")

    def test(self):
        try:
            okobau_service1 = OkobauService()
            epds_list = okobau_service1.get_epd_response_list()
            epd_item: EPDResponse = epds_list[5]
            base_url = (
                f"{Config.EXTERNAL_RESOURCES.OKOBAU.SINGLE_ITEM_URL}{epd_item.uuid}"
            )
            response = requests.get(f"{base_url}?format=json&view=extended")
            response.raise_for_status()
            data = response.json()
            data["source"] = base_url
            # part of epdx service
            # we will call epdx service di container and serialize it and use it in product service and feed our database and
            # also we gonna use epdx service serializer to make calculations
            # but first step is serialize and deserialize it for our db
            # and try to use automappers and pydantic
            epdx = lcax.convert_ilcd(data=json.dumps(data), as_type=str)
            epdx_dict = json.loads(epdx)  # Parse the JSON string into a dictionary
            print(epdx_dict)
            productEpdx = EPD(**epdx_dict)

            print("--------------------detailed epd---------------")
            print(data)
            print("\n")
            print("-----------------epdx---------------------")
            print(productEpdx)

            print("-----------------epdx to product----------------------")
            product = Product()
            # product.status user defined
            product.epd_name = productEpdx.name
            product.epd_declaredUnit = (
                productEpdx.declared_unit
            )  # declared_unit=<Unit.m2: 'm2'>
            product.epd_version = productEpdx.version  # version='1.1'
            product.epd_publishedDate = (
                productEpdx.published_date
            )  # datetime.date(2021, 1, 1)
            product.epd_validUntil = (
                productEpdx.valid_until
            )  # datetime.date(2028, 1, 1)
            product.epd_standard = (
                productEpdx.standard
            )  # <Standard.en15804a2: 'en15804a2'>
            product.epd_comment = productEpdx.comment  # comment=None
            product.epd_location = (
                productEpdx.location
            )  # location=<Country.unknown: 'unknown'> comes from class Country(Enum) in epdx_item
            product.epd_formatVersion = (
                productEpdx.format_version
            )  # format_version='2.6.3'
            product.epd_id = productEpdx.id
            product.epdx = productEpdx.model_dump_json()
            product.epd_sourceName = "okobaudat"  # user defined
            product.epd_sourceUrl = (
                "okobaudat url with id"  # user defined okobaudat url with id
            )
            product.epd_linear_density = next(
                (
                    i.meta_data.get("value")
                    for i in productEpdx.conversions
                    if i.meta_data.get("name") == "linear density"
                    and i.meta_data.get("value") is not None
                ),
                None,
            )
            product.epd_gross_density = next(
                (
                    i.meta_data.get("value")
                    for i in productEpdx.conversions
                    if i.meta_data.get("name") == "gross density"
                    and i.meta_data.get("value") is not None
                ),
                None,
            )
            product.epd_grammage = next(
                (
                    i.meta_data.get("value")
                    for i in productEpdx.conversions
                    if i.meta_data.get("name") == "epd grammage"
                    and i.meta_data.get("value") is not None
                ),
                None,
            )
            product.epd_layer_thickness = next(
                (
                    i.meta_data.get("value")
                    for i in productEpdx.conversions
                    if i.meta_data.get("name") == "layer thickness"
                    and i.meta_data.get("value") is not None
                ),
                None,
            )
            product.epd_bulk_density = next(
                (
                    i.meta_data.get("value")
                    for i in productEpdx.conversions
                    if i.meta_data.get("name") == "bulk density"
                    and i.meta_data.get("value") is not None
                ),
                None,
            )

            print("product epd_layer_thickness\n")
            print(product.epd_layer_thickness)
            print("linear density\n")
            print(product.epd_linear_density)

            #### implement serializer next step and create frontend forms also mock data in backend
        except:
            print("error")


# if __name__ ==
