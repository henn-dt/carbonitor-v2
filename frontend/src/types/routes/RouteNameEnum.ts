/**
 * Centralized route names to avoid typos and enable refactoring
 */
export enum RouteName {
    //1.------------- Auth ----------------------
    LOGIN = 'login',
    REGISTER = 'register',

    //2.------------- Main ----------------------
    HOME = 'home',
        // User Section
    PRODUCTS = 'products',
    BUILDUPS = 'buildups',
    MODELS = 'models',
    CATEGORIES = 'categories',
    
    //3.------------ Admin Section ---------------
    ADMIN_DASHBOARD = 'admin-dashboard',
    ADMIN_USERS = 'admin-users',
    ADMIN_ROLES = 'admin-roles',
    ADMIN_PRODUCTS = 'admin-products',
}