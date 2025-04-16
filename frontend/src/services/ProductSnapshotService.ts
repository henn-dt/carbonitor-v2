// src/services/ProductSNapshotService.ts
import { injectable, inject } from 'inversify';
import type { IProductRepository } from '@/repositories/IProductRepository';
import type { IProduct } from '@/types/product/IProduct';
import { TYPES } from '@/di/types';
import { Product } from '@/types/product/Product';
import { getProductStore } from '@/stores/storeAccessor';
import type { EPD } from 'lcax';
import type { IProductSnapshotService } from './IProductSnapshotService';

@injectable()
export class ProductSnapshotService implements IProductSnapshotService {
    constructor(
        @inject(TYPES.ProductRepository) private productRepository: IProductRepository
    ) {}

    public getProductSnapshotbyEpd(epd : EPD) : IProduct | null {
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
        } else {
            return null
        }
        
    }

    // move to ProductSnapshotService and to ProductSnapshotStore
    async convertEpdToProduct(epd : EPD) : Promise<IProduct> {
        try {

            const productSnapshotStore = getProductStore();
            const cachedProduct = this.getProductSnapshotbyEpd(epd)

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

}