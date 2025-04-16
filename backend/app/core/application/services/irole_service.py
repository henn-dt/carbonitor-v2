# app/core/application/services/irole_service.py

from typing import List, Optional, Set
from abc import ABC, abstractmethod
from app.core.application.dtos.role.create_role_dto import CreateRoleDTO
from app.core.application.dtos.role.update_role_dto import UpdateRoleDTO
from app.core.application.dtos.role.role_dto import RoleDTO, RoleDetailDTO

class IRoleService(ABC):
    """
    Interface defining the contract for role management operations.
    """
    
    @abstractmethod
    def create_role(self, dto: CreateRoleDTO) -> RoleDetailDTO:
        """
        Creates a new role with the provided details.
        
        Args:
            dto: Data transfer object containing role creation details
            
        Returns:
            Detailed information about the created role
            
        Raises:
            ValueError: If role name already exists or invalid permissions provided
        """
        pass
    
    @abstractmethod
    def create_role_with_preset(self, role_name: str, is_admin: bool = False) -> RoleDetailDTO:
        """
        Creates a new role with preset permissions based on admin status.
        
        Args:
            role_name: Name of the role to create
            is_admin: Whether to create an admin role with elevated permissions
            
        Returns:
            Detailed information about the created role
            
        Raises:
            ValueError: If role name already exists
        """
        pass
    
    @abstractmethod
    def get_role(self, role_id: int) -> Optional[RoleDetailDTO]:
        """
        Retrieves role information by ID.
        
        Args:
            role_id: ID of the role to retrieve
            
        Returns:
            Role details if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_all_roles(self) -> List[RoleDTO]:
        """
        Retrieves all available roles.
        
        Returns:
            List of all roles in the system
        """
        pass
    
    @abstractmethod
    def get_role_by_name(self, name: str) -> Optional[RoleDetailDTO]:
        """
        Retrieves role information by name.
        
        Args:
            name: Name of the role to retrieve
            
        Returns:
            Role details if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_available_permissions(self) -> Set[str]:
        """
        Retrieves all available permissions in the system.
        
        Returns:
            Set of permission strings
        """
        pass
    
    @abstractmethod
    def update_role(self, role_id: int, dto: UpdateRoleDTO) -> Optional[RoleDetailDTO]:
        """
        Updates an existing role with new details.
        
        Args:
            role_id: ID of the role to update
            dto: Data transfer object containing update details
            
        Returns:
            Updated role details if found, None if role doesn't exist
            
        Raises:
            ValueError: If invalid permissions provided
        """
        pass
    
    @abstractmethod
    def delete_role(self, role_id: int) -> None:
        """
        Deletes a role by ID.
        
        Args:
            role_id: ID of the role to delete
        """
        pass
    
    @abstractmethod
    def delete_role_by_name(self, role_name: str) -> None:
        """
        Deletes a role by name.
        
        Args:
            role_name: Name of the role to delete
        """
        pass
    
    @abstractmethod
    def check_or_create_role(self, role_name: str, is_admin: bool = False) -> str:
        """
        Checks if a role exists and creates it if it doesn't.
        
        Args:
            role_name: Name of the role to check/create
            is_admin: Whether to create as admin role if creation is needed
            
        Returns:
            Status message indicating whether role existed or was created
        """
        pass