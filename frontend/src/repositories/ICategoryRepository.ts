// src/repositories/ICategoryRepository.ts
import type { ICategory } from '@/types/category/ICategory';

export interface ICategoryRepository {
    getCategories(): Promise<ICategory[]>;
    getCategoryById(id: number): Promise<ICategory>;
    createCategory(category: Partial<ICategory>): Promise<ICategory>;
    updateCategory(id: number, category: Partial<ICategory>): Promise<ICategory>;
    deleteCategory(id: number): Promise<boolean>;
}