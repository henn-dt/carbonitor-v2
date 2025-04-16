import os
from app.configs.base_config import BaseConfig
from click import Tuple
from dotenv import load_dotenv
load_dotenv()

class AdminConfig:
    ADMIN_USERNAME=os.environ.get('ADMIN_USERNAME', BaseConfig.ADMIN_USERNAME)
    ADMIN_PASSWORD=os.environ.get('ADMIN_PASSWORD', BaseConfig.ADMIN_PASSWORD)
    ADMIN_EMAIL=os.environ.get('ADMIN_EMAIL', BaseConfig.ADMIN_EMAIL)
    ADMIN_AUTH_METHOD=os.environ.get('ADMIN_AUTH_METHOD', BaseConfig.ADMIN_AUTH_METHOD)
    ADMIN_ROLE_NAME=os.environ.get('ADMIN_ROLE_NAME', BaseConfig.ADMIN_ROLE_NAME)

    @staticmethod
    def get_admin_user_credentials() -> Tuple:
        email = AdminConfig.ADMIN_EMAIL
        username = AdminConfig.ADMIN_USERNAME
        password = AdminConfig.ADMIN_PASSWORD
        auth_method = AdminConfig.ADMIN_AUTH_METHOD
        return email, username, password, auth_method