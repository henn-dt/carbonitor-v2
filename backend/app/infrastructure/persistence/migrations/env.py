# app/infrastructure/persistence/migrations/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
# Import all entities and config
from app.core.domain.entities import *
from app.core.domain.entities import Base
from app.config import Config

config = context.config

if Config.PATHS.ALEMBIC_CONFIG_FILE.exists():
    fileConfig(str(Config.PATHS.ALEMBIC_CONFIG_FILE))

target_metadata = Base.metadata

# Override sqlalchemy.url with value from Config
def get_url():
    return Config.DATABASE_CONFIG.get_database_url()

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = {
        'sqlalchemy.url': get_url(),
        'sqlalchemy.echo': True,
    }
    connectable = engine_from_config(
        configuration,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,  # compatibility with sqlite
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()