# app/core/application/repositories/user_roles/iuser_roles_write_repository.py
from app.core.domain.entities import user_roles
from app.core.application.repositories.base.iassociation_write_repository import IAssociationWriteRepository

class IUserRolesWriteRepository(IAssociationWriteRepository[user_roles]):
    pass