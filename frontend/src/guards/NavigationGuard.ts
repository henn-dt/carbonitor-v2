import type { RouteLocationNormalized, NavigationGuardNext, Router } from 'vue-router'
import { container } from '@/di/container'
import { TYPES } from '@/di/types'
import type { IAuthService } from '@/services/IAuthService'
import type { IPermissionService } from '@/services/IPermissionService'
import { Permission } from '@/types/permissions/PermissionEnum'
import { Routes } from '@/types/routes/Routes'
import { RoutePath } from '@/types/routes/RoutePath'
import { getAuthStore } from '@/stores/storeAccessor'

/**
 * Determines the appropriate redirect path based on access denial context
 */
function getRedirectPath(permissionService: IPermissionService, to: RouteLocationNormalized, userPermissions: Permission[]):
typeof Routes.HOME | typeof Routes.ADMIN_DASHBOARD {
  // For admin routes, redirect to admin dashboard if they have general admin access
  if (to.path.startsWith(RoutePath.ADMIN) && permissionService.hasPermission(userPermissions, Permission.ADMIN)) {
    return Routes.ADMIN_DASHBOARD;
  }
  
  // Default fallback for authenticated users
  return Routes.HOME;
}

/**
 * Sets up all navigation guards for the router
 */
export default function setupNavigationGuards(router: Router): void {
  router.beforeEach(async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
    
    // Initialize auth service and get current state
    const authStore = getAuthStore();
    const authService = container.get<IAuthService>(TYPES.AuthService);
    await authService.initAuthData();
    const isAuthenticated = authStore.isLoggedIn;
    const userPermissions = authStore.getPermissions || [];
    const permissionService = container.get<IPermissionService>(TYPES.PermissionService);
    
    // STEP 1: Handle authentication state
    // -------------------------------------------------------
    
    // Store intended destination for post-login redirect (for all routes requiring auth)
    if (!isAuthenticated && to.matched.some(record => record.meta.requiresAuth || record.meta.requiresAdmin)) {
      sessionStorage.setItem('redirectPath', to.fullPath);
    }
    
    // Handle auth routes by path instead of name for more reliability
    const isLoginPage = to.path === Routes.LOGIN.path;
    const isRegisterPage = to.path === Routes.REGISTER.path;
    
    if (isLoginPage || isRegisterPage) {
      if (isAuthenticated) {
        const redirectPath = sessionStorage.getItem('redirectPath');
        sessionStorage.removeItem('redirectPath');
        if (redirectPath) {
          return next(redirectPath);
        } else {
          return next(Routes.HOME.path);
        }
      }
      return next();
    }
    
    // Check authentication for protected routes
    if (!isAuthenticated) {
      if (to.matched.some(record => record.meta.requiresAuth || record.meta.requiresAdmin)) {
        return next(Routes.LOGIN.path);
      }
      return next();
    }
    
    // STEP 2: Check permissions for each matched route
    // -------------------------------------------------------
    for (const record of to.matched) {
      if (!permissionService.hasRouteAccess(userPermissions, record.meta)) {
        const redirectRoute = getRedirectPath(permissionService, to, userPermissions);
        return next(redirectRoute.path);
      }
    }
    next();
  });
  
  // Global error handler
  router.onError((error) => {
    console.error('Navigation error:', error);
    router.push(Routes.HOME);
  });
}