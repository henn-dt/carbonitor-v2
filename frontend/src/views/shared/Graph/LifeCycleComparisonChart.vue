<template>
  <div class="lifecycle-comparison-chart">
    <div class="controls">
      <div class="control-row">
        <!-- X-Axis (string columns only) -->
        <div class="control-group">
          <label for="xAxis">Product Name:</label>
          <select 
            id="xAxis"
            v-model="xAxisColumn"
          >
            <option 
              v-for="col in availableStringColumns" 
              :key="col.key" 
              :value="col.key"
            >
              {{ col.label }}
            </option>
          </select>
        </div>
        
        <!-- Removed Impact Indicator dropdown -->
      </div>
      
      <div class="control-row">
        <!-- Include EndOfLife Toggle -->
        <div class="control-group checkbox-group">
          <input 
            type="checkbox" 
            id="includeEndOfLife" 
            v-model="includeEndOfLife"
          >
          <label for="includeEndOfLife">Compare with/without EndOfLife (C3)</label>
        </div>
      </div>
    </div>
    
    <div ref="graphContainer" class="graph-container">
      <!-- Plotly will render here -->
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, watch, onMounted } from 'vue';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import { useLifeCycleComparisonChart } from './useLifeCycleComparisonChart';
import { useColumnUtils } from '@/views/shared/Graph/useColumnUtils';

export default defineComponent({
  name: 'LifeCycleComparisonChart',
  props: {
    precalculatedTable: {
      type: Array as () => ColumnDefinition[],
      required: true
    },
    selectedIndices: {
      type: Array as () => number[],
      required: true
    }
  },
  setup(props) {
    // DOM reference
    const graphContainer = ref<HTMLElement | null>(null);
    
    // Control state
    const xAxisColumn = ref<string>('epd_name'); // Default to product name
    // Fixed to GWP - no longer using dropdown
    const indicatorColumn = ref<string>('gwp-Total'); 
    const includeEndOfLife = ref<boolean>(true); // Default to including EndOfLife comparison
    
    // Get column utilities
    const { 
      availableColumns,
      availableStringColumns
    } = useColumnUtils(props);
    
    // Create the chart generator
    const { generateLifeCycleComparisonChart } = useLifeCycleComparisonChart(
      props,
      graphContainer,
      {
        xAxisColumn,
        indicatorColumn,
        includeEndOfLife
      }
    );
    
    // Watch for changes to redraw the chart
    watch(
      [
        xAxisColumn,
        includeEndOfLife,
        () => props.selectedIndices
      ],
      () => {
        if (props.selectedIndices.length > 0) {
          generateLifeCycleComparisonChart();
        }
      },
      { deep: true }
    );
    
    // Initialize the component
    onMounted(() => {
      // Check if we already have selected indices to display
      if (props.selectedIndices.length > 0) {
        generateLifeCycleComparisonChart();
      }
    });
    
    return {
      graphContainer,
      xAxisColumn,
      includeEndOfLife,
      availableColumns,
      availableStringColumns
    };
  }
});
</script>
  
<style scoped>
  .lifecycle-comparison-chart {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
  }
  
  .controls {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
    background-color: #f5f5f5;
    border-radius: 4px;
    margin-bottom: 1rem;
  }
  
  .control-row {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    align-items: center;
  }
  
  .control-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .checkbox-group {
    display: flex;
    align-items: center;
  }
  
  .checkbox-group input {
    margin-right: 0.5rem;
  }
  
  label {
    font-weight: 600;
  }
  
  select {
    padding: 0.5rem;
    border-radius: 4px;
    border: 1px solid #ccc;
    background-color: white;
    min-width: 200px;
  }
  
  .graph-container {
    flex-grow: 1;
    min-height: 400px;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    padding: 1rem;
    background-color: white;
  }
</style>