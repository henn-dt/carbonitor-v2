// src/stores/productSnapshotStore.ts

// ReferenceSourceForProduct of type actual gets transformed into snapshot products, separate from products retrieved from db.
import { defineStore } from 'pinia';
import type { IProduct } from '@/types/product/IProduct';
import type { IProductState } from '@/types/product/IProductState';

export const useProductSnapshotStore = defineStore('product_snapshot', {
    state: (): IProductState => ({
        products: [],
        selectedProduct: null,
        loading: false,
        error: null,
        needsRefresh: true,
        totalProducts: 0,
        currentPage: 1,
        itemsPerPage: 10,
        lastFetchTimestamp: null
    }),

    getters: {
        getProducts: (state) => state.products,
        getSelectedProduct: (state) => state.selectedProduct,
        getLoading: (state) => state.loading,
        getError: (state) => state.error,
        getTotalPages: (state) => Math.ceil(state.totalProducts / state.itemsPerPage),
    },

    actions: {
        setProducts(products: IProduct[]) {
            this.products = products;
            this.totalProducts = products.length;
        },

        setSelectedProduct(product: IProduct | null) {
            this.selectedProduct = product;
        },

        setLoading(loading: boolean) {
            this.loading = loading;
        },

        setError(error: string | null) {
            this.error = error;
        },

        setPage(page: number) {
            this.currentPage = page;
        },

        setItemsPerPage(count: number) {
            this.itemsPerPage = count;
        },

        addProduct(product: IProduct) {
            this.products.push(product);
            this.totalProducts++;
        },

        setNeedsRefresh(needsRefresh : boolean) {
            this.needsRefresh = needsRefresh;
        },

        setLastFetchTimestamp(timestamp: number | null) {
            this.lastFetchTimestamp = timestamp;
        },

        updateProduct(updatedProduct: IProduct) {
            const index = this.products.findIndex(p => p.id === updatedProduct.id);
            if (index !== -1) {
            this.products[index] = updatedProduct;
            }
        },

        removeProduct(id: number) {
            this.products = this.products.filter(p => p.id !== id);
            this.totalProducts--;
            if (this.selectedProduct && this.selectedProduct.id === id) {
            this.selectedProduct = null;
            }
        },

        reset() {
            this.products = [];
            this.selectedProduct = null;
            this.loading = false;
            this.error = null;
            this.needsRefresh = true;
            this.totalProducts = 0;
            this.currentPage = 1;
            this.lastFetchTimestamp = null;
        }
    }
});