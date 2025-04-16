# app/infrastructure/services/permission_service.py
from typing import List, Set
from app.core.domain.enums.permissions import Permission
from app.core.application.services.ipermission_service import IPermissionService

class PermissionService(IPermissionService):
    RESOURCE_TYPES = ['user', 'product', 'role', 'user_roles']

    def __init__(self):
        self._all_permissions = set(Permission)
        self._default_user_perms = [
            Permission.PRODUCT_READ,
            Permission.PRODUCT_CREATE,
            Permission.PRODUCT_UPDATE,
            Permission.CATEGORY_READ,
            Permission.CATEGORY_CREATE,
            Permission.CATEGORY_UPDATE
        ]
        self._default_admin_perms = [
            Permission.USER_ALL,
            Permission.ROLE_ALL,
            Permission.USER_ROLES_ALL,
            Permission.PRODUCT_ALL,
            Permission.CATEGORY_ALL,
            Permission.ADMIN,
            Permission.ADMIN_USERS,
            Permission.ADMIN_ROLES,
            Permission.ADMIN_USER_ROLES,
            Permission.ADMIN_PRODUCTS
        ]

    def validate_permissions(self, permissions: List[Permission]) -> bool:
        if not permissions:
            return True

        # Validate all permissions exist
        if not all(perm in self._all_permissions for perm in permissions):
            return False

        # Check for conflicting resource permissions
        perm_values = {p.value for p in permissions}
        return not any(
            f"{resource}:all" in perm_values and
            any(p.startswith(f"{resource}:") and p != f"{resource}:all"
                for p in perm_values)
            for resource in self.RESOURCE_TYPES
        )

    def get_all_permissions(self) -> Set[Permission]:
        return self._all_permissions
    
    def default_user_permissions(self) -> List[str]:
        return [p.value for p in self._default_user_perms]
    
    def default_admin_permissions(self) -> List[str]:
        return [p.value for p in self._default_admin_perms]