import { inject, injectable } from "inversify";
import { TYPES } from "@/di/types";
import type { IProductMappingService } from "@/services/IProductMappingService";
import type { IImpactCalculationService } from "@/services/IImpactCalculationService";

import type { ICalculatedImpact } from "@/types/epdx/ICalculatedImpact";
import type { EPD, ImpactCategoryKey, LifeCycleStage } from "lcax";


import type { IProductWithCalculatedImpacts } from "@/types/epdx/IProductWithCalculatedImpacts";
import type { IBuildupWithProcessedProducts } from "@/types/epdx/IBuildupWithProcessedProducts";
import type { IBuildup } from "@/types/buildup/IBuildup";
import type { IProduct } from "@/types/product/IProduct";
import type { IMappedEntities } from "@/types/mapping/IMappedEntity";


/**
 * Implementation of the impact calculation service
 */
@injectable()
export class ImpactCalculationService implements IImpactCalculationService {
        constructor(
          @inject(TYPES.ProductMappingService) private productMappingService: IProductMappingService
        ) {}

    // Define lifecycle stage groups
    private readonly LIFECYCLE_GROUPS: Record<string, LifeCycleStage[]> = {
        Production: ['a1a3'],
        Construction: ['a4', 'a5'],
        Operation: ['b1', 'b2', 'b3', 'b4', 'b5'],
        Disassembly : ['c1', 'c2'],
        Disposal: ['c3', 'c4'],
        Reuse: ['d']
    };

    /**
     * Parse EPD string or object to EPD object
     */
    public parseEpdString(epdData: string | object): EPD | null {
        try {
            // If epdData is already an object, return it directly
            if (typeof epdData === 'object' && epdData !== null) {
                return epdData as EPD;
            }
            
            // Otherwise, try to parse it as a JSON string
            return JSON.parse(epdData as string) as EPD;
        } catch (error) {
            console.error('Error parsing EPD data:', error);
            return null;
        }
    }

    /**
     * Get impact value for a specific category and stage
     */
    public getImpactValue(epd: EPD | null, impactCategory: ImpactCategoryKey, stage: LifeCycleStage): number {
        if (!epd || !epd.impacts || !epd.impacts[impactCategory]) {
            return 0;
        }
        try {
            return epd.impacts[impactCategory][stage] || 0;
        } catch (error) {
            console.error(`Error getting impact value for ${impactCategory}:${stage}:`, error);
            return 0;
        }
    }

    /**
     * Calculate impacts grouped by lifecycle stages
     */
    public calculateImpacts(epd: EPD | null, quantity: number = 1): Record<ImpactCategoryKey, ICalculatedImpact> {
        const result: Record<ImpactCategoryKey, ICalculatedImpact> = {} as Record<ImpactCategoryKey, ICalculatedImpact>;
        if (!epd || !epd.impacts) {
            return result;
        }
        // Get all impact categories from the EPD
        const impactCategories = Object.keys(epd.impacts) as ImpactCategoryKey[];
        // Calculate impacts for each category
        impactCategories.forEach(category => {
            const calculatedImpact: ICalculatedImpact = {
                Production: 0,
                Construction: 0,
                Operation: 0 ,
                Disassembly: 0 ,
                Disposal: 0,
                Reuse: 0
            };
            // Sum up impacts for each lifecycle group
            Object.entries(this.LIFECYCLE_GROUPS).forEach(([groupName, stages]) => {
                const groupTotal = stages.reduce((sum, stage) => {
                    return sum + this.getImpactValue(epd, category, stage);
                }, 0);
                calculatedImpact[groupName as keyof ICalculatedImpact] = groupTotal * quantity;
            });
            result[category] = calculatedImpact;
        });
        return result;
    }

    /**
     * Get lifecycle groups
     */
    public getLifecycleGroups(): Record<string, LifeCycleStage[]> {
        return this.LIFECYCLE_GROUPS;
    }

    /**
   * Process products to add EPD objects and calculated impacts
   */
    public processProducts<T extends { epdx: string | object }>(products: T[], quantities?:number[]): (T & IProductWithCalculatedImpacts)[] {
        return products.map((product , index)=> {
            // Get quantity for this product (default to 1 if not provided)
            const quantity = quantities && quantities[index] !== undefined ? quantities[index] : 1;
            // Parse EPD string or object to EPD object
            const epdObject = this.parseEpdString(product.epdx);
            // Calculate impacts for the EPD
            const calculatedImpacts = this.calculateImpacts(epdObject, quantity);
            // Return the extended product object
            return {
                ...product,
                epdObject,
                calculatedImpacts,
                quantity
            };
        });
    }


    public async processSingleBuildupImpacts(buildup: IBuildup): Promise<IBuildupWithProcessedProducts> {
        const id = buildup.id
        if (buildup.results === null) {
            // Return a partially processed buildup without the processed products
            return {
                id: id,
                mappedProducts: {},
                processedProducts: [],
                isFullyProcessed: false
            };
        }
        
        try {
            // First, map the product references to actual products
            const mappedEntities: IMappedEntities<IProduct> = await this.productMappingService.mapProducts(
                buildup.products, 
                buildup.results
            );
            
            // Extract all products and their quantities from the mapped entities
            const productsArray: IProduct[] = [];
            const quantitiesArray: number[] = [];
            
            // Process mapped entities for single buildup
            Object.values(mappedEntities).forEach(mappedEntitiesForGroup => {
                mappedEntitiesForGroup.forEach(mappedEntity => {
                    productsArray.push(mappedEntity.entity);
                    quantitiesArray.push(mappedEntity.quantity);
                });
            });
            
            // Process the products with their quantities to calculate impacts
            const processedProducts = this.processProducts(
                productsArray,
                quantitiesArray
            );
            
            // Convert the mappedEntities format to the new mappedProducts format
            const mappedProducts: Record<string, (IProduct & IProductWithCalculatedImpacts)[]> = {};
            
            // Create a lookup map to find processed product by original product
            const processedProductMap = new Map<IProduct, IProduct & IProductWithCalculatedImpacts>();
            productsArray.forEach((product, index) => {
                processedProductMap.set(product, processedProducts[index]);
            });
            
            // Transform the mappedEntities into the mappedProducts format
            Object.entries(mappedEntities).forEach(([mappingId, entitiesForGroup]) => {
                mappedProducts[mappingId] = entitiesForGroup.map(mappedEntity => {
                    const processedProduct = processedProductMap.get(mappedEntity.entity);
                    if (!processedProduct) {
                        throw new Error(`Could not find processed product for entity`);
                    }
                    return processedProduct;
                });
            });
            
            return {
                id,
                mappedProducts,
                processedProducts,
                isFullyProcessed: true
            };
        } catch (error) {
            // If there's an error in processing, return a partially processed buildup
            console.error("Error processing buildup:", error);
            return {
                id,
                mappedProducts: {},
                processedProducts: [],
                isFullyProcessed: false
            };
        }
    }

    public async processBuildupsImpacts(buildups: IBuildup[]): Promise<IBuildupWithProcessedProducts[]> {
        // Process all buildups concurrently
        const processedBuildups = await Promise.all(
            buildups.map(async (buildup) => {
                try {
                    return await this.processSingleBuildupImpacts(buildup);
                } catch (error) {
                    console.error(`Error processing buildup ${buildup.id}:`, error);
                    // Return a partially processed buildup in case of error
                    return {
                        id : buildup.id,
                        mappedProducts: {},
                        processedProducts: [],
                        isFullyProcessed: false
                    };
                }
            })
        );
        
        return processedBuildups;
    }
}