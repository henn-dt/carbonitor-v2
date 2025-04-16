// src/stores/productStore.ts
import { defineStore } from 'pinia';
import type { ICategory } from '@/types/category/ICategory';
import type { ICategoryState } from '@/types/category/ICategoryState';

export const useCategoryStore = defineStore('category', {
    state: (): ICategoryState => ({
        categories: [],
        selectedCategory: null,
        loading: false,
        error: null,
        needsRefresh: true,
        totalCategories: 0,
        lastFetchTimestamp: null
    }),

    getters: {
        getCategories:   (state) => state.categories,
        getSelectedCategory: (state) => state.selectedCategory,
        getLoading: (state) => state.loading,
        getError: (state) => state.error,
        getTotalPages: (state) => state.totalCategories,
        isDataLoaded: (state) => state.categories.length > 0 && !state.loading,
    },

    actions: {


        setCategories(categories: ICategory[]) {
            this.categories = categories;
            this.totalCategories = categories.length;
        },

        setSelectedCategory(category: ICategory | null) {
            this.selectedCategory = category;
        },

        setLoading(loading: boolean) {
            this.loading = loading;
        },

        setError(error: string | null) {
            this.error = error;
        },

        setNeedsRefresh(needsRefresh : boolean) {
            this.needsRefresh = needsRefresh;
        },

        setLastFetchTimestamp(timestamp: number | null) {
            this.lastFetchTimestamp = timestamp;
        },

        addCategory(category: ICategory) {
            this.categories.push(category);
            this.totalCategories++;
        },

        updateCategory(updatedCategory: ICategory) {
            const index = this.categories.findIndex(c => c.id === updatedCategory.id);
            if (index !== -1) {
            this.categories[index] = updatedCategory;
            }
        },

        removeCategory(id: number) {
            this.categories = this.categories.filter(c => c.id !== id);
            this.totalCategories--;
            if (this.selectedCategory && this.selectedCategory.id === id) {
            this.selectedCategory = null;
            }
        },

        reset() {
            this.categories = [];
            this.selectedCategory = null;
            this.loading = false;
            this.error = null;
            this.needsRefresh = true;
            this.totalCategories = 0;
            this.lastFetchTimestamp = null
        },


    }
});