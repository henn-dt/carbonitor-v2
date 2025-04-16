// frontend/src/types/buildup/IBuildup.ts

import type { Assembly, EPD, ReferenceSource } from "lcax";

export type ReferenceSourceForProduct = ReferenceSource<EPD>
  
export interface IBuildup extends Omit<Assembly, 'id'| 'products' | 'results' | 'metaData'> {
    id : number;
    status: string;
    user_id_created: number;
    user_id_updated: number;
    products: Record<string, ReferenceSourceForProduct>;
    results : Record<string,  any> | null;
    metaData: Record<string, any> | null

    created_at?: string; // ISO date string from backend
    updated_at?: string; // ISO date string from backend
};