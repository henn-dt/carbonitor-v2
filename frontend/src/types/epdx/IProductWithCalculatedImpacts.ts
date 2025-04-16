import type { EPD, ImpactCategoryKey } from 'lcax';
import type { ICalculatedImpact } from '@/types/epdx/ICalculatedImpact';
/**
 * Interface for products with calculated impacts
 */
export interface IProductWithCalculatedImpacts {
    epdObject: EPD | null;
    calculatedImpacts: Record<ImpactCategoryKey, ICalculatedImpact>;
    quantity: number;
}