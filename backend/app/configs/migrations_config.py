from app.configs.path_config import PathConfig
from pathlib import Path

class MigrationsConfig:
    @classmethod
    def ensure_migrations_dir() -> None:
        """Ensure migrations directory structure exists"""
        migrations_dir_path = Path(PathConfig.MIGRATIONS_DIR)
        migrations_dir_path.mkdir(parents=True, exist_ok=True)
        migrations_versions_dir_path = Path(PathConfig.MIGRATIONS_VERSIONS_DIR)
        migrations_versions_dir_path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def ensure_migrations_files() -> None:
        alembic_file_path = Path(PathConfig.ALEMBIC_CONFIG_FILE)
        alembic_env_py_path = Path(PathConfig.ALEMBIC_ENV_PY_FILE)
        if not alembic_file_path.exists():
            with alembic_file_path.open('w') as file:
                file.write(MigrationsConfig.ALEMBIC_INI_TEMPLATE)
        if not alembic_env_py_path.exists():
            with alembic_env_py_path.open('w') as file:
                file.write(MigrationsConfig.ALEMBIC_PY_ENV)
            
    ALEMBIC_INI_TEMPLATE = """
        [alembic]
        script_location = .
        file_template = mig_%%(counter)03d

        [loggers]
        keys = root,sqlalchemy,alembic

        [handlers]
        keys = console

        [formatters]
        keys = generic

        [logger_root]
        level = WARN
        handlers = console
        qualname =

        [logger_sqlalchemy]
        level = WARN
        handlers =
        qualname = sqlalchemy.engine

        [logger_alembic]
        level = INFO
        handlers =
        qualname = alembic

        [handler_console]
        class = StreamHandler
        args = (sys.stderr,)
        level = NOTSET
        formatter = generic

        [formatter_generic]
    """
    ALEMBIC_PY_ENV="""
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
            return Config.DatabaseConfig.get_database_url()

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
                    compare_type=True,
                    compare_server_default=True,
                )

                with context.begin_transaction():
                    context.run_migrations()

        if context.is_offline_mode():
            run_migrations_offline()
        else:
            run_migrations_online()
    """