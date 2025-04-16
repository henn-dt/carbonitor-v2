import { RouteName } from "@/types/routes/RouteNameEnum";
import { RoutePath } from "@/types/routes/RoutePath";

/**
 * Route structure for strongly-typed access to both path and name
 */
export const Routes = {
    // Auth
    LOGIN: { path: RoutePath.LOGIN, name: RouteName.LOGIN },
    REGISTER: { path: RoutePath.REGISTER, name: RouteName.REGISTER },
    
    // Main
    HOME: { path: RoutePath.HOME, name: RouteName.HOME },
    
    // User Section
    PRODUCTS: { 
      path: RoutePath.PRODUCTS_FULL, 
      name: RouteName.PRODUCTS,
      segment: RoutePath.PRODUCTS_SEGMENT 
    },
    BUILDUPS: { 
      path: RoutePath.BUILDUPS_FULL, 
      name: RouteName.BUILDUPS,
      segment: RoutePath.BUILDUPS_SEGMENT 
    },
    MODELS: { 
      path: RoutePath.MODELS_FULL, 
      name: RouteName.MODELS,
      segment: RoutePath.MODELS_SEGMENT 
    },
    CATEGORIES: { 
      path: RoutePath.CATEGORIES_FULL, 
      name: RouteName.CATEGORIES,
      segment: RoutePath.CATEGORIES_SEGMENT 
    },
    
    // Admin Section
    ADMIN_DASHBOARD: { 
      path: RoutePath.ADMIN_DASHBOARD_FULL, 
      name: RouteName.ADMIN_DASHBOARD,
      segment: RoutePath.EMPTY
    },
    ADMIN_USERS: { 
      path: RoutePath.ADMIN_USERS_FULL, 
      name: RouteName.ADMIN_USERS,
      segment: RoutePath.ADMIN_USERS_SEGMENT 
    },
    ADMIN_ROLES: { 
      path: RoutePath.ADMIN_ROLES_FULL, 
      name: RouteName.ADMIN_ROLES,
      segment: RoutePath.ADMIN_ROLES_SEGMENT
    },
    ADMIN_PRODUCTS: { 
      path: RoutePath.ADMIN_PRODUCTS_FULL, 
      name: RouteName.ADMIN_PRODUCTS,
      segment: RoutePath.ADMIN_PRODUCTS_SEGMENT
    },
  } as const;