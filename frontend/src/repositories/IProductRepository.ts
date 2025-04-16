// src/repositories/IProductRepository.ts
import type { IProduct } from '@/types/product/IProduct';

export interface IProductRepository {
    getProducts(): Promise<IProduct[]>;
    getProductById(id: number): Promise<IProduct>;
    getProductByUri(uri: string): Promise<IProduct>;
    convertEpdToProduct(epd : any) : Promise<IProduct>;
    createProduct(product: Partial<IProduct>): Promise<IProduct>;
    updateProduct(id: number, product: Partial<IProduct>): Promise<IProduct>;
    deleteProduct(id: number): Promise<boolean>;
}