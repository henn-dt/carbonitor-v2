// src/stores/buildupStore.ts
import { defineStore } from 'pinia';
import type { IBuildup } from '@/types/buildup/IBuildup';
import type { IBuildupState } from '@/types/buildup/IBuildupState';
import type { IBuildupWithProcessedProducts } from '@/types/epdx/IBuildupWithProcessedProducts';

export const useBuildupStore = defineStore('buildup', {
    state: (): IBuildupState => ({
        buildups: [],
        selectedBuildup: null,
        loading: false,
        error: null,
        needsRefresh: true,
        lastFetchTimestamp: null,
        processedBuildups: [],
        processingStatus: {},
        processingErrors: {},
        processingAll: false
    }),

    getters: {
        getBuildups: (state) => state.buildups,
        getSelectedBuildup: (state) => state.selectedBuildup,
        getProcessedBuildups: (state) => state.processedBuildups,
        getLoading: (state) => state.loading,
        getError: (state) => state.error,
        findBuildupById: (state) => (id: number) => {
        return state.buildups.find(b => b.id === id) || null;
            },
        findProcessedDataById: (state) => (id: number) => {
        return state.processedBuildups.find(p => p.id === id) || null;
            },


        // New getters for processed data
        isProcessing: (state) => (buildupId: number) => state.processingStatus[buildupId] || false,
        isProcessingAll: (state) => state.processingAll,
        getProcessingError: (state) => (buildupId: number) => state.processingErrors[buildupId] || null,
          
        // Check if a buildup has been processed
        isBuildupProcessed: (state) => (buildupId: number) => {
            return state.processedBuildups.find(p => buildupId === p.id)?.isFullyProcessed || false;
        },
        // Get all processed buildup IDs
        processedBuildupIds: (state) => {
            return state.processedBuildups
                .filter(data => data.isFullyProcessed)
                .map(data => data.id);
        },
        getSelectedBuildupProcessedData: (state) => {
            return state.processedBuildups.find(p => state.selectedBuildup?.id === p.id)
        }
    },


    actions: {
        setBuildups(buildups: IBuildup[]) {
            this.buildups = buildups;
        },

        setSelectedBuildup(buildup: IBuildup | null) {
            this.selectedBuildup = buildup;
        },

        setLoading(loading: boolean) {
            this.loading = loading;
        },

        setError(error: string | null) {
            this.error = error;
        },



        addBuildup(buildup: IBuildup) {
            this.buildups.push(buildup);
        },

        addProcessedBuildup(processedBuildup : IBuildupWithProcessedProducts) {
            this.processedBuildups.push(processedBuildup)
        },

        setNeedsRefresh(needsRefresh : boolean) {
            this.needsRefresh = needsRefresh;
        },

        setLastFetchTimestamp(timestamp: number | null) {
            this.lastFetchTimestamp = timestamp;
        },

        updateBuildup(updatedBuildup: IBuildup) {
            const index = this.buildups.findIndex(p => p.id === updatedBuildup.id);
            if (index !== -1) {
            this.buildups[index] = updatedBuildup;
            }
        },

        removeBuildup(id: number) {
            this.buildups = this.buildups.filter(p => p.id !== id);
            if (this.selectedBuildup && this.selectedBuildup.id === id) {
            this.selectedBuildup = null;
            }
        },

        setProcessedBuildups(processedBuildups: IBuildupWithProcessedProducts[]) {
            this.processedBuildups = processedBuildups
        },

         // Modified actions for array-based processedData
        setProcessedBuildup(buildupId: number, data: Omit<IBuildupWithProcessedProducts, 'id'>) {
            // Find existing data and update, or add new
            const existingIndex = this.processedBuildups.findIndex(item => item.id === buildupId);

            const completeData: IBuildupWithProcessedProducts = {
                id: buildupId,
                ...data
            };

            if (existingIndex >= 0) {
                // Update existing data
                this.processedBuildups[existingIndex] = completeData;
            } else {
                // Add new data
                this.processedBuildups.push(completeData);
            }
        },
        
        setProcessingStatus(buildupId: number, status: boolean) {
            this.processingStatus[buildupId] = status;
        },

        setProcessingError(buildupId: number, error: string | null) {
            this.processingErrors[buildupId] = error;
        },

        setProcessingAllStatus(status: boolean) {
            this.processingAll = status;
        },

        reset() {
            this.buildups = [];
            this.selectedBuildup = null;
            this.loading = false;
            this.error = null;
            this.needsRefresh = true;
            this.lastFetchTimestamp = null;
            this.processedBuildups = [];
            this.processingStatus = {},
            this.processingErrors = {},
            this.processingAll = false
        }
    }
});