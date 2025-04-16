// src/services/IProductService.ts
import type { ICategory } from '@/types/category/ICategory';

export interface ICategoryService {
  getCategories(): Promise<ICategory[]>;
  subscribeToCategories(callback: (categories: ICategory[]) => void): () => void;
  getCategoryById(id: number): Promise<ICategory>;
  createCategory(category: Partial<ICategory>): Promise<ICategory>;
  updateCategory(id: number, category: Partial<ICategory>): Promise<ICategory>;
  deleteCategory(id: number): Promise<number>;
}