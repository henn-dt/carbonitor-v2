<template>
    <div class="filter-component">
      <div class="filter-header">
        <h3>Filter: {{ column.label }}</h3>
        <button @click="$emit('close')" class="close-button">×</button>
      </div>
      
      <div class="filter-body">
        <!-- Operator Selection -->
        <div class="filter-section" v-if="availableOperators.length > 1">
          <label>Operator</label>
          <div class="operator-selection">
            <button 
              v-for="op in availableOperators"
              :key="op"
              @click="currentOperator = op"
              :class="{ active: currentOperator === op }"
              class="operator-button"
            >
              {{ getOperatorLabel(op) }}
            </button>
          </div>
        </div>
        
        <!-- Filter Value Input - adapts to column type -->
        <div class="filter-section">
          <label>Value</label>
          
          <!-- String input -->
          <input 
            v-if="columnType === 'string'"
            type="text"
            v-model="currentValue"
            class="filter-input"
            placeholder="Enter text..."
          />
          
          <!-- Numeric input -->
          <input 
            v-else-if="columnType === 'numeric'"
            type="number"
            v-model.number="currentValue"
            class="filter-input"
            placeholder="Enter number..."
            step="any"
          />
          
          <!-- Date input -->
          <input 
            v-else-if="columnType === 'date'"
            type="date"
            v-model="currentValue"
            class="filter-input"
          />
          
          <!-- Default input for unknown types -->
          <input 
            v-else
            type="text"
            v-model="currentValue"
            class="filter-input"
            placeholder="Enter value..."
          />
        </div>
      </div>
      
      <div class="filter-footer">
        <button 
          @click="applyFilter" 
          class="action-button apply"
          :disabled="!isValidValue"
        >
          Apply
        </button>
        
        <button 
          @click="clearFilter" 
          class="action-button clear"
          :disabled="!hasExistingFilter"
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
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, computed, onMounted, type PropType } from 'vue';
  import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
  import { ColumnFilterOperator } from '@/views/shared/ColumnSelector/ColumnFilterOperator';
  import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';
  
  export default defineComponent({
    name: 'TableFilter',
    
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
      
      // Get column type
      const columnType = computed(() => {
        return props.column.columnProperties?.type || 'string';
      });
      
      // Get available operators from column definition
      const availableOperators = computed(() => {
        const operators = props.column.columnProperties?.filter?.operators || [];
        if (operators.length === 0) {
          // Default operators based on column type if none specified
          switch (columnType.value) {
            case ColumnType.numeric:
            case ColumnType.date:
              return [ColumnFilterOperator.gt, ColumnFilterOperator.lt];
            default:
              return [ColumnFilterOperator.consists];
          }
        }
        return operators;
      });
      
      // Check if we have an existing filter
      const hasExistingFilter = computed(() => {
        return !!props.filter;
      });
      
      // Check if current value is valid for filtering
      const isValidValue = computed(() => {
        if (currentValue.value === null || currentValue.value === undefined) return false;
        
        if (typeof currentValue.value === 'string') {
          return currentValue.value.trim() !== '';
        }
        
        if (typeof currentValue.value === 'number') {
          return !isNaN(currentValue.value);
        }
        
        return true;
      });
      
      // Initialize with existing filter if provided
      onMounted(() => {
        if (props.filter) {
          currentValue.value = props.filter.value;
          currentOperator.value = props.filter.operator;
        } else {
          // Set default operator from column definition if available
          const defaultOp = props.column.columnProperties?.filter?.defaultOperator;
          if (defaultOp) {
            currentOperator.value = defaultOp;
          }
        }
      });
      
      // Get label for operator
      function getOperatorLabel(operator: ColumnFilterOperator): string {
        switch (operator) {
          case ColumnFilterOperator.gt:
            return columnType.value === ColumnType.date ? 'After' : '>';
          case ColumnFilterOperator.lt:
            return columnType.value === ColumnType.date ? 'Before' : '<';
          case ColumnFilterOperator.consists:
            return 'Contains';
          default:
            return String(operator);
        }
      }
      
      // Apply the current filter
      function applyFilter() {
        if (!isValidValue.value) return;
        
        emit('apply', {
          value: currentValue.value,
          operator: currentOperator.value
        });
      }
      
      // Clear the filter
      function clearFilter() {
        emit('clear');
        currentValue.value = '';
      }
      
      return {
        currentValue,
        currentOperator,
        columnType,
        availableOperators,
        hasExistingFilter,
        isValidValue,
        getOperatorLabel,
        applyFilter,
        clearFilter
      };
    }
  });
  </script>
  
  <style scoped>
  .filter-component {
    width: 100%;
  }
  
  .filter-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #e0e0e0;
    background-color: #f5f5f5;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
  }
  
  .filter-header h3 {
    margin: 0;
    font-size: 1rem;
  }
  
  .close-button {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0;
    line-height: 1;
  }
  
  .filter-body {
    padding: 1rem;
  }
  
  .filter-section {
    margin-bottom: 1rem;
  }
  
  .filter-section label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
    color: #555;
  }
  
  .operator-selection {
    display: flex;
    gap: 0.5rem;
  }
  
  .operator-button {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid #ddd;
    background-color: #f9f9f9;
    cursor: pointer;
    font-weight: bold;
    border-radius: 4px;
  }
  
  .operator-button.active {
    background-color: #2196f3;
    color: white;
    border-color: #1e88e5;
  }
  
  .filter-input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }
  
  .filter-footer {
    display: flex;
    padding: 1rem;
    border-top: 1px solid #e0e0e0;
    background-color: #f5f5f5;
    gap: 0.5rem;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
  }
  
  .action-button {
    flex: 1;
    padding: 0.5rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
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