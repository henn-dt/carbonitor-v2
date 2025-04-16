# app/infrastructure/mappers/role_mapper.py
from app.core.application.dtos.role.create_role_dto import CreateRoleDTO
from app.core.application.dtos.role.update_role_dto import UpdateRoleDTO
from app.core.application.dtos.role.role_dto import RoleDTO, RoleDetailDTO
from app.core.application.mappers.irole_mapper import IRoleMapper
from app.core.domain.entities.role import Role

class RoleMapper(IRoleMapper):
    def create_dto_to_entity(self, dto: CreateRoleDTO) -> Role:
        """Maps CreateRoleDTO to Role entity"""
        return Role(
            name=dto.name.lower(),
            description=dto.description,
            permissions=dto.permissions or None
        )

    def update_dto_to_entity(self, role: Role, dto: UpdateRoleDTO) -> Role:
        """Maps UpdateRoleDTO to existing Role entity"""
        if dto.name is not None:
            role.name = dto.name.lower()
        if dto.description is not None:
            role.description = dto.description
        if dto.permissions is not None:
            role.permissions = dto.permissions
        return role

    def entity_to_dto(self, role: Role) -> RoleDTO:
        """Maps Role entity to RoleDTO"""
        return RoleDTO(
            id=role.id,
            name=role.name,
            permissions=role.permissions or None
        )

    def entity_to_detail_dto(self, role: Role) -> RoleDetailDTO:
        """Maps Role entity to RoleDetailDTO"""
        return RoleDetailDTO(
            id=role.id,
            name=role.name,
            description=role.description,
            permissions=role.permissions or None,
            created_at=role.created_at,
            updated_at=role.updated_at
        )