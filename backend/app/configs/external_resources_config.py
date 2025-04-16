import os
from dotenv import load_dotenv
load_dotenv()
from app.configs.base_config import BaseConfig

class OkobauConfig:
    DATASTOCK_ID = os.environ.get("OEKOBAU_DATASTOCK_ID", BaseConfig.OEKOBAU_DATASTOCK_ID)
    MAIN_URL = f"https://oekobaudat.de/OEKOBAU.DAT/resource/datastocks/{DATASTOCK_ID}"
    COMPLIANCE_ID_A1 = os.environ.get("OEKOBAU_COMPLIANCE_ID_A1", BaseConfig.OEKOBAU_COMPLIANCE_ID_A1)
    COMPLIANCE_ID_A2 = os.environ.get("OEKOBAU_COMPLIANCE_ID_A2", BaseConfig.OEKOBAU_COMPLIANCE_ID_A2) #choose a1 in first phases of dev
    FULL_LIST_URL = f"{MAIN_URL}/processes?search=true&compliance={COMPLIANCE_ID_A2}&format=json&pageSize=5000"
    FULL_LIST_URL_A1 = f"{MAIN_URL}/processes?search=true&format=json&pageSize=5000"
    SINGLE_ITEM_URL = f"{MAIN_URL}/processes/"

class ExternalResourcesConfig:
    OKOBAU = OkobauConfig