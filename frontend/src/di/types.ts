
// src/di/types.ts
export const TYPES = {
    //repo types
    HttpClient: Symbol.for('HttpClient'),
    BaseRepository: Symbol.for('BaseRepository'),
    AuthRepository: Symbol.for('AuthRepository'),
    ProductRepository: Symbol.for('ProductRepository'),
    BuildupRepository: Symbol.for('BuildupRepository'),
    UserRepository: Symbol.for('UserRepository'),
    CategoryRepository: Symbol.for('CategoryRepository'),
    //service types
    AuthService: Symbol.for('AuthService'),
    StorageService: {
        Persistent: Symbol.for('PersistentStorageService'),
        Session: Symbol.for('SessionStorageService')
    },
    PermissionService: Symbol.for('PermissionService'),
    ProductService: Symbol.for('ProductService'),
    BuildupService: Symbol.for('BuildupService'),
    UserService: Symbol.for('UserService'),
    ImpactCalculationService: Symbol.for('ImpactCalculationService'),
    CategoryService: Symbol.for('CategoryService'),
    ProductMappingService: Symbol.for('ProductMappingService'),
    ProductSnapshotService: Symbol.for('ProductSnapshotService'),
    BuildupProcessService: Symbol.for('BuildupProcessService')
    
};
