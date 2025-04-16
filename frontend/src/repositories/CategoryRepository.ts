// src/repositories/CategoryRepository.ts
import type { ICategoryRepository } from './ICategoryRepository';
import { BaseRepository } from './BaseRepository';
import type { ICategory } from '@/types/category/ICategory';
import { inject, injectable } from 'inversify';
import type { IHttpClient } from './IHttpClient';
import { TYPES } from '@/di/types';

@injectable()
export class CategoryRepository extends BaseRepository implements ICategoryRepository {
    private categoryUrl: string;

    constructor(
        @inject(TYPES.HttpClient) httpClient: IHttpClient
    ) {
        super(httpClient);
        this.categoryUrl = `${this.axios.defaults.baseURL}/categories/`;
    }

    async getCategories(): Promise<ICategory[]> {
        try {
            return await this.get<ICategory[]>(this.categoryUrl);
        } catch (error) {
            console.error('Error fetching categories:', error);
            throw error;
        }
    }

    async getCategoryById(id: number): Promise<ICategory> {
        try {
            return await this.get<ICategory>(`${this.categoryUrl}${id}`);
        } catch (error) {
            console.error(`Error fetching category with id ${id}:`, error);
            throw error;
        }
    }

    async createCategory(category: Partial<ICategory>): Promise<ICategory> {
        try {
            return await this.post<ICategory>(this.categoryUrl, category);
        } catch (error) {
            console.error('Error creating category:', error);
            throw error;
        }
    }

    async updateCategory(id: number, category: Partial<ICategory>): Promise<ICategory> {
        try {
            return await this.put<ICategory>(`${this.categoryUrl}${id}`, category);
        } catch (error) {
            console.error(`Error updating category with id ${id}:`, error);
            throw error;
        }
    }

    async deleteCategory(id: number): Promise<boolean> {
        try {
            await this.axios.delete(`${this.categoryUrl}${id}`);
            return true
        } catch (error) {
            console.error(`Repository level Error deleting category with id ${id}:`, error);
            throw error;
        }
    }

}