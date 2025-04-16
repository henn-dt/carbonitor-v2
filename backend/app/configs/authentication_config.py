import os
from app.configs.base_config import BaseConfig
from dotenv import load_dotenv
load_dotenv()

class AuthenticationConfig:
    JWT_SECRET = os.environ.get("JWT_SECRET", BaseConfig.JWT_SECRET)