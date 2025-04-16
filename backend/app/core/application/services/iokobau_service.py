from abc import ABC, abstractmethod

from app.core.application.dtos.epdx.epdx_dto import EPD
from app.core.application.dtos.okobau.okobau_dto import EPDResponse


class IOkobauService(ABC):
    @abstractmethod
    def get_epds(self) -> dict:
        pass

    @abstractmethod
    def get_epds_list() -> list:
        pass

    @abstractmethod
    def get_epd_response_list() -> list[EPDResponse]:
        pass

    @abstractmethod
    def get_language_statistics(self):
        pass

    @abstractmethod
    def get_ilcd_from_uuid(self, uuid: str) -> dict:
        pass

    @abstractmethod
    def get_epdx(self, epd: EPDResponse) -> EPD:
        pass

    @abstractmethod
    def get_epdx_list(self) -> list[EPD]:
        pass

    @abstractmethod
    def get_epdx_from_uuid(self, uuid: str) -> EPD:
        pass


    # Or more detailed version:
    @abstractmethod
    def analyze_languages(self):
        pass

    @abstractmethod
    def test(self):
        pass
