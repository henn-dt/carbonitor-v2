# app/core/application/services/role_service.py
from typing import List, Optional, Set
from app.core.domain.enums.permissions import Permission
from app.core.application.repositories.role.irole_read_repository import IRoleReadRepository
from app.core.application.repositories.role.irole_write_repository import IRoleWriteRepository
from app.core.application.services.ipermission_service import IPermissionService
from app.core.application.dtos.role.create_role_dto import CreateRoleDTO
from app.core.application.dtos.role.update_role_dto import UpdateRoleDTO
from app.core.application.dtos.role.role_dto import RoleDTO, RoleDetailDTO
from app.core.application.mappers.irole_mapper import IRoleMapper
from app.core.application.services.irole_service import IRoleService

class RoleService(IRoleService):
    def __init__(
        self,
        role_read_repository: IRoleReadRepository,
        role_write_repository: IRoleWriteRepository,
        role_mapper: IRoleMapper,
        permission_service: IPermissionService
    ):
        self._role_read_repository = role_read_repository
        self._role_write_repository = role_write_repository
        self._role_mapper = role_mapper
        self._permission_service = permission_service
    
    def _validate_and_convert_permissions(self, permission_strings: List[str]) -> List[Permission]:
        if not permission_strings:
            return []
        permissions = [Permission(p) for p in permission_strings]
        if not self._permission_service.validate_permissions(permissions):
            raise ValueError("Invalid permissions provided")
        return permissions

    def create_role(self, dto: CreateRoleDTO) -> RoleDetailDTO:
        if self.get_role_by_name(dto.name):
            raise ValueError("Role name already exists")
        
        if dto.permissions:
            self._validate_and_convert_permissions(dto.permissions)
            
        role = self._role_mapper.create_dto_to_entity(dto)
        created_role = self._role_write_repository.create(role)
        return self._role_mapper.entity_to_detail_dto(created_role)
    
    def create_role_with_preset(self, role_name: str, is_admin: bool = False) -> RoleDetailDTO:
        permissions = (self._permission_service.default_admin_permissions()
                      if is_admin else self._permission_service.default_user_permissions())
        
        return self.create_role(CreateRoleDTO(
            name=role_name,
            description=f"{'admin role with admin permissions' if is_admin else 'default role with default permissions'}",
            permissions=permissions
        ))

    def get_role(self, role_id: int) -> Optional[RoleDetailDTO]:
        role = self._role_read_repository.get_by_id(role_id)
        return self._role_mapper.entity_to_dto(role) if role else None
    
    def get_all_roles(self) -> List[RoleDTO]:
        return [self._role_mapper.entity_to_dto(role) 
                for role in self._role_read_repository.get_all()]
    
    def get_role_by_name(self, name: str) -> Optional[RoleDetailDTO]:
        roles = self._role_read_repository.filter(name=name)
        return self._role_mapper.entity_to_dto(roles[0]) if roles else None
    
    def get_available_permissions(self) -> Set[str]:
        return {p.value for p in self._permission_service.get_all_permissions()}
    
    def update_role(self, role_id: int, dto: UpdateRoleDTO) -> Optional[RoleDetailDTO]:
        existing_role = self._role_read_repository.get_by_id(role_id)
        if not existing_role:
            return None
            
        if dto.permissions is not None:
            self._validate_and_convert_permissions(dto.permissions)
            
        changed_role = self._role_mapper.update_dto_to_entity(existing_role, dto)
        updated_role = self._role_write_repository.update(changed_role)
        return self._role_mapper.entity_to_detail_dto(updated_role)
    
    def delete_role(self, role_id: int) -> None:
        self._role_write_repository.delete(role_id)

    def delete_role_by_name(self, role_name: str) -> None:
        if role := self.get_role_by_name(role_name):
            self.delete_role(role.id)

    def check_or_create_role(self, role_name: str, is_admin: bool = False) -> str:
        if self.get_role_by_name(role_name):
            return f"Role {role_name} already exists."
        self.create_role_with_preset(role_name, is_admin)
        return f"Role {role_name} created."