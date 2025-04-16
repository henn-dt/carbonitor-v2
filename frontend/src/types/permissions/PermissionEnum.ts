export enum Permission {
    // User permissions
    USER_CREATE = "user:create",
    USER_READ = "user:read",
    USER_UPDATE = "user:update",
    USER_DELETE = "user:delete",
    USER_ALL = "user:all",
    
    // Role permissions
    ROLE_CREATE = "role:create",
    ROLE_READ = "role:read",
    ROLE_UPDATE = "role:update",
    ROLE_DELETE = "role:delete",
    ROLE_ALL = "role:all",

    // User roles permissions
    USER_ROLES_CREATE = "user_roles:create",
    USER_ROLES_READ = "user_roles:read",
    USER_ROLES_UPDATE = "user_roles:update",
    USER_ROLES_DELETE = "user_roles:delete",
    USER_ROLES_ALL = "user_roles:all",

    // Product permissions
    PRODUCT_CREATE = "product:create",
    PRODUCT_READ = "product:read",
    PRODUCT_UPDATE = "product:update",
    PRODUCT_DELETE = "product:delete",
    PRODUCT_ALL = "product:all",
    
    // Admin permissions
    ADMIN = "admin:access",
    ADMIN_USERS = "admin_users:access",
    ADMIN_ROLES = "admin_roles:access",
    ADMIN_USER_ROLES = "admin_user_roles:access",
    ADMIN_PRODUCTS = "admin_products:access",

    // Buildup permissions
    BUILDUP_CREATE = "buildup:create",
    BUILDUP_READ = "buildup:read",
    BUILDUP_UPDATE = "buildup:update",
    BUILDUP_DELETE = "buildup:delete",
    BUILDUP_ALL = "buildup:all",

    // Model permissions
    MODEL_CREATE = "model:create",
    MODEL_READ = "model:read",
    MODEL_UPDATE = "model:update",
    MODEL_DELETE = "model:delete",
    MODEL_ALL = "model:all",

    // Category permissions
    CATEGORY_CREATE = "category:create",
    CATEGORY_READ = "category:read",
    CATEGORY_UPDATE = "category:update",
    CATEGORY_DELETE = "category:delete",
    CATEGORY_ALL = "category:all",
}