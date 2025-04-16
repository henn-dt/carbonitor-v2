from enum import Enum
from app.core.application.dtos.epdx.epdx_dto import ImpactCategoryKey

class DefaultImpacts(str, Enum):
    GWP : ImpactCategoryKey = ImpactCategoryKey.gwp
    GWP_FOS : ImpactCategoryKey = ImpactCategoryKey.gwp_fos
    GWP_BIO : ImpactCategoryKey = ImpactCategoryKey.gwp_bio
    GWP_LUL : ImpactCategoryKey = ImpactCategoryKey.gwp_lul
    FW : ImpactCategoryKey = ImpactCategoryKey.fw