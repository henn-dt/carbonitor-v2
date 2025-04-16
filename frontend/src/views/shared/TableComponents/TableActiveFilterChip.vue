<template>
    <div class="filter-chip">
      <span class="filter-label">{{ label }}</span>
      <span class="filter-operator">{{ operatorLabel }}</span>
      <span class="filter-value">{{ formattedValue }}</span>
      <button 
        @click="$emit('remove')" 
        class="remove-filter"
        title="Remove filter"
      >
        ×
      </button>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, computed, type PropType } from 'vue';
  import { ColumnFilterOperator } from '@/views/shared/ColumnSelector/ColumnFilterOperator';
  import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';
  
  export default defineComponent({
    name: 'TableActiveFilterChip',
    
    props: {
      label: {
        type: String,
        required: true
      },
      operator: {
        type: String as PropType<ColumnFilterOperator>,
        required: true
      },
      value: {
        type: [String, Number, Boolean, Date] as PropType<any>,
        required: true
      },
      columnType: {
        type: String as PropType<ColumnType | null | undefined>,
        default: undefined
      }
    },
    
    emits: ['remove'],
    
    setup(props) {
      // Get display label for filter operator
      const operatorLabel = computed(() => {
        switch (props.operator) {
          case ColumnFilterOperator.consists: return 'contains';
          case ColumnFilterOperator.gt: return 'is greater than';
          case ColumnFilterOperator.lt: return 'is less than';
          default: return String(props.operator);
        }
      });
      
      // Format value based on column type
      const formattedValue = computed(() => {
        const value = props.value;
        
        if (value === null || value === undefined) return '';
        
        switch (props.columnType) {
          case ColumnType.numeric:
            return typeof value === 'number' 
              ? value.toLocaleString()
              : String(value);
            
          case ColumnType.date:
            try {
              const date = new Date(value);
              return date.toLocaleDateString();
            } catch (e) {
              return String(value);
            }
            
          default:
            return String(value);
        }
      });
      
      return {
        operatorLabel,
        formattedValue
      };
    }
  });
  </script>
  
  <style scoped>
  .filter-chip {
    display: inline-flex;
    align-items: center;
    background-color: #e0e0e0;
    padding: 0.3rem 0.6rem;
    border-radius: 16px;
    font-size: 0.85rem;
  }
  
  .filter-label {
    font-weight: bold;
    margin-right: 0.25rem;
  }
  
  .filter-operator {
    color: #555;
    margin-right: 0.25rem;
  }
  
  .filter-value {
    margin-right: 0.5rem;
  }
  
  .remove-filter {
    background: none;
    border: none;
    color: #555;
    cursor: pointer;
    font-size: 1rem;
    line-height: 1;
    padding: 0 0.25rem;
    border-radius: 50%;
  }
  
  .remove-filter:hover {
    background-color: rgba(0, 0, 0, 0.1);
  }
  </style>