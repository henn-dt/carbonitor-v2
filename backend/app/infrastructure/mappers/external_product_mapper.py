# backend/app/infrastructure/mappers/external_product_mapper.py

import json
from typing import Dict

import lcax
import requests
from app.config import Config
from app.core.application.dtos.epdx.epdx_dto import EPD
from app.core.application.dtos.okobau.okobau_dto import \
    EPDResponse as OkobauResponse
from app.core.application.mappers.iexternal_product_mapper import IOkobauMapper


class OkobauMapper(IOkobauMapper):

    @staticmethod
    def uuid_to_epdx(uuid: str) -> EPD:
        base_url = f"{Config.EXTERNAL_RESOURCES.OKOBAU.SINGLE_ITEM_URL}{uuid}"
        response = requests.get(f"{base_url}?format=json&view=extended")
        response.raise_for_status()
        data = response.json()
        epdx = lcax.convert_ilcd(data=json.dumps(data), as_type=str)
        epdx_dict = json.loads(epdx)  # Parse the JSON string into a dictionary
        epdx_dict["source"] = {"name": "Oekobaudat", "url": base_url}
        return EPD(**epdx_dict)

    @staticmethod
    def epd_to_epdx(epd: OkobauResponse) -> EPD:
        return OkobauMapper.uuid_to_epdx(epd.uuid)


    