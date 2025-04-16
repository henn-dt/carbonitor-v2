import click
from app.config import Config
from app.core.application.services.iepdx_service import IEpdxService
from app.core.application.services.iokobau_service import IOkobauService
from app.core.application.services.iproduct_service import IProductService
from app.core.application.services.irole_service import IRoleService
from app.core.application.services.iuser_roles_service import IUserRolesService
from app.core.application.services.iuser_service import IUserService
from app.infrastructure.container import Container
from dependency_injector.wiring import Provide, inject
from flask.cli import with_appcontext


@click.group(name="seed")
def seed_cli():
    """Database seeding commands."""
    pass


def seed_users(user_service: IUserService):
    """Core logic for seeding users."""
    email, username, password, auth_method = (
        Config.ADMIN_CONFIG.get_admin_user_credentials()
    )
    click.echo(
        user_service.verify_or_create_user(email, username, password, auth_method)
    )
    if Config.USER_CONFIG.is_test_user():
        email, username, password, auth_method = (
            Config.USER_CONFIG.get_test_user_credentials()
        )
        click.echo(
            user_service.verify_or_create_user(email, username, password, auth_method)
        )


def seed_roles(role_service: IRoleService):
    """Core logic for seeding roles."""
    click.echo(
        role_service.check_or_create_role(Config.ADMIN_CONFIG.ADMIN_ROLE_NAME, True)
    )
    click.echo(
        role_service.check_or_create_role(Config.USER_CONFIG.DEFAULT_USER_ROLE_NAME)
    )


def seed_user_roles(user_roles_service: IUserRolesService):
    click.echo(
        user_roles_service.verify_or_assign_role_to_user_by_names(
            Config.ADMIN_CONFIG.ADMIN_ROLE_NAME, Config.ADMIN_CONFIG.ADMIN_USERNAME
        )
    )
    if Config.USER_CONFIG.is_test_user():
        click.echo(
            user_roles_service.verify_or_assign_role_to_user_by_names(
                Config.USER_CONFIG.DEFAULT_USER_ROLE_NAME,
                Config.USER_CONFIG.test_user_username(),
            )
        )


def seed_okobau_product_by_uuid(
    uuid: str,
    okobau_service: IOkobauService,
    epdx_service: IEpdxService,
    product_service: IProductService,
    user_service: IUserService,
    ):

    admin_id = user_service.get_user_by_email(Config.ADMIN_CONFIG.get_admin_user_credentials()[0]).id
    product_dto = epdx_service.from_epdx_to_product(okobau_service.get_epdx_from_uuid(uuid))
    product_service.create_product_from_dto(product_dto, user_id=admin_id)

def seed_okobau_products(
    okobau_service: IOkobauService,
    epdx_service: IEpdxService,
    product_service: IProductService,
    user_service: IUserService,
):  
    admin_id = user_service.get_user_by_email(Config.ADMIN_CONFIG.get_admin_user_credentials()[0]).id
    product_dto_list = epdx_service.from_epdx_to_product_list(okobau_service.get_epdx_list())
    product_service.create_product_from_dto_list(product_dto_list, user_id = admin_id)


@seed_cli.command()
@with_appcontext
@inject
def users(user_service: IUserService = Provide[Container.user_service]):
    """Seed users table with sample data."""
    seed_users(user_service)


@seed_cli.command()
@with_appcontext
@inject
def roles(role_service: IRoleService = Provide[Container.role_service]):
    """Seed roles table with sample data."""
    seed_roles(role_service)


@seed_cli.command()
@with_appcontext
@inject
def user_roles(
    user_roles_service: IUserRolesService = Provide[Container.user_roles_service],
):
    """Seed roles table with sample data."""
    seed_user_roles(user_roles_service)


@seed_cli.command()
@with_appcontext
@inject
def products(
    okobau_service: IOkobauService = Provide[Container.okobau_service],
    epdx_service: IEpdxService = Provide[Container.epdx_service],
    product_service: IProductService = Provide[Container.product_service],
    user_service: IUserService = Provide[Container.user_service],
):
    """Seed users table with sample data."""
    seed_okobau_products(okobau_service, epdx_service, product_service, user_service)

@seed_cli.command('product_id')
@click.argument('uuid')
@with_appcontext
@inject
def product_id(
    uuid : str,
    okobau_service: IOkobauService = Provide[Container.okobau_service],
    epdx_service: IEpdxService = Provide[Container.epdx_service],
    product_service: IProductService = Provide[Container.product_service],
    user_service: IUserService = Provide[Container.user_service],
    
):
    """Seed users table with sample data."""
    seed_okobau_product_by_uuid(uuid, okobau_service, epdx_service, product_service, user_service)


@seed_cli.command()
@with_appcontext
@inject
def all(
    role_service: IRoleService = Provide[Container.role_service],
    user_service: IUserService = Provide[Container.user_service],
    user_roles_service: IUserRolesService = Provide[Container.user_roles_service],
):
    """Seed all tables with sample data."""
    seed_roles(role_service)
    seed_users(user_service)
    seed_user_roles(user_roles_service)
