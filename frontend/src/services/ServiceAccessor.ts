// frontend/src/services/serviceAccessor.ts

import { container } from '@/di/container';
import { TYPES } from '@/di/types';
import { createRefreshableService } from '@/composables/createRefreshableService';
import type { ICategoryService } from '@/services/ICategoryService';
import type { IProductService } from '@/services/IProductService';
import type { IBuildupService } from '@/services/IBuildupService';
import type { IBuildupProcessService } from './IBuildupProcessService';

// Type for the enhanced service
type RefreshableService<T> = T & {
    startAllBackgroundRefreshes: () => void;
    stopAllBackgroundRefreshes: () => void;
  };

// Singleton instances of enhanced services
let _categoryService: RefreshableService<ICategoryService> | null = null;
let _productService: RefreshableService<IProductService> | null = null;
let _buildupService: RefreshableService<IBuildupService> | null = null;
let _buildupProcessService: RefreshableService<IBuildupProcessService> | null = null;

// Get the enhanced Category Service
export function getCategoryService(): RefreshableService<ICategoryService> {
    if (!_categoryService) {
        // Get the raw service instance from the container
        const rawService = container.get<ICategoryService>(TYPES.CategoryService);
        
        // Enhance it with refreshable capabilities
        _categoryService = createRefreshableService(
            rawService,
            ['getCategories'],
            { refreshInterval: 5 * 60 * 1000 }
        );
    }
    return _categoryService;
}


// Get the enhanced Product Service
export function getProductService(): RefreshableService<IProductService> {
    if (!_productService) {
        // Get the raw service instance from the container
        const rawService = container.get<IProductService>(TYPES.ProductService);
        
        // Enhance it with refreshable capabilities
        _productService = createRefreshableService(
            rawService,
            ['getProducts'],
            { refreshInterval: 7 * 60 * 1000 }
        );
    }
    return _productService;
}

// Get the enhanced Product Service
export function getBuildupService(): RefreshableService<IBuildupService> {
    if (!_buildupService) {
        
        // Get the raw service instance from the container
        const rawService = container.get<IBuildupService>(TYPES.BuildupService);
        
        // Enhance it with refreshable capabilities
        _buildupService = createRefreshableService(
            rawService,
            ['getBuildups'],
            { refreshInterval: 4 * 60 * 1000 }
        );
    }
    return _buildupService;
}
export function getBuildupProcessService(): RefreshableService<IBuildupProcessService> {
    if (!_buildupProcessService) {
        
        // Get the raw service instance from the container
        const rawService = container.get<IBuildupProcessService>(TYPES.BuildupProcessService);
        
        // Enhance it with refreshable capabilities
        _buildupProcessService = createRefreshableService(
            rawService,
            ['processAllBuildups'],
            { refreshInterval: 4 * 60 * 1000 }
        );
    }
    return _buildupProcessService;
}


// Prefetch all data using the enhanced services
export function prefetchAllData() {
    // Start fetching data from all services
    console.log('pre-fetching all data')
    getCategoryService().getCategories();
    getProductService().getProducts();
    getBuildupService().getBuildups();
    getBuildupProcessService().processAllBuildups();
    // Add other services as needed
}

// Start background refreshes for all services
export function startAllBackgroundRefreshes() {
    getCategoryService().startAllBackgroundRefreshes();
    getProductService().startAllBackgroundRefreshes();
    getBuildupService().startAllBackgroundRefreshes();
    getBuildupProcessService().startAllBackgroundRefreshes();
    // Add other services
}

// Stop all background refreshes
export function stopAllBackgroundRefreshes() {
    getCategoryService().stopAllBackgroundRefreshes();
    getProductService().stopAllBackgroundRefreshes();
    getBuildupService().stopAllBackgroundRefreshes();
    getBuildupProcessService().startAllBackgroundRefreshes();
    // Add other services
}