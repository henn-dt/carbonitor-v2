<template>
    <div class="sort-manager">
      <slot 
        :sortedIndices="sortedIndices" 
        :sortConfig="sortConfig"
        :setSortColumn="setSortColumn"
      ></slot>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, computed, watchEffect, type PropType } from 'vue';
  import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
  import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';
  
  interface SortConfig {
    key: string;
    direction: 'asc' | 'desc';
  }
  
  export default defineComponent({
    name: 'TableSortManager',
    
    props: {
      // Column definitions
      columns: {
        type: Array as PropType<ColumnDefinition[]>,
        required: true
      },
      
      // Row indices pre-filtered by the filter manager
      rowIndices: {
        type: Array as PropType<number[]>,
        required: true
      }
    },
    
    emits: ['sort-changed'],
    
    setup(props, { emit }) {
      // Sort state
      const sortConfig = ref<SortConfig>({
        key: '',
        direction: 'asc'
      });
      
      // Apply sorting to filtered indices
      const sortedIndices = computed(() => {
        // No sorting if no sort key
        if (!sortConfig.value.key) {
          return [...props.rowIndices];
        }
        
        // Find sort column
        const column = props.columns.find(col => col.key === sortConfig.value.key);
        if (!column || !column.columnValues) {
          return [...props.rowIndices];
        }
        
        // Apply sorting
        return [...props.rowIndices].sort((a, b) => {
          const valueA = column.columnValues?.[a]?.value;
          const valueB = column.columnValues?.[b]?.value;
          
          return compareValues(
            valueA,
            valueB,
            column.columnProperties?.type,
            sortConfig.value.direction
          );
        });
      });
      
      // Emit changes when sort config changes
      watchEffect(() => {
        emit('sort-changed', sortConfig.value);
      });
      
      // Set sort column
      function setSortColumn(key: string): void {
        if (sortConfig.value.key === key) {
          // Toggle direction if already sorted by this column
          sortConfig.value.direction = sortConfig.value.direction === 'asc' ? 'desc' : 'asc';
        } else {
          // Set new sort column
          sortConfig.value = {
            key,
            direction: 'asc'
          };
        }
      }
      
      // Helper function to compare values for sorting
      function compareValues(
        a: any, 
        b: any, 
        type?: ColumnType | null,
        direction: 'asc' | 'desc' = 'asc'
      ): number {
        // Handle undefined/null
        if (a === undefined || a === null) return direction === 'asc' ? 1 : -1;
        if (b === undefined || b === null) return direction === 'asc' ? -1 : 1;
        
        let result = 0;
        
        // Compare based on type
        switch (type) {
          case ColumnType.numeric:
            result = Number(a) - Number(b);
            break;
            
          case ColumnType.date:
            try {
              const dateA = new Date(a).getTime();
              const dateB = new Date(b).getTime();
              result = dateA - dateB;
            } catch (e) {
              result = String(a).localeCompare(String(b));
            }
            break;
            
          case ColumnType.string:
          default:
            result = String(a).localeCompare(String(b));
            break;
        }
        
        // Reverse for descending
        return direction === 'desc' ? -result : result;
      }
      
      return {
        sortConfig,
        sortedIndices,
        setSortColumn
      };
    }
  });
  </script>
  
  <style scoped>
  .sort-manager {
    width: 100%;
  }
  </style>