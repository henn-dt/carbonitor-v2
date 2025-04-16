// src/services/IProductService.ts
import type { IProduct } from '@/types/product/IProduct';

export interface IProductService {
  getProducts(): Promise<IProduct[]>;
  getProductById(id: number): Promise<IProduct>;
  createProduct(product: Partial<IProduct>): Promise<IProduct>;
  updateProduct(id: number, product: Partial<IProduct>): Promise<IProduct>;
  deleteProduct(id: number): Promise<boolean>;
  deleteMultipleProducts(ids: number[]): Promise<{ success: number, failed: number }>;
  getProductsWithPagination(page: number, itemsPerPage: number): Promise<{
    products: IProduct[];
    total: number;
    page: number;
    totalPages: number;
  }>;
  getProductByUri(uri: string): Promise<IProduct> ;
  subscribeToProducts(callback: (products: IProduct[]) => void): () => void;
}