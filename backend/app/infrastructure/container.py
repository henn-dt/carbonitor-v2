# app/infrastructure/container.py
from app.config import Config
from app.infrastructure.infrastructure.services.authentication_service import AuthenticationService
from app.infrastructure.infrastructure.services.epdx_service import EpdxService
from app.infrastructure.infrastructure.services.jwt_service import JWTService
from app.infrastructure.infrastructure.services.okobau_service import OkobauService
from app.infrastructure.infrastructure.services.password_service import PasswordService
from app.infrastructure.infrastructure.services.permission_service import PermissionService
from app.infrastructure.mappers.category_association_mapper import CategoryAssociationMapper
from app.infrastructure.mappers.category_mapper import CategoryMapper
from app.infrastructure.mappers.epdx_mapper import EpdxMapper
from app.infrastructure.mappers.external_product_mapper import OkobauMapper
from app.infrastructure.mappers.product_mapper import ProductMapper
from app.infrastructure.mappers.role_mapper import RoleMapper
from app.infrastructure.mappers.user_mapper import UserMapper
from app.infrastructure.mappers.user_roles_mapper import UserRolesMapper
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.infrastructure.persistence.repositories.category.category_read_repository import CategoryReadRepository
from app.infrastructure.persistence.repositories.category.category_write_repository import CategoryWriteRepository
from app.infrastructure.persistence.repositories.category_association.category_association_read_repository import CategoryAssociationReadRepository
from app.infrastructure.persistence.repositories.category_association.category_association_write_repository import CategoryAssociationWriteRepository
from app.infrastructure.persistence.repositories.product.product_read_repository import ProductReadRepository
from app.infrastructure.persistence.repositories.product.product_write_repository import ProductWriteRepository
from app.infrastructure.persistence.repositories.role.role_read_repository import RoleReadRepository
from app.infrastructure.persistence.repositories.role.role_write_repository import RoleWriteRepository
from app.infrastructure.persistence.repositories.user.user_read_repository import UserReadRepository
from app.infrastructure.persistence.repositories.user.user_write_repository import UserWriteRepository
from app.infrastructure.persistence.repositories.user_roles.user_roles_read_repository import UserRolesReadRepository
from app.infrastructure.persistence.repositories.user_roles.user_roles_write_repository import UserRolesWriteRepository
from app.infrastructure.persistence.services.category_association_service import CategoryAssociationService
from app.infrastructure.persistence.services.category_service import CategoryService
from app.infrastructure.persistence.services.product_service import ProductService
from app.infrastructure.persistence.services.role_service import RoleService
from app.infrastructure.persistence.services.user_roles_service import UserRolesService
from app.infrastructure.persistence.services.user_service import UserService

from app.infrastructure.mappers.filter_element_mapper import FilterElementMapper
from app.infrastructure.persistence.repositories.filter_element.filter_element_read_repository import FilterElementReadRepository
from app.infrastructure.persistence.repositories.filter_element.filter_element_write_repository import FilterElementWriteRepository
from app.infrastructure.persistence.services.filter_element_service import FilterElementService

from app.infrastructure.mappers.filter_mapping_mapper import FilterMappingMapper
from app.infrastructure.persistence.repositories.filter_mapping.filter_mapping_read_repository import FilterMappingReadRepository
from app.infrastructure.persistence.repositories.filter_mapping.filter_mapping_write_repository import FilterMappingWriteRepository
from app.infrastructure.persistence.services.filter_mapping_service import FilterMappingService

from app.infrastructure.mappers.buildup_mapper import BuildupMapper
from app.infrastructure.persistence.repositories.buildup.buildup_read_repository import BuildupReadRepository
from app.infrastructure.persistence.repositories.buildup.buildup_write_repository import BuildupWriteRepository
from app.infrastructure.persistence.services.buildup_service import BuildupService

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.presentation.controllers.product_controller",
            "app.presentation.controllers.buildup_controller",
            "app.presentation.controllers.category_controller",
            "app.presentation.controllers.category_association_controller",
            "app.presentation.controllers.user_controller",
            "app.presentation.controllers.role_controller",
            "app.presentation.controllers.user_roles_controller",
            "app.presentation.controllers.authentication_controller",
            "app.presentation.controllers.filter_element_controller",
            "app.presentation.controllers.filter_mapping_controller",
            "app.cli.seed",
        ]
    )
    config = providers.Singleton(Config)
    db_context = providers.Singleton(
        DBContext, connection_string=Config.DATABASE_CONFIG.get_database_url()
    )

    # ----------REPOSITORIES---------------------
    product_read_repository = providers.Singleton(ProductReadRepository, db_context=db_context)
    product_write_repository = providers.Singleton(ProductWriteRepository, db_context=db_context)
    buildup_read_repository = providers.Singleton(BuildupReadRepository, db_context=db_context)
    buildup_write_repository = providers.Singleton(BuildupWriteRepository, db_context=db_context)
    user_read_repository = providers.Singleton(UserReadRepository, db_context=db_context)
    user_write_repository = providers.Singleton(UserWriteRepository, db_context=db_context)
    role_read_repository = providers.Singleton(RoleReadRepository, db_context=db_context)
    role_write_repository = providers.Singleton(RoleWriteRepository, db_context=db_context)
    user_roles_read_repository = providers.Singleton(UserRolesReadRepository, db_context=db_context)
    user_roles_write_repository = providers.Singleton(UserRolesWriteRepository, db_context=db_context)
    category_read_repository = providers.Singleton(CategoryReadRepository, db_context=db_context)
    category_write_repository = providers.Singleton(CategoryWriteRepository, db_context=db_context)
    category_association_read_repository = providers.Singleton(CategoryAssociationReadRepository, db_context=db_context)
    category_association_write_repository = providers.Singleton(CategoryAssociationWriteRepository, db_context=db_context)

    filter_element_read_repository = providers.Singleton(FilterElementReadRepository, db_context=db_context)
    filter_element_write_repository = providers.Singleton(FilterElementWriteRepository, db_context=db_context)

    filter_mapping_read_repository = providers.Singleton(FilterMappingReadRepository, db_context=db_context)
    filter_mapping_write_repository = providers.Singleton(FilterMappingWriteRepository, db_context=db_context)

    # ---------------------INFRASTRUCTURE SERVICES-------------------
    permission_service = providers.Singleton(PermissionService)
    password_service = providers.Singleton(PasswordService)

    # ------------------------MAPPERS--------------------------------
    role_mapper = providers.Singleton(RoleMapper)
    user_mapper = providers.Singleton(UserMapper, password_service=password_service)
    user_roles_mapper = providers.Singleton(UserRolesMapper)
    epdx_mapper = providers.Singleton(EpdxMapper)
    okobau_mapper = providers.Singleton(OkobauMapper)
    product_mapper = providers.Singleton(ProductMapper)

    category_mapper = providers.Singleton(CategoryMapper)
    category_association_mapper = providers.Singleton(CategoryAssociationMapper)

    filter_element_mapper = providers.Singleton(FilterElementMapper)
    filter_mapping_mapper = providers.Singleton(FilterMappingMapper)
    

    # ------------------------PERSISTENCE SERVICES------------------------
    epdx_service = providers.Singleton(EpdxService, mapper=epdx_mapper)
    okobau_service = providers.Singleton(OkobauService, mapper=okobau_mapper)
    product_service = providers.Singleton(
        ProductService,
        product_read_repository=product_read_repository,
        product_write_repository=product_write_repository,
        product_mapper=product_mapper,
        epdx_service=epdx_service,
    )

    buildup_mapper = providers.Singleton(BuildupMapper, product_service = product_service)     # should restructure this a bit, so that things are grouped consistently.
    buildup_service = providers.Singleton(
        BuildupService,
        buildup_read_repository=buildup_read_repository,
        buildup_write_repository=buildup_write_repository,
        buildup_mapper=buildup_mapper,
        product_service = product_service
        
    )

    category_service = providers.Singleton(
        CategoryService,
        category_read_repository=category_read_repository,
        category_write_repository=category_write_repository,
        category_mapper=category_mapper,
    )

    category_association_service = providers.Singleton(
        CategoryAssociationService,
        category_association_read_repository= category_association_read_repository,
        category_association_write_repository= category_association_write_repository,
        category_association_mapper= category_association_mapper,
        category_service= category_service
    )

    filter_element_service = providers.Singleton(
        FilterElementService,
        filter_element_read_repository = filter_element_read_repository,
        filter_element_write_repository = filter_element_write_repository,
        filter_element_mapper = filter_element_mapper
    )

    filter_mapping_service = providers.Singleton(
        FilterMappingService,
        filter_mapping_read_repository = filter_mapping_read_repository,
        filter_mapping_write_repository = filter_mapping_write_repository,
        filter_mapping_mapper = filter_mapping_mapper
    )
 
    
    user_service = providers.Singleton(
        UserService,
        user_read_repository=user_read_repository,
        user_write_repository=user_write_repository,
        user_mapper=user_mapper,
    )
    role_service = providers.Singleton(
        RoleService,
        role_read_repository=role_read_repository,
        role_write_repository=role_write_repository,
        role_mapper=role_mapper,
        permission_service=permission_service,
    )
    user_roles_service = providers.Singleton(
        UserRolesService,
        user_roles_read_repository=user_roles_read_repository,
        user_roles_write_repository=user_roles_write_repository,
        user_service=user_service,
        role_service=role_service,
        user_roles_mapper=user_roles_mapper,
    )
    jwt_service = providers.Singleton(
        JWTService,
        secret_key=Config.AUTH_CONFIG.JWT_SECRET,
        access_token_expire_minutes=15,
        refresh_token_expire_days=7,
        algorithm="HS256",
    )
    
    authentication_service = providers.Singleton(
        AuthenticationService,
        user_service=user_service,
        role_service=role_service,
        user_roles_service=user_roles_service,
        jwt_service=jwt_service,
        password_service=password_service,
    )
