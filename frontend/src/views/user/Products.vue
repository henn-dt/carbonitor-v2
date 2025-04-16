<template>
  <div class="sidebar-page">
    <div class="page-content">
  <!-- Header and Title -->
<!--   <h1 class="title">Products</h1>
  <h2 class="subtitle">this page lists all products in the database</h2> -->
  
  
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
  
  <!-- Graph Visualization Toggle -->
  <div class="visualization-toggle">
    <button 
      @click="showGraph = !showGraph" 
      class="toggle-btn"
    >
      {{ showGraph ? 'Hide' : 'Show' }} Graph Visualization
    </button>
  </div>
  
  <!-- Plotly Graph Component -->
  <div v-if="showGraph" class="visualization-container">
    <ProductGraph
      :precalculatedTable="precalculatedTable"
      :filteredIndices="filteredProducts"
      :selectedIndices="selectedProducts"
    />
  </div>

  <!-- Product Table -->
  <DataTable
    :precalculatedTable="precalculatedTable"
    :loading="loading"
    :error="error"
    :entityName="entityName"
    :entityNamePlural="entityNamePlural"
    @filtered-indices-changed="onFilteredIndicesChanged"
    @selection-changed="onSelectionChanged"
  />
</div>
<SelectorBar>
  <div class="selector-items-container">
      <ProductColumnSelector 
        class="product-column-selector " 
        @columnsChanged="onColumnsChanged"
      />
    </div>
    
    <!-- Impact Indicator Selector -->
    <div class="selector-items-container">
      <ImpactIndicatorSelector 
        class="product-indicator-selector" 
        @columnsChanged="onMoreIndicatorsChanged"
      />
    </div>
    
    <!-- Lifecycle Stage Selector -->
    <div class="selector-items-container">
      <LifeCycleSelector 
        class="product-lifecycle-selector" 
        @lifeCycleChanged="onLifeCycleChanged"
      />
    </div>
    </SelectorBar>
</div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed, watch, onUnmounted } from 'vue';
import { container } from '@/di/container';
import { TYPES } from '@/di/types';
import type { IProductService } from '@/services/IProductService';
import type { IImpactCalculationService } from '@/services/IImpactCalculationService';
import type { IProductWithCalculatedImpacts } from '@/types/epdx/IProductWithCalculatedImpacts';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';

// Import components
import ProductColumnSelector from '@/views/user/components/products/productColumn/ProductColumnSelector.vue';
import ImpactIndicatorSelector from '@/views/shared/ImpactIndicator/ImpactIndicatorSelector.vue';
import LifeCycleSelector from '@/views/shared/LifeCycle/LifeCycleSelector.vue';
import DataTable from '@/views/shared/DataTable/DataTable.vue';
import ProductGraph from '@/views/user/components/products/productGraph/ProductGraph.vue';
import SelectorBar from '@/views/shared/SelectorBar/SelectorBarSidebar.vue';

// Import column definitions and services
import { getAllProductColumns, getDefaultProductColumns } from '@/views/user/components/products/productColumn/ProductColumnDefinitions';
import { getDefaultImpactCategories } from '@/views/shared/ImpactIndicator/ImpactIndicatorDefinitions';
import { getDefaultLifeCycleStages } from '@/views/shared/LifeCycle/LifeCycleDefinitons';
import { ProductDataService } from '@/views/user/components/products/ProductDataService';
import { getProductService } from '@/services/ServiceAccessor';
import type { IProduct } from '@/types/product/IProduct';

export default defineComponent({
  name: 'ProductsView',
  components: {
    ProductColumnSelector,
    ImpactIndicatorSelector,
    LifeCycleSelector,
    DataTable,
    ProductGraph,
    SelectorBar
  },
  setup() {
    
    const productService = getProductService();

    const impactService = container.get<IImpactCalculationService>(TYPES.ImpactCalculationService);
    
    // State management
    const processedProducts = ref<IProductWithCalculatedImpacts[]>([]);
    const loading = ref(true);
    const error = ref<string | undefined>(undefined);
    const entityName = "product"
    const entityNamePlural = "products"
    const selectedProducts = ref<number[]>([]);
    const filteredProducts = ref<number[]>([]);
    const showDebugInfo = ref(false);
    const showVisualization = ref(false);
    const showGraph = ref(false);
    
    // Selected columns state
    const selectedColumns = ref(getAllProductColumns());
    const selectedIndicators = ref(getDefaultImpactCategories());
    const selectedLifeCycles = ref(getDefaultLifeCycleStages());

    // Subscribe to products changes
    let unsubscribe: (() => void) | null = null;

    // Process store products into component state
    const updateProcessedProducts = (products: IProduct[]) => {
      if (products && products.length > 0) {
        processedProducts.value = impactService.processProducts(products);
      }
    };
    
    
    // Computed table data
    const precalculatedTable = computed(() => {
      if (!processedProducts.value.length) {
        return [];
      }
      
      // Use the ProductDataService to transform data
      return ProductDataService.preparePrecalculatedTable(
        processedProducts.value,
        selectedColumns.value,
        selectedIndicators.value,
        selectedLifeCycles.value
      );
    });
    
    watch(precalculatedTable, () => {
      console.log(precalculatedTable);
    });
    // Fetch data on mount
    onMounted(async () => {
      try {
        loading.value = true;
        
        // Fetch products (this will use cache if available through the enhanced service)
        const products = await productService.getProducts();
        
        // Process the products
        updateProcessedProducts(products);
        
        // Subscribe to future changes
        if (!unsubscribe) {
          unsubscribe = productService.subscribeToProducts((updatedProducts) => {
            // Update the processed products when the store changes
            updateProcessedProducts(updatedProducts);
          });
        }
      } catch (err) {
        error.value = err instanceof Error ? err.message : 'Failed to load products';
        console.error('Error loading products:', err);
      } finally {
        loading.value = false;
      }
    });
    

    onUnmounted(() => {
      // Clean up subscription
      if (unsubscribe) {
        unsubscribe();
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
      selectedProducts.value = selectedIds;
      console.log("selectedProducts:");
      console.log(selectedProducts.value);
      // Here you could trigger actions based on selection
    };

    const onFilteredIndicesChanged = (filteredIndices: number[]) => {
      filteredProducts.value = filteredIndices;
      console.log("filteredProducts:");
      console.log(filteredProducts.value);
    };
    
    return {
      // State
      loading,
      error,
      entityName,
      entityNamePlural,
      selectedProducts,
      selectedColumns,
      selectedIndicators,
      selectedLifeCycles,
      filteredProducts,
      showDebugInfo,
      showVisualization,
      showGraph,
      // Computed
      precalculatedTable,
      
      // Methods
      onColumnsChanged,
      onMoreIndicatorsChanged,
      onLifeCycleChanged,
      onSelectionChanged,
      onFilteredIndicesChanged
    };
  }
});
</script>

<style scoped>


.product-column-selector,
.product-indicator-selector,
.product-lifecycle-selector {
  width: 100%;
}


.toggle-btn {
  margin: 0.5rem 0 1.5rem 0;
  padding: 0.3rem 0.75rem;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: var(--rad, 4px);
  cursor: pointer;
}

.visualization-toggle {
  margin-bottom: 1rem;
}

.visualization-container {
  margin-bottom: 2rem;
  border: 1px solid #ddd;
  border-radius: var(--rad, 4px);
  padding: 1rem;
  background-color: #f9f9f9;
}
</style>