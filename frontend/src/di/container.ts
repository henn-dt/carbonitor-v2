// src/di/container.ts
import { Container } from 'inversify';
import { TYPES } from './types';
import type { IAuthService } from '@/services/IAuthService';
import type { IAuthRepository } from '@/repositories/IAuthRepository';
import type { IStorageService } from '@/services/IStorageService';
import { AuthService } from '@/services/AuthService';
import { AuthRepository } from '@/repositories/AuthRepository';
import { CookieStorageService } from '@/services/CookieStorageService';
import { WebStorageService } from '@/services/WebStorageService';
import type { IHttpClient } from '@/repositories/IHttpClient';
import { BaseRepository } from '@/repositories/BaseRepository';
import { HttpClient } from '@/repositories/HttpClient';
import type { IPermissionService } from '@/services/IPermissionService';
import { PermissionService } from '@/services/PermissionService';
import type { IProductRepository } from '@/repositories/IProductRepository';
import { ProductRepository } from '@/repositories/ProductRepository';
import type { IProductService } from '@/services/IProductService';
import { ProductService } from '@/services/ProductService';
import type { IUserRepository } from '@/repositories/IUserRepository';
import { UserRepository } from '@/repositories/UserRepository';
import { UserService } from '@/services/UserService';
import type { IUserService } from '@/services/IUserService';
import type { IImpactCalculationService } from '@/services/IImpactCalculationService';
import { ImpactCalculationService } from '@/services/ImpactCalculationService';
import type { ICategoryRepository } from '@/repositories/ICategoryRepository';
import { CategoryRepository } from '@/repositories/CategoryRepository';
import type { ICategoryService } from '@/services/ICategoryService';
import { CategoryService } from '@/services/CategoryService';
import type { IBuildupRepository } from '@/repositories/IBuildupRepository';
import { BuildupRepository } from '@/repositories/BuildupRepository';
import type { IBuildupService } from '@/services/IBuildupService';
import { BuildupService } from '@/services/BuildupService';
import type { IProductMappingService } from '@/services/IProductMappingService';
import { ProductMappingService } from '@/services/ProductMappingService';
import type { IProductSnapshotService } from '@/services/IProductSnapshotService';
import { ProductSnapshotService } from '@/services/ProductSnapshotService';
import { BuildupProcessService } from "@/services/BuildupProcessService";
import type { IBuildupProcessService } from '@/services/IBuildupProcessService';

const container = new Container();

// Repository bindings
container.bind<IHttpClient>(TYPES.HttpClient).to(HttpClient).inSingletonScope();
container.bind<BaseRepository>(TYPES.BaseRepository).to(BaseRepository);
container.bind<IAuthRepository>(TYPES.AuthRepository).to(AuthRepository);
container.bind<IProductRepository>(TYPES.ProductRepository).to(ProductRepository);
container.bind<IUserRepository>(TYPES.UserRepository).to(UserRepository);
container.bind<ICategoryRepository>(TYPES.CategoryRepository).to(CategoryRepository);
container.bind<IBuildupRepository>(TYPES.BuildupRepository).to(BuildupRepository);

// Storage bindings
container.bind<IStorageService>(TYPES.StorageService.Persistent).to(CookieStorageService);
container.bind<IStorageService>(TYPES.StorageService.Session).to(WebStorageService);
container.bind<string>('StorageType').toConstantValue('session');

// Service bindings
container.bind<IAuthService>(TYPES.AuthService).to(AuthService);
container.bind<IUserService>(TYPES.UserService).to(UserService);
container.bind<IPermissionService>(TYPES.PermissionService).to(PermissionService);
container.bind<IProductService>(TYPES.ProductService).to(ProductService);
container.bind<IProductMappingService>(TYPES.ProductMappingService).to(ProductMappingService);
container.bind<IProductSnapshotService>(TYPES.ProductSnapshotService).to(ProductSnapshotService);

container.bind<IImpactCalculationService>(TYPES.ImpactCalculationService).to(ImpactCalculationService);

container.bind<IBuildupService>(TYPES.BuildupService).to(BuildupService);
container.bind<IBuildupProcessService>(TYPES.BuildupProcessService).to(BuildupProcessService);

container.bind<ICategoryService>(TYPES.CategoryService).to(CategoryService);

export { container };