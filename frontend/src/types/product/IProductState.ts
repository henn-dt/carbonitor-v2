import type { IProduct } from "@/types/product/IProduct";

export interface IProductState {
    products: IProduct[];
    selectedProduct: IProduct | null;
    loading: boolean;
    error: string | null;
    needsRefresh : boolean;
    totalProducts: number;
    currentPage: number;
    itemsPerPage: number;
    lastFetchTimestamp: number | null;
}