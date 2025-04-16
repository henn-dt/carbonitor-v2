import 'vue-router'
import { Permission } from '@/types/permissions/PermissionEnum'

// Extend the meta fields for route records
declare module 'vue-router' {
  interface RouteMeta {
    // Authentication requirements
    requiresAuth?: boolean
    requiresAdmin?: boolean
    
    // Permission requirements
    requiresPermission?: Permission
    requiresPermissions?: Permission[]
    requireAllPermissions?: boolean
  }
}