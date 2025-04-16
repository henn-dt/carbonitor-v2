// src/services/ProductService.ts
import { injectable, inject } from 'inversify';
import type { IProductService } from './IProductService';
import type { IProductRepository } from '@/repositories/IProductRepository';
import type { IProduct } from '@/types/product/IProduct';
import { TYPES } from '@/di/types';
import { Product } from '@/types/product/Product';
import { useProductStore } from '@/stores/productStore';
import { getProductStore } from '@/stores/storeAccessor';
import type { EPD } from 'lcax';

@injectable()
export class ProductService implements IProductService {
    constructor(
        @inject(TYPES.ProductRepository) private productRepository: IProductRepository
    ) {}
    //async initProducts(): Promise
    async getProducts(): Promise<IProduct[]> {
        try {
            const productStore = getProductStore();

            // If we already have products loaded, return them
            if (productStore.products.length > 0 && !productStore.needsRefresh) {

                return [...productStore.products]; // Return a copy to prevent accidental mutations
            }

            productStore.setLoading(true);
            
            const products = await this.productRepository.getProducts();
            const productDTOs = products.map(product => new Product(product));
            
            // Update the store state
            productStore.setProducts(productDTOs);
            productStore.setLoading(false);
            productStore.setNeedsRefresh(false);
            productStore.setLastFetchTimestamp(new Date().getTime());
            
            return productDTOs;
        } catch (error) {
            const productStore = getProductStore();
            productStore.setLoading(false);          
            productStore.setError(error instanceof Error ? error.message : 'Failed to fetch products');
            throw error;
        }
    }

    subscribeToProducts(callback: (products: IProduct[]) => void): () => void {
        const productStore = getProductStore();
        
        // Create a watcher function that calls the callback whenever categories change
        const unsubscribe = productStore.$subscribe(
            (mutation, state) => {
                callback([...state.products]);
            }
        );
        
        // Immediately call with current data
        callback([...productStore.products]);
        
        // Return the unsubscribe function
        return unsubscribe;
    }

    async getProductById(id: number): Promise<IProduct> {
        try {
            const productStore = getProductStore();
            
            // Check if product is already in the store
            const cachedProduct = productStore.products.find(p => p.id === id);
            if (cachedProduct) {
                productStore.setSelectedProduct(cachedProduct);
                return cachedProduct;
            }
            
            productStore.setLoading(true);
            const product = await this.productRepository.getProductById(id);
            const productDTO = new Product(product);
            
            // Update the store
            productStore.setSelectedProduct(productDTO);
            productStore.setLoading(false);
            
            return productDTO;
        } catch (error) {
            const productStore = getProductStore();
            productStore.setLoading(false);
            productStore.setError(error instanceof Error ? error.message : `Failed to fetch product #${id}`);
            throw error;
        }
    }

    // Uri is a string formatted as <epd_sourceName>.<epd_id>
    async getProductByUri(uri: string): Promise<IProduct> {
        try {
            const productStore = getProductStore();
            
            // Check if product is already in the store
            const cachedProduct = productStore.products.find(p => `${p.epd_sourceName}.${p.epd_id}` === uri);
            if (cachedProduct) {
                productStore.setSelectedProduct(cachedProduct);
                return cachedProduct;
            }
            
            productStore.setLoading(true);
            
            // Split the URI into source name and ID
            const [epd_sourceName, epd_id] = uri.split('.');
            if (!epd_sourceName || !epd_id) {
                throw new Error(`Invalid URI format: ${uri}. Expected format: <epd_sourceName>.<epd_id>`);
            }
            
            const product = await this.productRepository.getProductByUri(uri);
            const productDTO = new Product(product);
            
            // Update the store
            productStore.setSelectedProduct(productDTO);
            productStore.setLoading(false);
            
            return productDTO;
        } catch (error) {
            const productStore = getProductStore();
            productStore.setLoading(false);
            productStore.setError(error instanceof Error ? error.message : `Failed to fetch product with URI: ${uri}`);
            throw error;
        }
    }

    // move to ProductSnapshotService and to ProductSnapshotStore
    async convertEpdToProduct(epd : EPD) : Promise<IProduct> {
        try {
            const productSnapshotStore = getProductStore();
        
            // convert validation function to separate function
            // Check if product with this EPD ID and other key parameters is already in the store
            const cachedProduct = productSnapshotStore.products.find(p => {
                // Basic checks for EPD id, version and source name
                const basicMatch = 
                    p.epd_id === epd.id && 
                    p.epd_version === epd.version && 
                    p.epd_sourceName === (epd.source?.name || '');
                
                if (!basicMatch) return false;
                
                // Check for metadata overrides match if they exist
                if (epd.metaData?.overrides) {
                    // Parse epdx from string to object if it's a string
                    let parsedEpdx: any = null;
                    
                    try {
                        if (typeof p.epdx === 'string') {
                            parsedEpdx = JSON.parse(p.epdx);
                        } else {
                            // If it's already an object, use it directly
                            parsedEpdx = p.epdx;
                        }
                    } catch (e) {
                        // If parsing fails, assume no match
                        return false;
                    }
                    
                    // Compare metadata overrides if they exist in parsed epdx
                    if (!parsedEpdx?.metaData?.overrides) {
                        return false;
                    }
                    
                    // Compare the stringified versions for deep equality
                    return JSON.stringify(parsedEpdx.metaData.overrides) === 
                           JSON.stringify(epd.metaData.overrides);
                }
                
                // If no overrides to check, the basic match is sufficient
                return true;
            });

            if (cachedProduct) {
                productSnapshotStore.setSelectedProduct(cachedProduct);
                return cachedProduct;
            }


            productSnapshotStore.setLoading (true);

            const createdProduct = await this.productRepository.convertEpdToProduct(epd)
            const productDTO = new Product(createdProduct);

            // Update the store
            productSnapshotStore.addProduct(productDTO);
            productSnapshotStore.setLoading(false);
            
            return productDTO;

            }
            
            catch (error) {
                const productStore = getProductStore();
                productStore.setLoading(false);
                productStore.setError(
                    error instanceof Error 
                        ? error.message 
                        : `Failed to create product from EPD: ${epd.id}`
                );
                throw error;
            }
        }

    async createProduct(product: Partial<IProduct>): Promise<IProduct> {
        try {
            const productStore = getProductStore();
            productStore.setLoading(true);
            
            // Add timestamp and set status if not present
            if (!product.status) {
                product.status = 'active';
            }
            
            // Call repository to save in backend
            const createdProduct = await this.productRepository.createProduct(product);
            const productDTO = new Product(createdProduct);
            
            // Update the store
            productStore.addProduct(productDTO);
            productStore.setLoading(false);
            
            return productDTO;
        } catch (error) {
            const productStore = getProductStore();
            productStore.setLoading(false);
            productStore.setError(error instanceof Error ? error.message : 'Failed to create product');
            throw error;
        }
    }

    async updateProduct(id: number, product: Partial<IProduct>): Promise<IProduct> {
        try {
            const productStore = getProductStore();
            productStore.setLoading(true);
            
            // Call repository to update in backend
            const updatedProduct = await this.productRepository.updateProduct(id, product);
            const productDTO = new Product(updatedProduct);
            
            // Update the store
            productStore.updateProduct(productDTO);
            productStore.setLoading(false);
            
            return productDTO;
        } catch (error) {
            const productStore = getProductStore();
            productStore.setLoading(false);
            productStore.setError(error instanceof Error ? error.message : `Failed to update product #${id}`);
            throw error;
        }
    }

    async deleteProduct(id: number): Promise<boolean> {
        try {
            const productStore = getProductStore();
            productStore.setLoading(true);
            
            // Call repository to delete from backend
            const result = await this.productRepository.deleteProduct(id);
            
            if (result) {
                // Update the store by removing the product
                productStore.removeProduct(id);
            }
            
            productStore.setLoading(false);
            return result;
        } catch (error) {
            const productStore = getProductStore();
            productStore.setLoading(false);
            productStore.setError(error instanceof Error ? error.message : `Failed to delete product #${id}`);
            throw error;
        }
    }
    
    /**
     * Bulk delete multiple products
     */
    async deleteMultipleProducts(ids: number[]): Promise<{ success: number, failed: number }> {
        const result = { success: 0, failed: 0 };
        const productStore = getProductStore();
        productStore.setLoading(true);
        
        try {
            for (const id of ids) {
                try {
                    const deleted = await this.productRepository.deleteProduct(id);
                    if (deleted) {
                        productStore.removeProduct(id);
                        result.success++;
                    } else {
                        result.failed++;
                    }
                } catch (error) {
                    console.error(`Failed to delete product #${id}:`, error);
                    result.failed++;
                }
            }
            
            return result;
        } finally {
            productStore.setLoading(false);
        }
    }
    
    /**
     * Get products with pagination
     */
    async getProductsWithPagination(page: number, itemsPerPage: number): Promise<{
        products: IProduct[],
        total: number,
        page: number,
        totalPages: number
    }> {
        try {
            const productStore = getProductStore();
            productStore.setLoading(true);
            
            // For now, we'll use client-side pagination with all products
            // In a real app, you'd have a backend endpoint for pagination
            const allProducts = await this.getProducts();
            
            const startIndex = (page - 1) * itemsPerPage;
            const paginatedProducts = allProducts.slice(startIndex, startIndex + itemsPerPage);
            const totalPages = Math.ceil(allProducts.length / itemsPerPage);
            
            // Update store pagination info
            productStore.setPage(page);
            productStore.setItemsPerPage(itemsPerPage);
            
            productStore.setLoading(false);
            
            return {
                products: paginatedProducts,
                total: allProducts.length,
                page,
                totalPages
            };
        } catch (error) {
            const productStore = getProductStore();
            productStore.setLoading(false);
            productStore.setError(error instanceof Error ? error.message : 'Failed to fetch products');
            throw error;
        }
    }
}