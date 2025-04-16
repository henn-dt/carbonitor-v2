// src/services/ProductService.ts
import { injectable, inject } from 'inversify';
import type { ICategoryService } from './ICategoryService';
import { TYPES } from '@/di/types';
import type { ICategoryRepository } from '@/repositories/ICategoryRepository';
import { Category } from '@/types/category/Category';
import type { ICategory } from '@/types/category/ICategory';
import type { ICreateCategory } from '@/types/category/ICreateCategory';
import { getAuthStore, getCategoryStore } from '@/stores/storeAccessor';

@injectable()
export class CategoryService implements ICategoryService {
    constructor(
        @inject(TYPES.CategoryRepository) private categoryRepository: ICategoryRepository,
    ) {}

    async getCategories(): Promise<ICategory[]> {
        try {

            const categoryStore = getCategoryStore();


            // If we already have categories loaded, return them
            if (categoryStore.categories.length > 0 && !categoryStore.needsRefresh) {

                return [...categoryStore.categories]; // Return a copy to prevent accidental mutations
            }

            const authStore = getAuthStore();

            categoryStore.setLoading(true);

            const categories = await this.categoryRepository.getCategories();
            const categoryDTOs = categories.map(category => new Category(category));
            
            // Update the store state
            categoryStore.setCategories(categoryDTOs);
            categoryStore.setNeedsRefresh(false);
            categoryStore.setLoading(false);
            categoryStore.setLastFetchTimestamp(new Date().getTime());
            
            return categoryDTOs;
        } catch (error) {
            const categoryStore = getCategoryStore();
            categoryStore.setLoading(false);
            categoryStore.setError(error instanceof Error ? error.message : 'Failed to fetch categories');
            throw error;
        }
    }

    //subscribe to category changes

    subscribeToCategories(callback: (categories: ICategory[]) => void): () => void {
        const categoryStore = getCategoryStore();
        
        // Create a watcher function that calls the callback whenever categories change
        const unsubscribe = categoryStore.$subscribe(
            (mutation, state) => {
                callback([...state.categories]);
            }
        );
        
        // Immediately call with current data
        callback([...categoryStore.categories]);
        
        // Return the unsubscribe function
        return unsubscribe;
    }


    async getCategoryById(id: number): Promise<ICategory> {
        try {
            const categoryStore = getCategoryStore();
            
            // Check if product is already in the store
            const cachedCategory = categoryStore.categories.find(c => c.id === id);
            if (cachedCategory) {
                categoryStore.setSelectedCategory(cachedCategory);
                return cachedCategory;
            }
            
            categoryStore.setLoading(true);
            const category = await this.categoryRepository.getCategoryById(id);
            const categoryDTO = new Category(category);
            
            // Update the store
            categoryStore.setSelectedCategory(categoryDTO);
            categoryStore.setLoading(false);
            
            return categoryDTO;
        } catch (error) {
            const categoryStore = getCategoryStore();
            categoryStore.setLoading(false);
            categoryStore.setError(error instanceof Error ? error.message : `Failed to fetch category #${id}`);
            throw error;
        }
    }

    async createCategory(category: Partial<ICreateCategory>): Promise<ICategory> {
        try {
            const categoryStore = getCategoryStore();
            const authStore = getAuthStore();
            categoryStore.setLoading(true);
            
            // Add timestamp and set status if not present
            if (!category.status) {
                category.status = 'active';
            }

            if (!category.property_schema) {
                category.property_schema = {}
            }

            if (!authStore.user) {
                throw "no user is logged in";
              }               
              
            const currentUserId = authStore.user?.id

            const categoryWithUserData = {
                ...category,
                user_id_created: currentUserId,
                user_id_updated: currentUserId
            };
            
            // Call repository to save in backend
            const createdCategory = await this.categoryRepository.createCategory(categoryWithUserData);
            const categoryDTO = new Category(createdCategory);
            
            // Update the store
            categoryStore.addCategory(categoryDTO);
            categoryStore.setLoading(false);
            
            return categoryDTO;
        } catch (error) {
            const categoryStore = getCategoryStore();
            categoryStore.setLoading(false);
            categoryStore.setError(error instanceof Error ? error.message : 'Failed to create category');
            throw error;
        }
    }

    async updateCategory(id: number, category: Partial<ICategory>): Promise<ICategory> {
        try {
            const categoryStore = getCategoryStore();
            const authStore = getAuthStore();
            categoryStore.setLoading(true);
            
            // retrieve user data

            if (!authStore.user) {
                // This will immediately exit the function and trigger the catch block
                throw "No user is logged in";
                
              }
            
            category.user_id_updated = authStore.user.id
            

            // Call repository to update in backend
            const updatedCategory = await this.categoryRepository.updateCategory(id, category);
            const categoryDTO = new Category(updatedCategory);
            
            // Update the store
            categoryStore.updateCategory(categoryDTO);
            categoryStore.setLoading(false);
            
            return categoryDTO;
        } catch (error) {
            const categoryStore = getCategoryStore();
            categoryStore.setLoading(false);
            categoryStore.setError(error instanceof Error ? error.message : `Failed to update category #${id}`);
            throw error;
        }
    }

    async deleteCategory(id: number): Promise<number> {
        try {
            const categoryStore = getCategoryStore();
            categoryStore.setLoading(true);

            
            // Call repository to delete from backend
            const result = await this.categoryRepository.deleteCategory(id);
            let output = 0
            if (result) {
                // Update the store by removing the category
                categoryStore.removeCategory(id);
                output = id
                categoryStore.setLoading(false);
            }
            
            
            return output;
        } catch (error) {
            const categoryStore = getCategoryStore();
            categoryStore.setLoading(false);
            categoryStore.setError(error instanceof Error ? error.message : `Failed to delete category #${id}`);
            throw error;
        }
    }   
}