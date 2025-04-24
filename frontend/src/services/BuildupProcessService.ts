// src/services/BuildupService.ts
import { injectable, inject } from 'inversify';
import { TYPES } from '@/di/types';
import type { IBuildupProcessService } from './IBuildupProcessService';
import { getAuthStore, getBuildupStore } from '@/stores/storeAccessor';
import type { IBuildupWithProcessedProducts } from '@/types/epdx/IBuildupWithProcessedProducts';
import type { IImpactCalculationService } from './IImpactCalculationService';
import type { IBuildup } from '@/types/buildup/IBuildup';


@injectable()
export class BuildupProcessService implements IBuildupProcessService {
    constructor(
        @inject(TYPES.ImpactCalculationService) private impactService: IImpactCalculationService
    ) {}

    async processIfNeeded() {
        const buildupStore = getBuildupStore();
        if (buildupStore.needsProcessing) {
            this.processAllBuildups()
            buildupStore.setNeedsProcessing(false)
        }
    }
    /**
     * Process a single buildup with incremental update check
     */
    async processBuildup(buildupId: number): Promise<IBuildupWithProcessedProducts> {
        try {
            const buildupStore = getBuildupStore();

            
            // Find the buildup in the store
            const buildup = buildupStore.buildups.find(b => b.id === buildupId);
            if (!buildup) {
                throw new Error(`Buildup with ID ${buildupId} not found`);
            }
            
            // Check if this buildup already has processed data
            const existingProcessedData = buildupStore.findProcessedDataById(buildupId);
            
            // If we have existing processed data, check if we need to update it
            if (existingProcessedData && !buildupStore.needsRefresh) {
                // Get the buildup's last update timestamp
                const buildupLastUpdate = buildup.updated_at 
                    ? new Date(buildup.updated_at).getTime() 
                    : 0;
                
                // Get the processed data's last update timestamp
                const processedLastUpdate = existingProcessedData.lastLocalUpdate 
                    ? new Date(existingProcessedData.lastLocalUpdate).getTime() 
                    : 0;
                
                // If the processed data is newer than the buildup, no update needed
                if (processedLastUpdate >= buildupLastUpdate) {
                    console.log(`Processed data for buildup ${buildupId} is up-to-date`);

                    return this.getCombinedBuildup(buildupId);
                }
                
                console.log(`Processed data for buildup ${buildupId} needs updating`);
                buildupStore.setProcessingStatus(buildupId, true);
            }
            
            // Process the buildup
            const processedBuildup = await this.impactService.processSingleBuildupImpacts(buildup);
            
            // Add timestamp to processed data
            const processedWithTimestamp: IBuildupWithProcessedProducts = {
                ...processedBuildup,
                lastLocalUpdate: new Date().toISOString()
            };
            
            // Store the processed data with timestamp
            buildupStore.setProcessedBuildup(buildupId, processedWithTimestamp);
            buildupStore.setProcessingStatus(buildupId, false);
            
            
            // Return the combined view
            return this.getCombinedBuildup(buildupId);
        } catch (error) {
            const buildupStore = getBuildupStore();
            buildupStore.setProcessingError(buildupId, error instanceof Error ? error.message : 'Failed to process buildup');
            buildupStore.setProcessingStatus(buildupId, false);
            throw error;
        }
    }
        
        // Get a buildup with its processed data
        getCombinedBuildup(buildupId: number): (IBuildup & IBuildupWithProcessedProducts) {
            const buildupStore = getBuildupStore();
            const buildup = buildupStore.buildups.find(b => b.id === buildupId);
            if (!buildup) {
                throw new Error(`Buildup with ID ${buildupId} not found`);
            }
            
            const processedData = buildupStore.findProcessedDataById(buildupId)
            if (!processedData) {
                return {
                    ...buildup,
                    mappedProducts: {},
                    processedProducts: [],
                    isFullyProcessed: false
                };
            }
            
            return {
                ...buildup,
                mappedProducts: processedData.mappedProducts,
                processedProducts: processedData.processedProducts,
                isFullyProcessed: processedData.isFullyProcessed
            };
        }

        getAllCombinedBuildups(): (IBuildup & IBuildupWithProcessedProducts)[] {
            const buildupStore = getBuildupStore();
            const buildups = buildupStore.buildups;

            if (buildups.length === 0) {
                return [];
            }
            return buildups.map(buildup => {
                try {
                  return this.getCombinedBuildup(buildup.id);
                } catch (err) {
                  console.error(`Error combining buildup ${buildup.id}:`, err);
                  // Return a default partial buildup
                  return {
                    ...buildup,
                    mappedProducts: {},
                    processedProducts: [],
                    isFullyProcessed: false
                  };
                }
              });
        }
    /**
     * Process all buildups with incremental update check
     */
    async processAllBuildups(): Promise<IBuildupWithProcessedProducts[]> {
        try {
            const buildupStore = getBuildupStore();
            
            // Get all buildups
            const buildups = [...buildupStore.buildups];
            
            // If needsRefresh is set, process all buildups
            if (buildupStore.needsProcessing) {
                console.log("Full refresh of processed buildups requested");
                await this.processAllBuildupsFull(buildups);
                return this.getAllCombinedBuildups();
            }
            
            // Otherwise, do incremental processing
            await this.processAllBuildupsIncremental(buildups);
            return this.getAllCombinedBuildups();
        } catch (error) {
            const buildupStore = getBuildupStore();
            buildupStore.setProcessingAllStatus(false);
            buildupStore.setError(error instanceof Error ? error.message : 'Failed to process buildups');
            throw error;
        } finally {
            const buildupStore = getBuildupStore();
            buildupStore.setProcessingAllStatus(false);
            buildupStore.setNeedsProcessing(false)
        }
    }


        /**
     * Process all buildups without incremental checking
     */
        private async processAllBuildupsFull(buildups: IBuildup[]): Promise<void> {
            if (buildups.length === 0) return;
            
            const buildupStore = getBuildupStore();
            const currentTime = new Date().toISOString();
            
            // Process all buildups
            const processedBuildups = await this.impactService.processBuildupsImpacts(buildups);
            
            // Add timestamp and store all processed buildups
            processedBuildups.forEach(processedBuildup => {
                const processedWithTimestamp: IBuildupWithProcessedProducts = {
                    ...processedBuildup,
                    lastLocalUpdate: currentTime
                };
                
                buildupStore.setProcessedBuildup(processedBuildup.id, processedWithTimestamp);
            });
            
            console.log(`Processed all ${processedBuildups.length} buildups`);
        }
        
        /**
         * Process only buildups that need updates
         */
        private async processAllBuildupsIncremental(buildups: IBuildup[]): Promise<void> {
            if (buildups.length === 0) return;
            
            const buildupStore = getBuildupStore();
            const buildupsToProcess: IBuildup[] = [];
            
            // Identify buildups that need processing
            for (const buildup of buildups) {
                const processedData = buildupStore.findProcessedDataById(buildup.id);
                
                // If no processed data exists, it needs processing
                if (!processedData) {
                    buildupsToProcess.push(buildup);
                    continue;
                }
                
                // If buildup has been updated since last processing, it needs reprocessing
                const buildupLastUpdate = buildup.updated_at 
                    ? new Date(buildup.updated_at).getTime() 
                    : 0;
                
                const processedLastUpdate = processedData.lastLocalUpdate 
                    ? new Date(processedData.lastLocalUpdate).getTime() 
                    : 0;
                
                if (buildupLastUpdate > processedLastUpdate) {
                    buildupsToProcess.push(buildup);
                }
            }
            
            if (buildupsToProcess.length === 0) {
                console.log("All buildups are already processed and up-to-date");
                return;
            }
            
            console.log(`Processing ${buildupsToProcess.length} out of ${buildups.length} buildups that need updates`);
            
            // Process only the buildups that need it
            const currentTime = new Date().toISOString();
            const processedBuildups = await this.impactService.processBuildupsImpacts(buildupsToProcess);
            
            // Add timestamp and store processed buildups
            processedBuildups.forEach(processedBuildup => {
                const processedWithTimestamp: IBuildupWithProcessedProducts = {
                    ...processedBuildup,
                    lastLocalUpdate: currentTime
                };
                
                buildupStore.setProcessedBuildup(processedBuildup.id, processedWithTimestamp);
            });
        }

    /**
     * Subscribe to buildup process updates
     */
    subscribeToBuildupProcess(callback: (processedBuildups: IBuildupWithProcessedProducts[]) => void): () => void {
        const buildupStore = getBuildupStore();
        
        // Create a watcher function that calls the callback whenever processed buildups change
        // but only when not processing
        const unsubscribe = buildupStore.$subscribe(
            (mutation, state) => {
                if (!state.loading && !state.processingAll) {
                    // Convert store processed data to combined buildups
                    const combinedBuildups = this.getAllCombinedBuildups();
                    callback(combinedBuildups);
                }
            }
        );
        
        // Immediately call with current data if not loading
        if (!buildupStore.loading && !buildupStore.processingAll) {
            const combinedBuildups = this.getAllCombinedBuildups();
            callback(combinedBuildups);
        }
        
        // Return the unsubscribe function
        return unsubscribe;
    }
    }