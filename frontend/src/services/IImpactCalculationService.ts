import type { IBuildup } from "@/types/buildup/IBuildup";
import type { IBuildupWithProcessedProducts } from "@/types/epdx/IBuildupWithProcessedProducts";
import type { ICalculatedImpact } from "@/types/epdx/ICalculatedImpact";
import type { IProductWithCalculatedImpacts } from "@/types/epdx/IProductWithCalculatedImpacts";
import type { EPD, ImpactCategoryKey, LifeCycleStage } from "lcax";

/**
 * Service interface for impact calculations
 */
export interface IImpactCalculationService {
    /**
     * Converts an EPD string to an EPD object
     * @param epdString The EPD data as a JSON string
     * @returns The parsed EPD object or null if parsing fails
     */
    parseEpdString(epdData: string | object): EPD | null;

    /**
     * Calculates impacts grouped by lifecycle stages for a given EPD
     * @param epd The EPD object
     * @returns Record of impact categories with calculated impact values by lifecycle group
     */
    calculateImpacts(epd: EPD | null): Record<ImpactCategoryKey, ICalculatedImpact>;

    /**
     * Gets the impact value for a specific category and lifecycle stage
     * @param epd The EPD object
     * @param impactCategory The impact category key
     * @param stage The lifecycle stage
     * @returns The impact value or 0 if not found
     */
    getImpactValue(epd: EPD | null, impactCategory: ImpactCategoryKey, stage: LifeCycleStage): number;

    /**
     * Gets the lifecycle stage groups used for calculations
     * @returns Record of lifecycle stage groups
     */
    getLifecycleGroups(): Record<string, LifeCycleStage[]>;

    /**
     * Processes products to add EPD objects and calculated impacts
     * @param products Array of products to process
     * @returns Array of products with EPD objects and calculated impacts
     */
    processProducts<T extends { epdx: string | object }>(products: T[]): (T & IProductWithCalculatedImpacts)[];


    processSingleBuildupImpacts(buildup: IBuildup): Promise<IBuildupWithProcessedProducts> 
   
    /**
     * Processes buildups to add product objects, their EPD and calculated impacts
     * @param buildups Array of buildups to process
     * @returns Array of buildups with products, EPD objects and calculated impacts
     */
    processBuildupsImpacts(buildups: IBuildup[]): Promise<(IBuildupWithProcessedProducts)[]>;

}