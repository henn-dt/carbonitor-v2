<template>
    <div class="active-filters">
      <div class="filters-header">
        <span>Active Filters:</span>
        <button @click="$emit('clear-all')" class="clear-all-button">Clear All</button>
      </div>
      <div class="filter-chips">
        <TableActiveFilterChip
          v-for="(filter, key) in filters" 
          :key="key" 
          :label="getColumnLabel(key)"
          :operator="filter.operator"
          :value="filter.value"
          :columnType="getColumnType(key)"
          @remove="$emit('remove-filter', key)"
        />
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, type PropType } from 'vue';
  import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
  import { ColumnFilterOperator } from '@/views/shared/ColumnSelector/ColumnFilterOperator';
  import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';
  import TableActiveFilterChip from '@/views/shared/TableComponents/TableActiveFilterChip.vue';
  
  export default defineComponent({
    name: 'TableActiveFilters',
    components: {
      TableActiveFilterChip
    },
    
    props: {
      filters: {
        type: Object as PropType<Record<string, { value: any, operator: ColumnFilterOperator }>>,
        required: true
      },
      columns: {
        type: Array as PropType<ColumnDefinition[]>,
        required: true
      }
    },
    
    emits: ['remove-filter', 'clear-all'],
    
    setup(props) {
      // Get column label from key
      function getColumnLabel(key: string): string {
        const column = props.columns.find(col => col.key === key);
        return column?.label || key;
      }
      
      // Get column type from key
      function getColumnType(key: string): ColumnType | null | undefined {
        const column = props.columns.find(col => col.key === key);
        return column?.columnProperties?.type;
      }
      
      return {
        getColumnLabel,
        getColumnType
      };
    }
  });
  </script>
  
  <style scoped>
  .active-filters {
    margin-bottom: 1rem;
    padding: 0.75rem;
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .filters-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
    font-weight: bold;
  }
  
  .clear-all-button {
    background: none;
    border: none;
    color: #f44336;
    cursor: pointer;
    font-size: 0.8rem;
    text-decoration: underline;
  }
  
  .filter-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  </style>