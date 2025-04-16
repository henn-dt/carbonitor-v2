<template>
    <div class="sidebar-page">
        <FilterBar>
          <template #title>
            <a class="sidebar-title">Buildups Picker</a>
          </template>
            <BuildupList 
            :buildups = collectedBuildups
            :loading = loading
            :error = error
            v-model:filteredBuildups="filteredBuildups"
            v-model:selectedBuildups="selectedBuildups"
            >
            </BuildupList>
        </FilterBar>

        <div class="page-content">
            <!-- Header and Title -->
            <h1 class="title">Buildups</h1>
            <h2 class="subtitle">browse and compare Buildups</h2>

            <div v-if="loading" class="loading-indicator">
              Loading buildups...
            </div>

            <div v-if="error" class="error-message">
              {{ error }}
            </div>
        
          <!-- Debug info - only show during development -->
          <div v-if="showDebugInfo" class="debug-info">
            <h3>Selected Configuration:</h3>
            <div class="debug-section">
              <h4>Selected Columns:</h4>
              <ul>
                <li v-for="col in selectedColumns" :key="col.key">{{ col.label }}</li>
              </ul>
            </div>
            <div class="debug-section">
              <h4>Selected Indicators:</h4>
              <ul>
                <li v-for="ind in selectedIndicators" :key="ind.key">{{ ind.label }}</li>
              </ul>
            </div>
            <div class="debug-section">
              <h4>Selected Lifecycle Stages:</h4>
              <ul>
                <li v-for="stage in selectedLifeCycles" :key="stage.key">{{ stage.label }}</li>
              </ul>
            </div>
            <button @click="showDebugInfo = false" class="toggle-btn">Hide Debug Info</button>
          </div>
          <button v-else @click="showDebugInfo = true" class="toggle-btn">Show Debug Info</button>



        <div class ="container">
        <!-- Buildup Table -->
        <DataTable
          :precalculatedTable="precalculatedTable"
          :loading="loading"
          :error="error"
          :entityName="entityName"
          :entityNamePlural="entityNamePlural"
          v-model:selectedElements="selectedBuildups"
          @filtered-indices-changed="onFilteredIndicesChanged"
          @selection-changed="onSelectionChanged"
        >

        </DataTable>


        </div>
        </div>
        <SelectorBar>

          <div class="selector-items-container">
        <BuildupColumnSelector 
        class="buildup-column-selector " 
        @columnsChanged="onColumnsChanged"
      />
    </div>
    
        <!-- Impact Indicator Selector -->
        <div class="selector-items-container">
          <ImpactIndicatorSelector 
            class="buildup-indicator-selector" 
            @columnsChanged="onMoreIndicatorsChanged"
          />
        </div>

        <!-- Lifecycle Stage Selector -->
        <div class="selector-items-container">
          <LifeCycleSelector 
            class="buildup-lifecycle-selector" 
            @lifeCycleChanged="onLifeCycleChanged"
          />
        </div>
        </SelectorBar>
        </div>

</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed, watch, onUnmounted, shallowRef } from 'vue';
import { container } from '@/di/container';
import { TYPES } from '@/di/types';

import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';

// Import components
import BuildupColumnSelector from '@/views/user/components/buildups/buildupColumn/BuildupColumnSelector.vue';
import ImpactIndicatorSelector from '@/views/shared/ImpactIndicator/ImpactIndicatorSelector.vue';
import LifeCycleSelector from '@/views/shared/LifeCycle/LifeCycleSelector.vue';
import DataTable from '@/views/shared/DataTable/DataTable.vue';

import SelectorBar from '@/views/shared/SelectorBar/SelectorBarSidebar.vue';
import FilterBar from '@/views/shared/FilterBar/FilterBarSidebar.vue';
import BuildupList from '@/views/user/components/buildups/BuildupSelector.vue'

// Import column definitions and services

import { getDefaultImpactCategories } from '@/views/shared/ImpactIndicator/ImpactIndicatorDefinitions';
import { getDefaultLifeCycleStages } from '@/views/shared/LifeCycle/LifeCycleDefinitons';

import { getBuildupService, getBuildupProcessService } from '@/services/ServiceAccessor';
import { BuildupDataService } from '@/views/user/components/buildups/BuildupDataService';

import type { IBuildup } from '@/types/buildup/IBuildup';

import { getAllBuildupColumns } from '@/views/user/components/buildups/buildupColumn/BuildupColumnDefinitions';
import BuildupsCommands from '@/views/user/components/buildups/BuildupsCommands.vue';
import { getBuildupStore } from '@/stores/storeAccessor';
import type { IBuildupWithProcessedProducts } from '@/types/epdx/IBuildupWithProcessedProducts';

export default defineComponent({
  name: 'BuildupsView',
  components: {
    ImpactIndicatorSelector,
    LifeCycleSelector,
    SelectorBar,
    FilterBar,
    BuildupList,
    BuildupColumnSelector,
    DataTable,
    BuildupsCommands,
  },
  setup() {
    const entityName = "buildup"
    const entityNamePlural = "buildups"
    const buildupService = getBuildupService();
    const buildupProcessService = getBuildupProcessService()
    const buildupStore = getBuildupStore()
    
    // State management
    const isProcessing = ref(false);
    const error = ref<string | undefined>(undefined);
    const selectedBuildups = ref<number[]>([]);
    const filteredBuildups = ref<number[]>([]);
    const showDebugInfo = ref(false);
    const showVisualization = ref(false);
    const showGraph = ref(false);

   // Monitor store loading state
   const isLoading = computed(() => {
      return buildupStore.loading || buildupStore.processingAll;
    });

    // Raw buildups from store
    const buildups = computed<IBuildup[]>(() => {
      return buildupStore.buildups;
    });
    

    // Combined buildups with processed data
    const combinedBuildups = shallowRef<(IBuildup & IBuildupWithProcessedProducts)[]>([]);
    const updateCombinedBuildups = () => {
      if (isLoading.value) return;
      
      try {
        combinedBuildups.value = buildupProcessService.getAllCombinedBuildups();
        console.log(`Updated combined buildups: ${combinedBuildups.value.length} items`);
      } catch (err) {
        console.error('Error getting combined buildups:', err);
      }
    };

    // Selected columns state
    const selectedColumns = ref(getAllBuildupColumns());
    const selectedIndicators = ref(getDefaultImpactCategories());
    const selectedLifeCycles = ref(getDefaultLifeCycleStages());
  
    // Computed table data - only calculate when not loading
    const precalculatedTable = computed(() => {
      if (isLoading.value || combinedBuildups.value.length === 0) {
        return [];
      }
      
      // Use the BuildupDataService to transform data
      return BuildupDataService.prepareBuildupTable(
        combinedBuildups.value,
        selectedColumns.value,
        selectedIndicators.value,
        selectedLifeCycles.value
      );
    });
    
    watch(filteredBuildups, (newValue) => {
      console.log("Parent: filteredBuildups changed:", newValue);
    }, { deep: true });


    // Initialize data
    const initializeData = async () => {
      try {
        isProcessing.value = true;
        // Get buildups (this will handle incremental updates internally)
        await buildupService.getBuildups();
        
        // Process buildups (this will also handle incremental updates)
        if (buildupStore.buildups.length > 0) {
          await buildupProcessService.processAllBuildups();
        }

        updateCombinedBuildups()
      } catch (err) {
        error.value = err instanceof Error ? err.message : 'Failed to load or process buildups';
        console.error('Error initializing data:', err);
      } finally {
        isProcessing.value = false;
      }
    };

    // Modified version of the subscribeToBuildupProcess
    // This is a crucial fix for breaking the infinite loop
    const createSafeSubscriptionToProcess = () => {
      return buildupProcessService.subscribeToBuildupProcess((processedBuildups) => {
        // Only update UI if we're not already processing
        if (!isProcessing.value && !isLoading.value) {
          console.log('Received processed buildups update from subscription');
          updateCombinedBuildups();
        }
      });
    };


    // Fetch data on mount
    onMounted(async () => {
      try {
        // Initialize data first
        await initializeData();
        
        // Subscribe to raw buildup changes (separate from processed buildups)
        const buildupSubscription = buildupService.subscribeToBuildups(async (buildups) => {
          // Only trigger processing if we have buildups, aren't already processing,
          // and the store isn't in a loading state
          if (buildups.length > 0 && !isProcessing.value && !isLoading.value) {
            console.log('Buildup Store changes detected, processing...');
            isProcessing.value = true;
            try {
              await buildupProcessService.processAllBuildups();
              updateCombinedBuildups();
            } finally {
              isProcessing.value = false;
            }
          }
        });
        
        // Subscribe to processed buildup changes
        const processedSubscription = createSafeSubscriptionToProcess();
        
        // Clean up subscriptions on unmount
        onUnmounted(() => {
          buildupSubscription();
          processedSubscription();
        });
      } catch (err) {
        error.value = err instanceof Error ? err.message : 'Failed to load buildups';
        console.error('Error loading buildups:', err);
      }
    });
    
    // Event handlers
    const onColumnsChanged = (columns: ColumnDefinition[]) => {
      const columnKeys: string[] = columns.map(col => col.key); 
      selectedColumns.value.forEach(element => {
        columnKeys.includes(element.key) ? element.visible = true : element.visible = false;
      });
    };
    
    const onMoreIndicatorsChanged = (columns: ColumnDefinition[]) => {
      selectedIndicators.value = columns;
    };
    
    const onLifeCycleChanged = (stages: ColumnDefinition[]) => {
      selectedLifeCycles.value = stages;
    };
    
    const onSelectionChanged = (selectedIds: number[]) => {
      selectedBuildups.value = selectedIds;
      console.log("selectedBuildups:");
      console.log(selectedBuildups.value);
      // Here you could trigger actions based on selection
    };


    // Handler for when the table changes the filtered buildups
    const onFilteredIndicesChanged = (filteredIndices: number[]) => {
      console.log("Parent: Table updated filtered buildups:", filteredIndices);
      
      // Only update if actually changed to prevent loops
      if (!arraysEqual(filteredBuildups.value, filteredIndices)) {
        filteredBuildups.value = filteredIndices;
        console.log("Parent: Updated filteredBuildups from table:", filteredBuildups.value);
      }
    };

    // Helper to compare arrays
    const arraysEqual = (a: number[], b: number[]) => {
      if (a.length !== b.length) return false;
      const sortedA = [...a].sort();
      const sortedB = [...b].sort();
      return sortedA.every((val, idx) => val === sortedB[idx]);
    };

    // Force a refresh of data
    const refreshData = async () => {
      // Set needsRefresh to true
      buildupStore.setNeedsRefresh(true);
      
      // Re-initialize data
      await initializeData();
    };
    
    return {
      // State
      loading :isLoading,
      error,
      entityName,
      entityNamePlural,
      selectedBuildups: selectedBuildups,
      filteredBuildups: filteredBuildups,
      collectedBuildups : buildups,
      selectedIndicators,
      selectedLifeCycles,
      selectedColumns,
      showDebugInfo,
      showVisualization,
      showGraph,
      precalculatedTable,
      
      // Methods
      onColumnsChanged,
      onMoreIndicatorsChanged,
      onLifeCycleChanged,
      onSelectionChanged,
      onFilteredIndicesChanged,
      refreshData
    };
  }
});


</script>

<style scoped>


.debug-info {
  margin-bottom: 1.5rem;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: var(--rad, 4px);
  background-color: #f9f9f9;
}

.debug-info h3 {
  margin-top: 0;
  margin-bottom: 0.75rem;
}

.debug-info h4 {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.debug-section {
  margin-bottom: 1rem;
}

.debug-section ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
}

.debug-section li {
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}

</style>