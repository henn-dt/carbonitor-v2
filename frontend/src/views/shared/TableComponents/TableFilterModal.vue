<template>
    <div class="filter-modal">
      <div class="filter-modal-content">
        <div class="filter-modal-header">
          <h3>Filter: {{ column.label }}</h3>
          <button @click="$emit('close')" class="close-button">×</button>
        </div>
        
        <div class="filter-modal-body">
          <div class="filter-input">
            <label>Operator:</label>
            <select v-model="currentOperator">
              <option 
                v-for="op in operators" 
                :key="op" 
                :value="op"
              >
                {{ getOperatorLabel(op) }}
              </option>
            </select>
          </div>
          
          <div class="filter-input">
            <label>Value:</label>
            <input 
              :type="inputType"
              v-model="currentValue"
              placeholder="Filter value..."
            />
          </div>
        </div>
        
        <div class="filter-modal-footer">
          <button 
            @click="applyFilter" 
            class="action-button apply"
            :disabled="!currentValue"
          >
            Apply
          </button>
          
          <button 
            @click="clearFilter" 
            class="action-button clear"
            :disabled="!hasFilter"
          >
            Clear
          </button>
          
          <button 
            @click="$emit('close')" 
            class="action-button cancel"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, computed, onMounted, type PropType } from 'vue';
  import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
  import { ColumnFilterOperator } from '@/views/shared/ColumnSelector/ColumnFilterOperator';
  import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';
  
  export default defineComponent({
    name: 'TableFilterModal',
    
    props: {
      column: {
        type: Object as PropType<ColumnDefinition>,
        required: true
      },
      filter: {
        type: Object as PropType<{ value: any, operator: ColumnFilterOperator } | undefined>,
        default: undefined
      }
    },
    
    emits: ['apply', 'clear', 'close'],
    
    setup(props, { emit }) {
      // Local state for filter values
      const currentValue = ref<any>('');
      const currentOperator = ref<ColumnFilterOperator>(ColumnFilterOperator.consists);
      
      // Available operators for this column
      const operators = computed(() => {
        if (props.column.columnProperties?.filter?.operators) {
          return props.column.columnProperties.filter.operators;
        }
        
        // Default operators based on column type
        switch (props.column.columnProperties?.type) {
          case ColumnType.numeric:
          case ColumnType.date:
            return [ColumnFilterOperator.gt, ColumnFilterOperator.lt];
          
          case ColumnType.string:
          default:
            return [ColumnFilterOperator.consists];
        }
      });
      
      // Input type based on column type
      const inputType = computed(() => {
        switch (props.column.columnProperties?.type) {
          case ColumnType.numeric: return 'number';
          case ColumnType.date: return 'date';
          default: return 'text';
        }
      });
      
      // Check if column has an active filter
      const hasFilter = computed(() => {
        return !!props.filter;
      });
      
      // Initialize with existing filter if provided
      onMounted(() => {
        if (props.filter) {
          currentValue.value = props.filter.value;
          currentOperator.value = props.filter.operator;
        } else if (props.column.columnProperties?.filter?.defaultOperator) {
          // Use default operator from column properties
          currentOperator.value = props.column.columnProperties.filter.defaultOperator;
        }
      });
      
      // Get display label for filter operator
      function getOperatorLabel(operator: ColumnFilterOperator): string {
        switch (operator) {
          case ColumnFilterOperator.consists: return 'Contains';
          case ColumnFilterOperator.gt: return 'Greater than';
          case ColumnFilterOperator.lt: return 'Less than';
          default: return String(operator);
        }
      }
      
      // Apply filter
      function applyFilter() {
        if (!currentValue.value) return;
        
        emit('apply', props.column.key, {
          value: currentValue.value,
          operator: currentOperator.value
        });
      }
      
      // Clear filter
      function clearFilter() {
        emit('clear', props.column.key);
        currentValue.value = '';
      }
      
      return {
        currentValue,
        currentOperator,
        operators,
        inputType,
        hasFilter,
        getOperatorLabel,
        applyFilter,
        clearFilter
      };
    }
  });
  </script>
  
  <style scoped>
  .filter-modal {
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
  
  .filter-modal-content {
    background-color: white;
    border-radius: 4px;
    width: 400px;
    max-width: 90%;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .filter-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #ddd;
  }
  
  .filter-modal-header h3 {
    margin: 0;
    font-size: 1.1rem;
  }
  
  .close-button {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0;
    line-height: 1;
  }
  
  .filter-modal-body {
    padding: 1rem;
  }
  
  .filter-input {
    margin-bottom: 1rem;
  }
  
  .filter-input label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
  }
  
  .filter-input select,
  .filter-input input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .filter-modal-footer {
    display: flex;
    justify-content: flex-end;
    padding: 1rem;
    border-top: 1px solid #ddd;
    gap: 0.5rem;
  }
  
  .action-button {
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
    border: none;
  }
  
  .action-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .action-button.apply {
    background-color: #4caf50;
    color: white;
  }
  
  .action-button.clear {
    background-color: #f44336;
    color: white;
  }
  
  .action-button.cancel {
    background-color: #e0e0e0;
    color: #333;
  }
  </style>