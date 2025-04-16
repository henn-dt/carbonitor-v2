# app/config.py

from app.configs.admin_config import AdminConfig
from app.configs.migrations_config import MigrationsConfig
from app.configs.path_config import PathConfig
from app.configs.external_resources_config import ExternalResourcesConfig
from app.configs.database_config import DatabaseConfig
from app.configs.user_config import UserConfig
from app.configs.authentication_config import AuthenticationConfig


class Config:
    PATHS = PathConfig
    DATABASE_CONFIG = DatabaseConfig
    MIGRATIONS = MigrationsConfig
    EXTERNAL_RESOURCES  = ExternalResourcesConfig
    ADMIN_CONFIG = AdminConfig
    USER_CONFIG = UserConfig
    AUTH_CONFIG = AuthenticationConfig