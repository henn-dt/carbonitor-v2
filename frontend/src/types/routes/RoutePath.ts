/**
 * Route path constants
 */
export const RoutePath = {
    // Base paths
    BASE: '/',
    AUTH: '/auth',
    ADMIN: '/admin',
    
    // Auth
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    
    // Main
    HOME: '/',
    
    // User Section (both full paths and segments)
    PRODUCTS_FULL: '/products',
    BUILDUPS_FULL: '/buildups',
    MODELS_FULL: '/models',
    CATEGORIES_FULL: '/categories',
    
    // Path segments (for nested routes)
    PRODUCTS_SEGMENT: 'products',
    BUILDUPS_SEGMENT: 'buildups',
    MODELS_SEGMENT: 'models',
    CATEGORIES_SEGMENT: 'categories',
    
    // Admin Section (both full paths and segments)
    ADMIN_DASHBOARD_FULL: '/admin',
    ADMIN_USERS_FULL: '/admin/users',
    ADMIN_ROLES_FULL: '/admin/roles',
    ADMIN_PRODUCTS_FULL: '/admin/products',
    
    // Admin segments (for nested routes)
    ADMIN_USERS_SEGMENT: 'users',
    ADMIN_ROLES_SEGMENT: 'roles',
    ADMIN_PRODUCTS_SEGMENT: 'products',
    
    // Special
    EMPTY: '',
  } as const;