# app/cli/db.py
import click
from flask.cli import with_appcontext
from alembic import command
from alembic.config import Config as AlembicConfig
from sqlalchemy import text
from app.config import Config
from app.infrastructure.persistence.contexts.dbcontext import DBContext

def get_config() -> AlembicConfig:
    """Get Alembic configuration."""
    # Ensure migrations directory exists
    Config.MIGRATIONS.ensure_migrations_dir
    
    # Create alembic.ini if it doesn't exist
    Config.MIGRATIONS.ensure_migrations_files

    config = AlembicConfig(str(Config.PATHS.ALEMBIC_CONFIG_FILE))
    config.set_main_option('sqlalchemy.url', Config.DATABASE_CONFIG.get_database_url())
    config.set_main_option('script_location', str(Config.PATHS.MIGRATIONS_DIR))
    return config

def get_db_context() -> DBContext:
    """Get database context."""
    config=get_config()
    db_url = config.get_main_option('sqlalchemy.url')
    return DBContext(db_url)

@click.group(name='db')
def db_cli() -> None:
    """Database migration commands."""
    pass

@db_cli.command()
@with_appcontext
def init() -> None:
    """Initialize migration environment."""
    config = get_config()
    command.init(config, str(Config.PATHS.MIGRATIONS_DIR))

@db_cli.command()
@click.option('--description', '-d', default=None, help='Migration description')
@with_appcontext
def migrate(description: str | None) -> None:
    """Generate new migration."""
    config = get_config()
    command.revision(config, autogenerate=True, message=description)

@db_cli.command()
@with_appcontext
def upgrade() -> None:
    """Apply all migrations."""
    config = get_config()
    command.upgrade(config, "head")

@db_cli.command()
@with_appcontext
def downgrade() -> None:
    """Revert last migration."""
    config = get_config()
    command.downgrade(config, "-1")

@db_cli.command()
@with_appcontext
def recreate() -> None:
    """Drop all tables and recreate them."""
    config = get_config()
    command.downgrade(config, "base")
    command.upgrade(config, "head")

@db_cli.command()
@with_appcontext
def verify() -> bool:
    """Verify database connection and configuration."""
    try:
        db_context = get_db_context()
        with db_context.session() as session:
            session.execute(text("SELECT 1"))
        click.echo("Database connection successful!")
        return True
    except Exception as e:
        click.echo(f"Database connection failed: {str(e)}", err=True)
        return False

@db_cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Show full information about each revision')
@with_appcontext
def history(verbose: bool) -> None:
    """Show revision history."""
    config = get_config()
    command.history(config, verbose=verbose)

# New current command to show the current revision
@db_cli.command()
@with_appcontext
def current() -> None:
    """Show current revision."""
    config = get_config()
    command.current(config)

# New show command to display the given revision
@db_cli.command()
@click.argument('revision')
@with_appcontext
def show(revision: str) -> None:
    """Show the given revision."""
    config = get_config()
    command.show(config, revision)

# New heads command to display the heads of the script
@db_cli.command()
@click.option('--resolve-dependencies', '-d', is_flag=True, help='Treat dependency versions as down revisions')
@with_appcontext
def heads(resolve_dependencies: bool) -> None:
    """Show current available heads in the script."""
    config = get_config()
    command.heads(config, resolve_dependencies=resolve_dependencies)

# New branches command to show unmerged branches
@db_cli.command()
@with_appcontext
def branches() -> None:
    """Show unmerged branches."""
    config = get_config()
    command.branches(config)