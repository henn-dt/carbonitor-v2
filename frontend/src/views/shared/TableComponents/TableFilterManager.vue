<template>
  <div class="filter-manager">
    <!-- Active filters display -->
    <TableActiveFilters
      v-if="hasFilters"
      :filters="filters"
      :columns="columns"
      @remove-filter="removeFilter"
      @clear-all="clearAllFilters"
    />
    
    <!-- Single unified filter component -->
    <div v-if="activeFilterColumn !== null" class="filter-overlay" @click="closeFilterModal">
      <!-- Prevent click propagation to overlay -->
      <div class="filter-component-container" @click.stop>
        <TableFilter
          :column="activeFilterColumn"
          :filter="activeFilterColumn ? filters[activeFilterColumn.key] : undefined"
          @apply="(filter) => activeFilterColumn && applyFilter(activeFilterColumn.key, filter)"
          @clear="() => activeFilterColumn && clearColumnFilter(activeFilterColumn.key)"
          @close="closeFilterModal"
        />
      </div>
    </div>
    
    <!-- Slot that receives filtered indices -->
    <slot 
      :filteredIndices="filteredIndices" 
      :filters="filters"
      :openFilter="openFilter"
    ></slot>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, watch, nextTick, type PropType } from 'vue';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import { ColumnFilterOperator } from '@/views/shared/ColumnSelector/ColumnFilterOperator';
import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';
import TableActiveFilters from '@/views/shared/TableComponents/TableActiveFilters.vue';
import TableFilter from '@/views/shared/TableComponents/TableFilter.vue';

export default defineComponent({
  name: 'TableFilterManager',
  components: {
    TableActiveFilters,
    TableFilter
  },
  
  props: {
    // Column definitions
    columns: {
      type: Array as PropType<ColumnDefinition[]>,
      required: true
    }
  },
  
  emits: ['filters-changed','filtered-indices-changed'],
  
  setup(props, { emit }) {
    // Filter state
    const filters = ref<Record<string, { value: any, operator: ColumnFilterOperator }>>({});
    const activeFilterColumn = ref<ColumnDefinition | null>(null);
    
    // Total row count (from first column's values)
    const rowCount = computed(() => {
      if (!props.columns.length) return 0;
      return props.columns[0]?.columnValues?.length || 0;
    });
    
    // Check if we have any active filters
    const hasFilters = computed(() => {
      return Object.keys(filters.value).length > 0;
    });
    
    // Create a base array of all indices once
    const allIndices = ref<number[]>([]);
    
    // Update all indices when row count changes
    watch(rowCount, (newCount) => {
      allIndices.value = Array.from({ length: newCount }, (_, i) => i);
    }, { immediate: true });
    
    // Calculate filtered indices without creating new arrays on each run
    const filteredIndices = computed(() => {
      // If no rows or no filters, return appropriate array
      if (rowCount.value === 0) return [];
      if (!hasFilters.value) return allIndices.value;
      
      // Start with all indices and filter them
      return allIndices.value.filter(rowIndex => {
        // Check each filter
        for (const [key, filter] of Object.entries(filters.value)) {
          if (filter.value === undefined || filter.value === null || filter.value === '') continue;
          
          const column = props.columns.find(col => col.key === key);
          if (!column || !column.columnValues) continue;
          
          const columnValue = column.columnValues[rowIndex];
          if (columnValue === undefined || columnValue === null) return false;
          
          // If any filter doesn't match, exclude this index
          if (!matchesFilter(
            columnValue.value,
            filter.value,
            filter.operator,
            column.columnProperties?.type
          )) {
            return false;
          }
        }
        // All filters matched (or no filters)
        return true;
      });
    });
    
    // Pure function to generate filtered indices - not a computed property
    function calculateFilteredIndices() {
      if (rowCount.value === 0) return [];
      
      let indices = Array.from({ length: rowCount.value }, (_, i) => i);
      
      if (!hasFilters.value) return indices;
      
      for (const [key, filter] of Object.entries(filters.value)) {
        if (filter.value === undefined || filter.value === null || filter.value === '') continue;
        
        const column = props.columns.find(col => col.key === key);
        if (!column || !column.columnValues) {
          console.warn(`Column not found or no values: ${key}`);
          continue;
        }
        
        indices = indices.filter(rowIndex => {
          const columnValue = column.columnValues?.[rowIndex];
          if (columnValue === undefined || columnValue === null) return false;
          
          return matchesFilter(
            columnValue.value,
            filter.value,
            filter.operator,
            column.columnProperties?.type
          );
        });
      }
      
      return indices;
    }

    // Handle emissions when filters change
    watch(filters, (newFilters) => {
      // Emit the filters-changed event immediately
      emit('filters-changed', newFilters);
      
      // Use nextTick to ensure UI responsiveness
      nextTick(() => {
        // Calculate indices in the handler, not using computed
        const indices = calculateFilteredIndices();
        emit('filtered-indices-changed', indices);
      });
    }, { deep: true });
    
    // Initial emission
    nextTick(() => {
      const indices = calculateFilteredIndices();
      emit('filtered-indices-changed', indices);
    });
    
    // Open filter modal/dropdown for a column
    function openFilter(column: ColumnDefinition | null) {
      if (column && column.columnProperties?.filter) {
        activeFilterColumn.value = column;
      }
    }
    
    // Close filter modal/dropdown
    function closeFilterModal() {
      activeFilterColumn.value = null;
    }
    
    // Apply a filter
    function applyFilter(columnKey: string, filter: { value: any, operator: ColumnFilterOperator }) {
      if (!filter.value && filter.value !== 0) return;
      
      filters.value = {
        ...filters.value,
        [columnKey]: filter
      };
      closeFilterModal();
    }
    
    // Clear filter for a specific column
    function clearColumnFilter(columnKey: string) {
      if (filters.value[columnKey]) {
        const { [columnKey]: _, ...rest } = filters.value;
        filters.value = rest;
      }
    }
    
    // Remove a filter (from active filters display)
    function removeFilter(key: string) {
      clearColumnFilter(key);
    }
    
    // Clear all filters
    function clearAllFilters() {
      filters.value = {};
    }
    
    // Helper function to check if a value matches a filter
    function matchesFilter(
      value: any, 
      filterValue: any, 
      operator: ColumnFilterOperator, 
      type?: ColumnType | null
    ): boolean {
      // Handle null/undefined values
      if (value === undefined || value === null) {
        return false;
      }
      
      switch (type) {
        case ColumnType.string:
          const strValue = String(value).toLowerCase();
          const strFilter = String(filterValue).toLowerCase();
          if (operator === ColumnFilterOperator.consists) {
            return strValue.includes(strFilter);
          }
          break;
          
        case ColumnType.numeric:
          const numValue = Number(value);
          const numFilter = Number(filterValue);
          
          if (isNaN(numValue) || isNaN(numFilter)) {
            return false;
          }
          
          if (operator === ColumnFilterOperator.gt) {
            return numValue > numFilter;
          } else if (operator === ColumnFilterOperator.lt) {
            return numValue < numFilter;
          }
          break;
          
        case ColumnType.date:
          try {
            const dateValue = value instanceof Date ? value : new Date(value);
            const dateFilter = filterValue instanceof Date ? filterValue : new Date(filterValue);
            
            if (operator === ColumnFilterOperator.gt) {
              return dateValue > dateFilter;
            } else if (operator === ColumnFilterOperator.lt) {
              return dateValue < dateFilter;
            }
          } catch (e) {
            console.error('Date comparison error:', e);
            return false;
          }
          break;
      }
      // Default fallback for unknown types
      return String(value).toLowerCase().includes(String(filterValue).toLowerCase());
    }
    
    return {
      filters,
      hasFilters,
      filteredIndices,
      activeFilterColumn,
      openFilter,
      closeFilterModal,
      applyFilter,
      clearColumnFilter,
      removeFilter,
      clearAllFilters
    };
  }
});
</script>

<style scoped>
.filter-manager {
  width: 100%;
  position: relative;
}

.filter-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.filter-component-container {
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  max-width: 90%;
  width: 400px;
}
</style>