# app/core/application/services/ipermission_service.py
from typing import List, Set
from app.core.domain.enums.permissions import Permission
from abc import ABC, abstractmethod

class IPermissionService(ABC):
    abstractmethod
    def validate_permissions(self, permissions: List[Permission]) -> bool:
        """Validate if all permissions in the list are valid"""
        pass

    abstractmethod
    def get_all_permissions(self) -> Set[Permission]:
        """Get all available permissions"""
        pass

    abstractmethod
    def default_user_permissions(self) -> List[str]:
        """Get default user permissions"""
        pass
    
    abstractmethod
    def default_admin_permissions(self) -> List[str]:
        """Get default admin permissions"""
        pass