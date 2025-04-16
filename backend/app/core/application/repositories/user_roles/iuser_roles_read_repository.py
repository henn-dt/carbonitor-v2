# app/core/application/repositories/user_roles/iuser_roles_read_repository.py
from app.core.domain.entities import user_roles
from app.core.application.repositories.base.iassociation_read_repository import IAssociationReadRepository

class IUserRolesReadRepository(IAssociationReadRepository[user_roles]):
    pass