#backend/app/configs/database_config.py

import os
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()
from app.configs.base_config import BaseConfig

class DatabaseConfig:
    @staticmethod
    def is_external_db() -> bool:
        return os.environ.get('USE_EXTERNAL_DB', BaseConfig.USE_EXTERNAL_DB).lower() == 'true'

    @staticmethod
    def validate_database_url(url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    @staticmethod
    def get_database_url():
        
        use_external = DatabaseConfig.is_external_db()
        
        if use_external:
            external_db = os.environ.get('EXTERNAL_DATABASE_URL')
            if not external_db:
                raise ValueError("External database URL is required when USE_EXTERNAL_DB is true")
            if not DatabaseConfig.validate_database_url(external_db):
                raise ValueError("Invalid external database URL")
            return external_db

#backend/app/configs/database_config.py
        # SQLite internal database
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # Go up two levels to reach the root
        internal_db_path = os.path.join(root_dir, 'internal.db')
        return f'sqlite:///{internal_db_path}'

"""         internal_db = BaseConfig.INTERNAL_DATABASE_URL            
        if not DatabaseConfig.validate_database_url(internal_db):
            raise ValueError("Invalid internal database URL")
        return internal_db """