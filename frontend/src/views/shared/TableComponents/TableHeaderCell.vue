<template>
    <th 
      class="column-header"
      :class="{ 'sorted': sortConfig.key === column.key }"
      @click="$emit('sort-requested', column.key)"
    >
      <div class="column-header-content">
        <span>{{ column.label }}</span>
        
        <span v-if="sortConfig.key === column.key" class="sort-indicator">
          {{ sortConfig.direction === 'asc' ? '▲' : '▼' }}
        </span>
        
        <button 
          v-if="hasFilter"
          class="filter-button"
          @click.stop="$emit('filter-requested', column)"
          :class="{ 'has-active-filter': !!filter }"
        >
          <span>📋</span>
        </button>
      </div>
    </th>
  </template>
  
  <script lang="ts">
  import { defineComponent, computed, type PropType } from 'vue';
  import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
  import { ColumnFilterOperator } from '@/views/shared/ColumnSelector/ColumnFilterOperator';
  
  interface SortConfig {
    key: string;
    direction: 'asc' | 'desc';
  }
  
  export default defineComponent({
    name: 'TableHeaderCell',
    
    props: {
      column: {
        type: Object as PropType<ColumnDefinition>,
        required: true
      },
      sortConfig: {
        type: Object as PropType<SortConfig>,
        required: true
      },
      filter: {
        type: Object as PropType<{ value: any, operator: ColumnFilterOperator } | undefined>,
        default: undefined
      }
    },
    
    emits: ['sort-requested', 'filter-requested'],
    
    setup(props) {
      // Check if column has filter capability
      const hasFilter = computed(() => {
        return !!props.column.columnProperties?.filter;
      });
      
      return {
        hasFilter
      };
    }
  });
  </script>
  
  <style scoped>
  .column-header {
    cursor: pointer;
    user-select: none;
    background-color: #f5f5f5;
    padding: 0.75rem;
    border: 1px solid #ddd;
    text-align: left;
    position: relative;
  }
  
  .column-header:hover {
    background-color: #eee;
  }
  
  .column-header.sorted {
    background-color: #e8eaf6;
  }
  
  .column-header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .sort-indicator {
    margin-left: 0.5rem;
    font-size: 0.8rem;
  }
  
  .filter-button {
    background: none;
    border: none;
    cursor: pointer;
    margin-left: 0.5rem;
    padding: 0.25rem;
    border-radius: 3px;
  }
  
  .filter-button:hover {
    background-color: #e0e0e0;
  }
  
  .filter-button.has-active-filter {
    color: #2196f3;
  }
  </style>