// src/services/BuildupService.ts
import { injectable, inject } from 'inversify';
import type { IBuildupService } from './IBuildupService';
import type { IBuildupRepository } from '@/repositories/IBuildupRepository';
import type { IBuildup } from '@/types/buildup/IBuildup';
import { TYPES } from '@/di/types';
import { Buildup } from '@/types/buildup/Buildup';
import { getAuthStore, getBuildupStore } from '@/stores/storeAccessor';
import { BuildupToBackend } from '@/types/buildup/BuildupToBackend';

@injectable()
export class BuildupService implements IBuildupService {
    constructor(
        @inject(TYPES.BuildupRepository) private buildupRepository: IBuildupRepository
    ) {}

    private updatedStore() {
        const buildupStore = getBuildupStore();
        const currentTime = new Date().getTime();
        buildupStore.setNeedsRefresh(false)
        buildupStore.setNeedsProcessing(true)
        buildupStore.setLastFetchTimestamp(currentTime)
    }
    //async initBuildups(): Promise
    async getBuildups(): Promise<IBuildup[]> {
        try {
            const buildupStore = getBuildupStore();
            buildupStore.setLoading(true);

            // Check if we need a full refresh
            if (buildupStore.needsRefresh) {
                console.log('Performing full refresh of buildup data');
                return await this.performFullRefresh();
                }

            // If we already have buildups and no refresh is needed, check for incremental updates
            if (buildupStore.buildups.length > 0) {
                console.log('Checking for incremental updates...');
                return await this.performIncrementalUpdate();
            }

            // Initial load (store is empty)
            console.log('Buildup Store is empty, performing initial load');
            return await this.performFullRefresh();
            
        } 
        catch (error) {
            const buildupStore = getBuildupStore();
            buildupStore.setLoading(false);          
            buildupStore.setError(error instanceof Error ? error.message : 'Failed to fetch buildups');
            throw error;
        } finally {
            const buildupStore = getBuildupStore();
            buildupStore.setLoading(false);
        }
        
    }

    /**
     * Performs a full refresh of all buildups
     */
    private async performFullRefresh(): Promise<IBuildup[]> {
        const buildupStore = getBuildupStore();
        try {
            const buildups = await this.buildupRepository.getBuildups();           
            // Replace all buildups in the store
            buildupStore.setBuildups(buildups);
            console.log(`Buildup store refreshed with ${buildups.length} elements`);
            
            // Update store metadata
            this.updatedStore()         
            return [...buildups]; // Return a copy
        } finally {
            buildupStore.setLoading(false);
        }
    }

    /**
     * Performs an incremental update by fetching only changed buildups
     */
    private async performIncrementalUpdate(): Promise<IBuildup[]> {
        const buildupStore = getBuildupStore();
        const lastFetchTime = buildupStore.lastFetchTimestamp;
        
        try {
            // Option 1: If your API supports fetching changes since a timestamp
            // const changedBuildups = await this.buildupRepository.getChangedBuildupsSince(lastFetchTime);
            
            // Option 2: Fetch all and filter client-side (fallback if API doesn't support incremental)
            const allBuildups = await this.buildupRepository.getBuildups();
           
            // Find which buildups are new or updated
            const existingBuildupMap = new Map(buildupStore.buildups.map(b => [b.id, b]));
            const newBuildups: IBuildup[] = [];
            const updatedBuildups: IBuildup[] = [];
            
            for (const buildup of allBuildups) {
                const existing = existingBuildupMap.get(buildup.id);
                
                if (!existing) {
                    // This is a new buildup
                    newBuildups.push(buildup);
                } else if (this.isBuildupUpdated(existing, buildup)) {
                    // This buildup has been updated
                    updatedBuildups.push(buildup);
                }
            }
            
            // Find deleted buildups
            const currentBuildupIds = new Set(allBuildups.map(b => b.id));
            const deletedBuildupIds = buildupStore.buildups
                .filter(b => !currentBuildupIds.has(b.id))
                .map(b => b.id);
            
            console.log(`Found ${newBuildups.length} new, ${updatedBuildups.length} updated, and ${deletedBuildupIds.length} deleted buildups`);
            
            // Apply updates to store if there are any changes
            if (newBuildups.length > 0 || updatedBuildups.length > 0 || deletedBuildupIds.length > 0) {
                // Add new buildups
                for (const buildup of newBuildups) {
                    buildupStore.addBuildup(buildup);
                }
                
                // Update changed buildups
                for (const buildup of updatedBuildups) {
                    buildupStore.updateBuildup(buildup);
                }
                
                // Remove deleted buildups
                for (const id of deletedBuildupIds) {
                    buildupStore.removeBuildup(id);
                }
                
                // Update the timestamp
                this.updatedStore()   
            } else {
                console.log('No changes detected in buildups');
            }
            
            return [...buildupStore.buildups]; // Return a copy of all buildups
        } finally {
            buildupStore.setLoading(false);
        }
    }
    
    /**
     * Determines if a buildup has been updated by comparing timestamps
     */
    private isBuildupUpdated(existing: IBuildup, current: IBuildup): boolean {
        // If the backend provides updated_at timestamps, use those
        if (existing.updated_at && current.updated_at) {
            return new Date(current.updated_at).getTime() > new Date(existing.updated_at).getTime();
        }
        
        // Otherwise, use a deep comparison of relevant properties
        // This is a simplified example - adjust based on your buildup structure
        return JSON.stringify(this.getNormalizedBuildup(existing)) !== 
               JSON.stringify(this.getNormalizedBuildup(current));
    }
    
    /**
     * Creates a normalized version of a buildup for comparison
     * (removes properties that shouldn't affect equality)
     */
    private getNormalizedBuildup(buildup: IBuildup): Partial<IBuildup> {
        // Create a copy without the properties that shouldn't affect equality
        const { updated_at, created_at, ...normalized } = buildup;
        return normalized;
    }

    subscribeToBuildups(callback: (buildups: IBuildup[]) => void): () => void {
        const buildupStore = getBuildupStore();
        
        // Create a watcher function that calls the callback whenever buildups change
        const unsubscribe = buildupStore.$subscribe(
            (mutation, state) => {
                if (!state.loading) {
                    callback([...state.buildups]);
                }
            }
        );
        
        // Immediately call with current data
        callback([...buildupStore.buildups]);
        
        // Return the unsubscribe function
        return unsubscribe;
    }
    /**
     * Get a buildup by ID with refresh checking
     */
    async getBuildupById(id: number): Promise<IBuildup> {
        try {
            const buildupStore = getBuildupStore();
            buildupStore.setLoading(true);
            
            // Check if buildup is already in the store
            const cachedBuildup = buildupStore.buildups.find(p => p.id === id);
            
            // If cached and we don't need a refresh, use the cached version
            if (cachedBuildup && !buildupStore.needsRefresh) {
                // Fetch the latest version to check for updates
                const freshBuildup = await this.buildupRepository.getBuildupById(id);
                const freshBuildupDTO = new Buildup(freshBuildup);
                
                // Check if the buildup has been updated
                if (this.isBuildupUpdated(cachedBuildup, freshBuildupDTO)) {
                    console.log(`Buildup #${id} has been updated, refreshing cache`);
                    // Update the buildup in the store
                    buildupStore.updateBuildup(freshBuildupDTO);
                    buildupStore.setSelectedBuildup(freshBuildupDTO);
                    buildupStore.setLoading(false);
                    return freshBuildupDTO;
                }
                
                // If no update needed, use cached
                console.log(`Buildup #${id} is up to date`);
                buildupStore.setSelectedBuildup(cachedBuildup);
                buildupStore.setLoading(false);
                return cachedBuildup;
            }
            
            // If not in cache or needs refresh, fetch it
            console.log(`Fetching buildup #${id} from repository`);
            const buildup = await this.buildupRepository.getBuildupById(id);
            const buildupDTO = new Buildup(buildup);
            
            // If it was already in the cache, update it; otherwise add it
            if (cachedBuildup) {
                buildupStore.updateBuildup(buildupDTO);
            } else {
                buildupStore.addBuildup(buildupDTO);
            }
            
            // Update selected buildup
            buildupStore.setSelectedBuildup(buildupDTO);
            buildupStore.setLoading(false);
            
            return buildupDTO;
        } catch (error) {
            const buildupStore = getBuildupStore();
            buildupStore.setLoading(false);
            buildupStore.setError(error instanceof Error ? error.message : `Failed to fetch buildup #${id}`);
            throw error;
        }
    }
    /**
     * Get a buildup by name with refresh checking
     */
    async getBuildupByName(name: string): Promise<IBuildup> {
        try {
            const buildupStore = getBuildupStore();
            buildupStore.setLoading(true);
            
            // Check if buildup is already in the store
            const cachedBuildup = buildupStore.buildups.find(p => `${p.name}` === name);
            
            // If cached and we don't need a refresh, check for updates
            if (cachedBuildup && !buildupStore.needsRefresh) {
                // Fetch the latest version to check for updates
                const freshBuildup = await this.buildupRepository.getBuildupByName(name);
                const freshBuildupDTO = new Buildup(freshBuildup);
                
                // Check if the buildup has been updated
                if (this.isBuildupUpdated(cachedBuildup, freshBuildupDTO)) {
                    console.log(`Buildup "${name}" has been updated, refreshing cache`);
                    // Update the buildup in the store
                    buildupStore.updateBuildup(freshBuildupDTO);
                    buildupStore.setSelectedBuildup(freshBuildupDTO);
                    buildupStore.setLoading(false);
                    return freshBuildupDTO;
                }
                
                // If no update needed, use cached
                console.log(`Buildup "${name}" is up to date`);
                buildupStore.setSelectedBuildup(cachedBuildup);
                buildupStore.setLoading(false);
                return cachedBuildup;
            }
            
            // If not in cache or needs refresh, fetch it
            console.log(`Fetching buildup "${name}" from repository`);
            const buildup = await this.buildupRepository.getBuildupByName(name);
            const buildupDTO = new Buildup(buildup);
            
            // If it was already in the cache, update it; otherwise add it
            if (cachedBuildup) {
                buildupStore.updateBuildup(buildupDTO);
            } else {
                buildupStore.addBuildup(buildupDTO);
            }
            
            // Update selected buildup
            buildupStore.setSelectedBuildup(buildupDTO);
            buildupStore.setLoading(false);
            
            return buildupDTO;
        } catch (error) {
            const buildupStore = getBuildupStore();
            buildupStore.setLoading(false);
            buildupStore.setError(error instanceof Error ? error.message : `Failed to fetch buildup with name: ${name}`);
            throw error;
        }
    }

    async createBuildup(buildup: Partial<IBuildup>): Promise<IBuildup> {
        try {
            const buildupStore = getBuildupStore();
            const authStore = getAuthStore();
            buildupStore.setLoading(true);
            
            // Add timestamp and set status if not present
            if (!buildup.status) {
                buildup.status = 'active';
            }

            if (!authStore.user) {
                throw "no user is logged in";
              }               
              
            const currentUserId = authStore.user?.id

            const buildupWithUserData = {
                ...buildup,
                user_id_created: currentUserId,
                user_id_updated: currentUserId
            };
            
            const payload = new BuildupToBackend(buildupWithUserData)

            // Call repository to save in backend
            const createdBuildup = await this.buildupRepository.createBuildup(payload);
            const buildupDTO = new Buildup(createdBuildup);
            
            // Update the store
            buildupStore.addBuildup(buildupDTO);
            buildupStore.setLoading(false);
            this.updatedStore()
            
            return buildupDTO;
        } catch (error) {
            const buildupStore = getBuildupStore();
            buildupStore.setLoading(false);
            buildupStore.setError(error instanceof Error ? error.message : 'Failed to create buildup');
            throw error;
        }
    }

    async updateBuildup(id: number, buildup: Partial<IBuildup>): Promise<IBuildup> {
        try {
            const buildupStore = getBuildupStore();
            const authStore = getAuthStore();
            buildupStore.setLoading(true);
            

            if (!authStore.user) {
                throw "no user is logged in";
              }               
              
            const currentUserId = authStore.user?.id

            const buildupWithUserData = {
                ...buildup,
                user_id_updated: currentUserId
            };

            const payload = new BuildupToBackend(buildupWithUserData)

            // Call repository to update in backend
            const updatedBuildup = await this.buildupRepository.updateBuildup(id, payload);
            const buildupDTO = new Buildup(updatedBuildup);

            
            // Update the store
            buildupStore.updateBuildup(buildupDTO);
            buildupStore.setLoading(false);
            this.updatedStore()
            
            return buildupDTO;
        } catch (error) {
            const buildupStore = getBuildupStore();
            buildupStore.setLoading(false);
            buildupStore.setError(error instanceof Error ? error.message : `Failed to update buildup #${id}`);
            throw error;
        }
    }

    async deleteBuildup(id: number): Promise<boolean> {
        try {
            const buildupStore = getBuildupStore();
            buildupStore.setLoading(true);
            
            // Call repository to delete from backend
            const result = await this.buildupRepository.deleteBuildup(id);
            
            if (result) {
                // Update the store by removing the buildup
                buildupStore.removeBuildup(id);
            }
            this.updatedStore()
            
            buildupStore.setLoading(false);
            return result;
        } catch (error) {
            const buildupStore = getBuildupStore();
            buildupStore.setLoading(false);
            buildupStore.setError(error instanceof Error ? error.message : `Failed to delete buildup #${id}`);
            throw error;
        }
    }
    
    /**
     * Bulk delete multiple buildups
     */
    async deleteMultipleBuildups(ids: number[]): Promise<{ success: number, failed: number }> {
        const result = { success: 0, failed: 0 };
        const buildupStore = getBuildupStore();
        buildupStore.setLoading(true);
        
        try {
            for (const id of ids) {
                try {
                    const deleted = await this.buildupRepository.deleteBuildup(id);
                    if (deleted) {
                        buildupStore.removeBuildup(id);
                        result.success++;
                    } else {
                        result.failed++;
                    }
                } catch (error) {
                    console.error(`Failed to delete buildup #${id}:`, error);
                    result.failed++;
                }
            }
            
            return result;
        } finally {
            this.updatedStore()
            buildupStore.setLoading(false);
        }
    }
    

}