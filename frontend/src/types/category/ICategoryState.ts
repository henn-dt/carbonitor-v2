import type { ICategory } from "./ICategory";

/**
 * State interface for tracking category state
 */
export interface ICategoryState {
    categories: ICategory[];
    selectedCategory?: ICategory | null;
    loading: boolean;
    error: string | null;
    needsRefresh : boolean;
    totalCategories: number;
    lastFetchTimestamp: number | null;  
  }