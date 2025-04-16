# app/infrastructure/persistence/repositories/user_roles/user_roles_write_repository.py
from app.core.application.repositories.user_roles.iuser_roles_write_repository import IUserRolesWriteRepository
from app.core.domain.entities import user_roles
from app.infrastructure.persistence.contexts.dbcontext import DBContext
from app.infrastructure.persistence.repositories.base.association_write_repository import AssociationWriteRepository

class UserRolesWriteRepository(AssociationWriteRepository[user_roles], IUserRolesWriteRepository):
    def __init__(self, db_context: DBContext):
        super().__init__(db_context, user_roles, ["user_id", "role_id"])