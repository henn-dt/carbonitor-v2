import { Permission } from "@/types/permissions/PermissionEnum";
import type { IPermissionService } from "@/services/IPermissionService";
import type { RouteMeta } from "vue-router";
import { injectable } from "inversify";

@injectable()
export class PermissionService implements IPermissionService {
    /**
     * Checks if a user has a specific permission
     */
    hasPermission(userPermissions: Permission[], permission: Permission): boolean {
      if (userPermissions.includes(permission)) {
          return true;
      }
      const [resourceType] = permission.split(':');
      return userPermissions.some(userPermission => {
          const [userResourceType, userAction] = userPermission.split(':');
          return userResourceType === resourceType && userAction === 'all';
      });
    }
    
    /**
     * Checks if a user has any of the specified permissions
     */
    hasAnyPermission(userPermissions: Permission[], permissions: Permission[]): boolean {
      if (permissions.length === 0) return true;
      return permissions.some(permission => this.hasPermission(userPermissions, permission));
    }
    
    /**
     * Checks if a user has all of the specified permissions
     */
    hasAllPermissions(userPermissions: Permission[], permissions: Permission[]): boolean {
      if (permissions.length === 0) return true;
      return permissions.every(permission => this.hasPermission(userPermissions, permission));
    }
    
    /**
     * Checks if a value is a valid Permission enum value
     */
    isValidPermission(value: unknown): value is Permission {
      return typeof value === 'string' && Object.values(Permission).includes(value as Permission);
    }
    
    /**
     * Checks if a user has access to a route based on its meta requirements
     */
    hasRouteAccess(userPermissions: Permission[], routeMeta: RouteMeta): boolean {
      // Check admin requirement
      if (routeMeta.requiresAdmin && !this.hasPermission(userPermissions, Permission.ADMIN)) {
        return false;
      }
      
      // Check single permission
      const singlePermission = routeMeta.requiresPermission;
      if (singlePermission && this.isValidPermission(singlePermission)) {
        if (!this.hasPermission(userPermissions, singlePermission)) {
          return false;
        }
      }
      
      // Check multiple permissions
      const multiplePermissions = routeMeta.requiresPermissions as Permission[] | undefined;
      if (Array.isArray(multiplePermissions) && multiplePermissions.length > 0) {
        const requireAll = routeMeta.requireAllPermissions === true;
        
        if (requireAll) {
          if (!this.hasAllPermissions(userPermissions, multiplePermissions)) {
            return false;
          }
        } else {
          if (!this.hasAnyPermission(userPermissions, multiplePermissions)) {
            return false;
          }
        }
      }
      
      return true;
    }
}