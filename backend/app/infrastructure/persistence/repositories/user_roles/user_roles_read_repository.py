# app/infrastructure/persistence/repositories/user_roles/user_roles_read_repository.py
from app.core.application.repositories.user_roles.iuser_roles_read_repository import IUserRolesReadRepository
from app.core.domain.entities import user_roles
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.infrastructure.persistence.repositories.base.association_read_repository import AssociationReadRepository

class UserRolesReadRepository(AssociationReadRepository[user_roles], IUserRolesReadRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, user_roles, ["user_id", "role_id"])