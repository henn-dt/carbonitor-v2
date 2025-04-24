<template>
    <div class="lifecycle-comparison-controls">
      <div class="control-row">
        <!-- X-Axis (string columns only) -->
        <div class="control-group">
          <label for="xAxis">Label:</label>
          <select 
            id="xAxis"
            :value="xAxisColumn"
            @change="handleXAxisChange"
          >
            <option 
              v-for="col in availableStringColumns" 
              :key="col.key" 
              :value="col.key"
            >
              {{ col.label }}
            </option>
          </select>
        </div>
      </div>
      
      <div class="control-row">
        <!-- Include EndOfLife Toggle -->
        <div class="control-group checkbox-group">
          <input 
            type="checkbox" 
            id="includeEndOfLife"
            :checked="includeEndOfLife"
            @change="handleEndOfLifeChange"
          >
          <label for="includeEndOfLife">Compare with/without EndOfLife (C3)</label>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, computed } from 'vue';
  import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
  import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';
  
  export default defineComponent({
    name: 'LifeCycleComparisonControls',
    props: {
      availableColumns: {
        type: Array as () => ColumnDefinition[],
        required: true
      },
      availableStringColumns: {
        type: Array as () => ColumnDefinition[],
        required: true
      },
      xAxisColumn: {
        type: String,
        required: true
      },
      yAxisColumn: {
        type: String,
        required: true
      },
      includeEndOfLife: {
        type: Boolean,
        required: true
      }
    },
    emits: [
      'update:xAxis',
      'update:yAxis',
      'update:includeEndOfLife'
    ],
    setup(props, { emit }) {
      // Filter to only show Total columns for y-axis
      const totalColumns = computed(() => {
        return props.availableColumns.filter(col => 
          col.key.includes('-Total') && 
          col.columnProperties?.type === ColumnType.numeric
        );
      });
      
      // Event handlers
      const handleXAxisChange = (event: Event) => {
        const target = event.target as HTMLSelectElement;
        emit('update:xAxis', target.value);
      };
  
      const handleYAxisChange = (event: Event) => {
        const target = event.target as HTMLSelectElement;
        emit('update:yAxis', target.value);
      };
  
      const handleEndOfLifeChange = (event: Event) => {
        const target = event.target as HTMLInputElement;
        emit('update:includeEndOfLife', target.checked);
      };
  
      return {
        totalColumns,
        handleXAxisChange,
        handleYAxisChange,
        handleEndOfLifeChange
      };
    }
  });
</script>
  
<style scoped>
  .lifecycle-comparison-controls {
    display: flex;
    flex-direction: column;
    gap: 1rem;
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
  
  .checkbox-group {
    display: flex;
    align-items: center;
  }
  
  .checkbox-group input {
    margin-right: 0.5rem;
  }
  
  label {
    font-weight: 600;
    min-width: 100px;
  }
  
  select {
    padding: 0.5rem;
    border-radius: 4px;
    border: 1px solid #ccc;
    background-color: white;
    min-width: 150px;
  }
</style>