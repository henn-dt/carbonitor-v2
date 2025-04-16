import { Permission } from '@/types/permissions/PermissionEnum'
import type { RouteMeta } from 'vue-router'

export interface IPermissionService {
  /**
   * Checks if a user has a specific permission
   */
  hasPermission(userPermissions: Permission[], permission: Permission): boolean;
  
  /**
   * Checks if a user has any of the specified permissions
   */
  hasAnyPermission(userPermissions: Permission[], permissions: Permission[]): boolean;
  
  /**
   * Checks if a user has all of the specified permissions
   */
  hasAllPermissions(userPermissions: Permission[], permissions: Permission[]): boolean;
  
  /**
   * Checks if a value is a valid Permission enum value
   */
  isValidPermission(value: unknown): value is Permission;
  
  /**
   * Checks if a user has access to a route based on its meta requirements
   */
  hasRouteAccess(userPermissions: Permission[], routeMeta: RouteMeta): boolean;
}