# app/core/application/mappers/dto_entity_mappers/irole_mapper.py
from abc import ABC, abstractmethod

from app.core.application.dtos.role.create_role_dto import CreateRoleDTO
from app.core.application.dtos.role.update_role_dto import UpdateRoleDTO
from app.core.application.dtos.role.role_dto import RoleDTO, RoleDetailDTO
from app.core.domain.entities.role import Role

class IRoleMapper(ABC):
    @abstractmethod
    def create_dto_to_entity(self, dto: CreateRoleDTO) -> Role:
        """Maps CreateRoleDTO to Role entity"""
        pass

    @abstractmethod
    def update_dto_to_entity(self, role: Role, dto: UpdateRoleDTO) -> Role:
        """Maps UpdateRoleDTO to existing Role entity"""
        pass

    @abstractmethod
    def entity_to_dto(self, role: Role) -> RoleDTO:
        """Maps Role entity to RoleDTO"""
        pass

    @abstractmethod
    def entity_to_detail_dto(self, role: Role) -> RoleDetailDTO:
        """Maps Role entity to RoleDetailDTO"""
        pass