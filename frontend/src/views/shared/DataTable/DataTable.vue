<template>
  <div class="table-container">
    <!-- Loading and Error states -->
    <div v-if="loading" class="loading-indicator">
      Loading {{ entityNamePlural }}...
    </div>
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>
    <template v-else>
      <!-- Table -->
      <TableFilterManager
        :columns="precalculatedTable"
        @filtered-indices-changed="onFilteredIndicesChanged"
        @filters-changed="onFiltersChanged"
      >
        <template v-slot="{ filteredIndices, filters, openFilter }">
          <TableSortManager 
            :columns="precalculatedTable" 
            :rowIndices="filteredIndices"
            @sort-changed="onSortChanged"
          >
            <template v-slot="{ sortedIndices, sortConfig, setSortColumn }">
              <TablePaginationManager
                :rowIndices="sortedIndices"
                :pageSize="pageSize"
                @page-changed="onPageChanged"
              >
                <template v-slot="{ paginatedIndices, pagination }">
                  <TableSelectionManager
                    ref="selectionManagerRef"
                    :rowIndices="paginatedIndices"
                    @selection-changed="onSelectionChanged"
                  >
                    <template v-slot="{ selectedIndices, selectionManager }">
                      <table 
                      :class="`${entityName}-table`">
                        <!-- Table Header -->
                        <thead>
                          <tr>
                            <!-- Selection cell -->
                            <th class="selection-cell">
                              <input 
                                type="checkbox" 
                                :checked="selectionManager.isAllSelected" 
                                @change="selectionManager.toggleSelectAll"
                                :disabled="paginatedIndices.length === 0"
                              />
                            </th>
                            
                            <!-- Column headers with sorting and filtering -->
                            <template v-for="column in precalculatedTable" :key="column.key">
                              <TableHeaderCell
                                v-if="column.visible"
                                :column="column"
                                :sortConfig="sortConfig"
                                :filter="filters[column.key]"
                                @sort-requested="setSortColumn"
                                @filter-requested="openFilter"
                              />
                            </template>
                          </tr>
                        </thead>
                        
                        <tbody>
                          <!-- Table rows -->
                          <tr 
                            v-for="rowIndex in paginatedIndices" 
                            :key="rowIndex"
                            :class="{ 'selected': selectedIndices.includes(rowIndex) }"
                          >
                            <!-- Selection cell -->
                            <td class="selection-cell">
                              <input 
                                type="checkbox" 
                                :checked="selectedIndices.includes(rowIndex)"
                                @click="selectionManager.toggleRowSelection(rowIndex)"
                              />
                            </td>
                            
                            <template v-for="column in precalculatedTable" :key="column.key">
                              <!-- Data cells -->
                              <TableCell
                                v-if="column.visible"
                                :key="column.key"
                                :column="column"
                                :rowIndex="rowIndex"
                              >
                              <!-- Forward command cell slot -->
                              <template v-if="column.columnProperties?.type === 'command'" v-slot:command-cell="slotProps">
                                <slot name="command-cell" v-bind="slotProps"></slot>
                              </template>
                              </TableCell>
                            </template>
                            
                          </tr>
                          
                          <!-- Empty state -->
                          <tr v-if="paginatedIndices.length === 0">
                            <td :colspan="precalculatedTable.length + 1" class="empty-state">
                              No {{ entityNamePlural }} found. Please check your filters or try again.
                            </td>
                          </tr>
                        </tbody>
                      </table>
                      
                      <!-- Pagination controls -->
                      <TablePagination
                        :pagination="pagination"
                        @page-change="pagination.goToPage"
                      />
                    </template>
                  </TableSelectionManager>
                </template>
              </TablePaginationManager>
            </template>
          </TableSortManager>
        </template>
      </TableFilterManager>
    </template>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, watch, type PropType } from 'vue';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';

// Import components
import TableFilterManager from '@/views/shared/TableComponents/TableFilterManager.vue';
import TableSortManager from '@/views/shared/TableComponents/TableSortManager.vue';
import TablePaginationManager from '@/views/shared/TableComponents/TablePaginationManager.vue';
import TableSelectionManager from '@/views/shared/TableComponents/TableSelectionManager.vue';
import TableHeaderCell from '@/views/shared/TableComponents/TableHeaderCell.vue';
import TableCell from '@/views/shared/TableComponents/TableCell.vue';
import TablePagination from '@/views/shared/TableComponents/TablePagination.vue';

export default defineComponent({
  name: 'DataTable',
  components: {
    TableFilterManager,
    TableSortManager,
    TablePaginationManager,
    TableSelectionManager,
    TableHeaderCell,
    TableCell,
    TablePagination
  },
  
  props: {
    // Core data - already precalculated by the relevant <Entity>DataService
    precalculatedTable: {
      type: Array as PropType<ColumnDefinition[]>,
      required: true,
      default: () => []
    },
    
    // State
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: undefined
    },
    selectedElements : {
      type: Array as PropType<number[]>,
      default: () => []
    },
    
    // Options
    pageSize: {
      type: Number,
      default: 10
    },

    entityName: {
      type: String,
      default: "entity"
    },
    entityNamePlural: {
      type: String,
      default: "entities"
    },
  },
  
  emits: ['selection-changed', 'filtered-indices-changed'],
  
  setup(props, { emit }) {

    // state handler
    interface SelectionManagerInterface {
    selectionManager: {
      setSelection: (selection: number[]) => void;
      isAllSelected: boolean;
      toggleRowSelection: (rowIndex: number) => void;
      toggleSelectAll: () => void;
    }
  }
    const selectionManagerRef = ref<SelectionManagerInterface | null>(null);

    watch(() => props.selectedElements, (newSelection) => {
    if (selectionManagerRef.value && newSelection) {
      // Using the setSelection method we defined in TableSelectionManager
      selectionManagerRef.value.selectionManager.setSelection(newSelection);
    }
  }, { immediate: true });  // immediate:true ensures it runs on component mount

  
    // Event handlers from manager components
    function onFiltersChanged(filters: any) {
      // We can store this state if needed, but filter manager already manages it internally
      console.log('Filters changed:', filters);
    }
    
    function onSortChanged(sortConfig: any) {
      // We can store this state if needed, but sort manager already manages it internally
      console.log('Sort changed:', sortConfig);
    }
    
    function onPageChanged(pageInfo: any) {
      // We can store this state if needed, but pagination manager already manages it internally
      console.log('Page changed:', pageInfo);
    }
    
    function onSelectionChanged(selectedIndices: number[]) {
      // Pass selection to parent component
      emit('selection-changed', selectedIndices);
    }

    function onFilteredIndicesChanged(filteredIndices: number[]) {
      emit('filtered-indices-changed', filteredIndices);
    }
    
    return {
      // state
      selectionManagerRef,
      // Event handlers
      onFiltersChanged,
      onSortChanged,
      onPageChanged,
      onSelectionChanged,
      onFilteredIndicesChanged
    };
  }
});
</script>

<style scoped>


.loading-indicator,
.error-message {
  padding: 2rem;
  text-align: center;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.error-message {
  color: #e53935;
}

.product-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #ddd;
  margin-bottom: 1rem;
}

.selection-cell {
  width: 40px;
  text-align: center;
  padding: 0.75rem;
  border: 1px solid #ddd;
}

.selected {
  background-color: #f5f5f5;
}

.empty-state {
  padding: 2rem;
  text-align: center;
  color: #757575;
}
</style>