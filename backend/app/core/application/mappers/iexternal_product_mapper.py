from abc import abstractmethod

from app.core.application.dtos.epdx.epdx_dto import EPD
from app.core.application.dtos.okobau.okobau_dto import \
    EPDResponse as OkobauResponse


class IOkobauMapper():
    @abstractmethod
    def uuid_to_epdx(uuid: str) -> EPD:
        pass

    @abstractmethod
    def epd_to_epdx(epd: OkobauResponse) -> EPD:
        pass