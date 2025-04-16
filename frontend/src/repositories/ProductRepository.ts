// src/repositories/ProductRepository.ts
import type { IProductRepository } from './IProductRepository';
import { BaseRepository } from './BaseRepository';
import type { IProduct } from '@/types/product/IProduct';
import { inject, injectable } from 'inversify';
import type { IHttpClient } from './IHttpClient';
import { TYPES } from '@/di/types';

@injectable()
export class ProductRepository extends BaseRepository implements IProductRepository {
    private productUrl: string;

    constructor(
        @inject(TYPES.HttpClient) httpClient: IHttpClient
    ) {
        super(httpClient);
        this.productUrl = `${this.axios.defaults.baseURL}/products/`;
    }

    async getProducts(): Promise<IProduct[]> {
        try {
            const { data } = await this.axios.get<IProduct[]>(this.productUrl);
            return data;
        } catch (error) {
            console.error('Error fetching products:', error);
            throw error;
        }
    }

    async convertEpdToProduct(epd : any) : Promise<IProduct> {
        try {
            const { data } = await this.axios.post<IProduct>(`${this.productUrl}/epd`, epd);
            return data;
        } catch (error) {
            console.error(`Error creating product with from epd with id ${epd.id}:`, error);
            throw error;
        }
        }

    async getProductById(id: number): Promise<IProduct> {
        try {
            const { data } = await this.axios.get<IProduct>(`${this.productUrl}/${id}`);
            return data;
        } catch (error) {
            console.error(`Error fetching product with id ${id}:`, error);
            throw error;
        }
    }

    async getProductByUri(uri: string): Promise<IProduct> {
        try {
            const { data } = await this.axios.get<IProduct>(`${this.productUrl}/uri/${uri}`);
            return data;
        } catch (error) {
            console.error(`Error fetching product with uri ${uri}:`, error);
            throw error;
        }
    }

    async createProduct(product: Partial<IProduct>): Promise<IProduct> {
        try {
            const { data } = await this.axios.post<IProduct>(this.productUrl, product);
            return data;
        } catch (error) {
            console.error('Error creating product:', error);
            throw error;
        }
    }

    async updateProduct(id: number, product: Partial<IProduct>): Promise<IProduct> {
        try {
            const { data } = await this.axios.put<IProduct>(`${this.productUrl}/${id}`, product);
            return data;
        } catch (error) {
            console.error(`Error updating product with id ${id}:`, error);
            throw error;
        }
    }

    async deleteProduct(id: number): Promise<boolean> {
        try {
            await this.axios.delete(`${this.productUrl}/${id}`);
            return true;
        } catch (error) {
            console.error(`Error deleting product with id ${id}:`, error);
            throw error;
        }
    }
}