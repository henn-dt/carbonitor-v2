import os
from click import Tuple
from dotenv import load_dotenv
load_dotenv()
from app.configs.base_config import BaseConfig

class EnvVarNotFoundError(Exception):
    """Custom exception for missing environment variables in .env file"""
    def __init__(self, var_name: str):
        self.var_name = var_name
        self.message = f"{var_name} not found in .env file"
        super().__init__(self.message)

class UserConfig:
    DEFAULT_USER_ROLE_NAME = os.environ.get('DEFAULT_USER_ROLE_NAME', BaseConfig.DEFAULT_USER_ROLE_NAME)

    @staticmethod
    def is_test_user() -> bool:
        test_user = os.environ.get('TEST_USER', BaseConfig.TEST_USER)
        if test_user:
            if test_user.lower() == 'true':
                return True
        return False
    
    @staticmethod
    def test_user_email() -> str:
        email = os.environ.get('TEST_USER_EMAIL', BaseConfig.TEST_USER_EMAIL)
        if UserConfig.is_test_user():
            if not email:
                raise EnvVarNotFoundError('TEST_USER_EMAIL', BaseConfig.TEST_USER_EMAIL)
            return email
        return None

    @staticmethod
    def test_user_username() -> str:
        username = os.environ.get('TEST_USER_USERNAME', BaseConfig.TEST_USER_USERNAME)
        if UserConfig.is_test_user():
            if not username:
                raise EnvVarNotFoundError('TEST_USER_USERNAME', BaseConfig.TEST_USER_USERNAME)
            return username
        return None

    @staticmethod
    def test_user_password() -> str:
        password = os.environ.get('TEST_USER_PASSWORD', BaseConfig.TEST_USER_PASSWORD)
        if UserConfig.is_test_user():
            if not password:
                raise EnvVarNotFoundError('TEST_USER_PASSWORD', BaseConfig.TEST_USER_PASSWORD)
            return password
        return None

    @staticmethod
    def test_user_auth() -> str:
        auth = os.environ.get('TEST_USER_AUTH', BaseConfig.TEST_USER_AUTH)
        if UserConfig.is_test_user():
            if not auth:
                raise EnvVarNotFoundError('TEST_USER_AUTH', BaseConfig.TEST_USER_AUTH)
            return auth
        return None
    
    @staticmethod
    def get_test_user_credentials() -> Tuple:
        email = UserConfig.test_user_email()
        username = UserConfig.test_user_username()
        password = UserConfig.test_user_password()
        auth_method = UserConfig.test_user_auth()
        
        return email, username, password, auth_method