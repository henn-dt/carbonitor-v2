import type { IProduct } from '@/types/product/IProduct';
import type { IProductWithCalculatedImpacts } from './IProductWithCalculatedImpacts';
/**
 * Interface for buildups with processed products
 */
export interface IBuildupWithProcessedProducts {
    id: number // reference to original buildup
    mappedProducts: Record<string, (IProduct & IProductWithCalculatedImpacts)[]>;
    processedProducts: (IProduct & IProductWithCalculatedImpacts)[];
    isFullyProcessed: boolean;
    lastLocalUpdate?: string; //ISO formatted datetime
}