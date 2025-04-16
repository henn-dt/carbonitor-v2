from pathlib import Path

class PathConfig:
    # Base path
    APP_DIR = Path(__file__).parent.parent  # Points to app directory
    # Infrastructure paths
    INFRASTRUCTURE_DIR = APP_DIR / 'infrastructure'
    PERSISTENCE_DIR = INFRASTRUCTURE_DIR / 'persistence'
    # Migration Directories
    MIGRATIONS_DIR = PERSISTENCE_DIR / 'migrations'
    MIGRATIONS_VERSIONS_DIR = MIGRATIONS_DIR / 'versions'
    # Migration files
    ALEMBIC_CONFIG_FILE = MIGRATIONS_DIR / 'alembic.ini'
    ALEMBIC_ENV_PY_FILE = MIGRATIONS_DIR / 'env.py'
    