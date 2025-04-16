<template>
  <div class="plotly-graph">
    <div class="controls">
      <!-- Graph Type Selector -->
      <ProductGraphTypeSelector 
        :graphType="graphType" 
        @update:graphType="graphType = $event" 
      />
      
      <!-- Display mode selector (except for pie chart and lifecycle comparison) -->
      <div class="control-row" v-if="graphType !== 'pie' && graphType !== 'lifeCycleComparison'">
        <div class="control-group">
          <label for="displayMode">Display:</label>
          <select id="displayMode" v-model="displayMode">
            <option v-for="mode in displayModes" :key="mode.key" :value="mode.key">
              {{ mode.label }}
            </option>
          </select>
        </div>
      </div>
      
      <!-- Note for lifecycle comparison and pie charts -->
      <div class="note" v-if="graphType === 'pie' || graphType === 'lifeCycleComparison'">
        <p><i>Note: This graph type only displays selected elements.</i></p>
      </div>
      
      <!-- Dynamic Controls based on graph type -->
      <BarGraphControls 
        v-if="graphType === 'bar'"
        :availableColumns="availableColumns"
        :availableStringColumns="availableStringColumns"
        :xAxisColumn="xAxisColumn"
        :yAxisColumn="yAxisColumn"
        :colorBy="colorBy"
        :availableUnits="availableUnits"
        :selectedUnit="selectedUnit"
        :showLifecycleOption="showLifecycleOption"
        @update:xAxis="xAxisColumn = $event"
        @update:yAxis="yAxisColumn = $event"
        @update:colorBy="colorBy = $event"
        @update:unit="selectedUnit = $event"
      />
      
      <ScatterGraphControls
        v-if="graphType === 'scatter'"
        :availableColumns="availableColumns"
        :xAxisColumn="xAxisColumn"
        :yAxisColumn="yAxisColumn"
        :zAxisColumn="zAxisColumn"
        :colorBy="colorBy"
        :availableStringColumns="availableStringColumns"
        @update:xAxis="xAxisColumn = $event"
        @update:yAxis="yAxisColumn = $event"
        @update:zAxis="zAxisColumn = $event"
        @update:colorBy="colorBy = $event"
      />
      
      <PieGraphControls
        v-if="graphType === 'pie'"
        :availableColumns="availableColumns"
        :sliceBy="sliceBy"
        :valueColumn="valueColumn"
        @update:sliceBy="sliceBy = $event"
        @update:valueColumn="valueColumn = $event"
      />
      
      <LifeCycleComparisonControls
        v-if="graphType === 'lifeCycleComparison'"
        :availableColumns="availableColumns"
        :availableStringColumns="availableStringColumns"
        :xAxisColumn="xAxisColumn"
        :yAxisColumn="yAxisColumn"
        :includeEndOfLife="includeEndOfLife"
        @update:xAxis="xAxisColumn = $event"
        @update:yAxis="yAxisColumn = $event"
        @update:includeEndOfLife="includeEndOfLife = $event"
      />
    </div>
    
    <!-- Use computed property to check length -->
    <div class="warning" v-if="graphType === 'lifeCycleComparison' && selectedIndicesLength < 2">
      <p>Please select at least 2 products to compare.</p>
    </div>
    
    <div ref="graphContainer" class="graph-container">
      <!-- Plotly will render here -->
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, watch, onMounted, onBeforeUnmount } from 'vue';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';

// Subcomponents
import ProductGraphTypeSelector from '@/views/user/components/products/productGraph/ProductGraphTypeSelector.vue';

// Graphs
import BarGraphControls from '@/views/shared/Graph/BarGraphControls.vue';
import ScatterGraphControls from '@/views/shared/Graph/ScatterGraphControls.vue';
import PieGraphControls from '@/views/shared/Graph/PieGraphControls.vue';
import LifeCycleComparisonControls from '@/views/shared/Graph/LifeCycleComparisonControls.vue';

// Graph generators
import { useGraphGenerator } from '@/views/shared/Graph/useGraphGenerator';
import { useColumnUtils } from '@/views/shared/Graph/useColumnUtils';

export default defineComponent({
  name: 'ProductGraph',
  components: {
    ProductGraphTypeSelector,
    BarGraphControls,
    ScatterGraphControls,
    PieGraphControls,
    LifeCycleComparisonControls
  },
  props: {
    precalculatedTable: {
      type: Array as () => ColumnDefinition[],
      required: true
    },
    filteredIndices: {
      type: Array as () => number[],
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
    
    // Graph configuration
    const graphType = ref<string>('bar'); // Default to bar graph
    
    // Common state
    const displayMode = ref<string>('filtered'); // Display mode: filtered, selected, or both
    
    // Bar and Scatter graph common state
    const xAxisColumn = ref<string>('epd_name'); // Default X-axis column
    const yAxisColumn = ref<string>('gwp-Total'); // Default Y-axis column
    
    // Bar graph specific state
    const selectedUnit = ref<string>(''); // Selected unit filter
    
    // Display mode options
    const displayModes = [
      { key: 'filtered', label: 'Filtered Products' },
      { key: 'selected', label: 'Selected Products' },
      { key: 'both', label: 'Both (Selected as Benchmark)' }
    ];
    
    // Scatter graph specific state
    const zAxisColumn = ref<string>(''); // Z-axis (third dimension) for scatter
    
    // Pie graph specific state
    const sliceBy = ref<string>('epd_subtype'); // What to slice the pie by
    const valueColumn = ref<string>('gwp-Total'); // What values to use for pie sizes
    
    // Common state
    const colorBy = ref<string>('none'); // For both bar and scatter
    
    // Lifecycle comparison specific state
    const includeEndOfLife = ref<boolean>(true); // Whether to include EndOfLife in comparison

    // Computed properties for column options
    const { availableColumns, availableStringColumns, availableNumericColumns, availableUnits } = 
      useColumnUtils(props);
      
    // Create a computed property that will react to changes in the selectedIndices array
    const selectedIndicesLength = computed(() => props.selectedIndices.length);
      
    // Determine if lifecycle colors option should be shown
    const showLifecycleOption = computed(() => {
      return yAxisColumn.value.includes('-Total');
    });
    
    const { loadPlotlyCDN, generatePlot } = 
      useGraphGenerator(props, graphContainer, graphType, {
        displayMode, xAxisColumn, yAxisColumn, zAxisColumn, colorBy,
        sliceBy, valueColumn, selectedUnit, includeEndOfLife
      });
    
    // Watch for changes to redraw the plot
    watch(
      [
        graphType, 
        xAxisColumn, 
        yAxisColumn, 
        zAxisColumn, 
        colorBy, 
        sliceBy, 
        valueColumn, 
        selectedUnit,
        includeEndOfLife,
        () => props.precalculatedTable,
        () => props.filteredIndices, 
        () => props.selectedIndices
      ],
      () => {
        // For debugging - log the number of selected indices whenever the watch triggers
        console.log('Watch triggered - Selected indices length:', props.selectedIndices.length);
        generatePlot();
      },
      { deep: true }
    );
    
    // Add a dedicated watch for selectedIndices for more reliable reactivity
    watch(
      () => [...props.selectedIndices], // Create a new array to ensure reactivity
      (newSelectedIndices) => {
        console.log('Selected indices changed:', newSelectedIndices.length);
        generatePlot();
      }
    );
    
    // Initialize the component
    onMounted(async () => {
      await loadPlotlyCDN();
      generatePlot();
      console.log('Component mounted - Selected indices length:', props.selectedIndices.length);
    });
    
    // Cleanup when component unmounts
    onBeforeUnmount(() => {
      if (graphContainer.value && (window as any).Plotly) {
        (window as any).Plotly.purge(graphContainer.value);
      }
    });
    
    return {
      graphContainer,
      graphType,
      displayMode,
      displayModes,
      xAxisColumn,
      yAxisColumn,
      zAxisColumn,
      colorBy,
      selectedUnit,
      sliceBy,
      valueColumn,
      includeEndOfLife,
      availableColumns,
      availableStringColumns,
      availableUnits,
      showLifecycleOption,
      selectedIndicesLength  // Use computed property instead of direct props reference
    };
  }
});
</script>

<style scoped>
.plotly-graph {
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

.graph-container {
  flex-grow: 1;
  min-height: 400px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 1rem;
  background-color: white;
}

.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  font-size: 1.2rem;
  color: #666;
}

.warning {
  padding: 1rem;
  margin-bottom: 1rem;
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeeba;
  border-radius: 4px;
}

.note {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}
</style>