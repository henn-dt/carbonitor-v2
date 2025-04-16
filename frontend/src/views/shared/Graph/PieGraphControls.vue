<template>
  <div class="pie-graph-controls">
    <div class="pie-info-text">
      <p>Pie charts only display selection. <strong>{{ selectedProductsCount || 'No' }} products currently selected.</strong></p>
    </div>
    
    <div class="control-row">
      <!-- Slice By (Category) -->
      <div class="control-group">
        <label for="sliceBy">Slice By:</label>
        <select 
          id="sliceBy"
          :value="sliceBy"
          @change="handleSliceByChange"
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
      
      <!-- Value Column (what to measure) -->
      <div class="control-group">
        <label for="valueColumn">Values:</label>
        <select 
          id="valueColumn"
          :value="valueColumn"
          @change="handleValueColumnChange"
        >
          <option 
            v-for="col in availableNumericColumns" 
            :key="col.key" 
            :value="col.key"
          >
            {{ col.label }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';

export default defineComponent({
  name: 'PieGraphControls',
  props: {
    availableColumns: {
      type: Array as () => ColumnDefinition[],
      required: true
    },
    sliceBy: {
      type: String,
      required: true
    },
    valueColumn: {
      type: String,
      required: true
    },
    selectedProductsCount: {
      type: Number,
      default: 0
    }
  },
  emits: [
    'update:sliceBy',
    'update:valueColumn'
  ],
  setup(props, { emit }) {
    // Handle event changes with proper typecasting
    const handleSliceByChange = (event: Event) => {
      const target = event.target as HTMLSelectElement;
      emit('update:sliceBy', target.value);
    };

    const handleValueColumnChange = (event: Event) => {
      const target = event.target as HTMLSelectElement;
      emit('update:valueColumn', target.value);
    };

    // Filter to only string columns for slicing
    const availableStringColumns = computed<ColumnDefinition[]>(() => {
      return props.availableColumns.filter(col => 
        col.columnProperties?.type === ColumnType.string || 
        col.columnProperties?.type === ColumnType.date
      );
    });
    
    // Filter to only numeric columns for values
    const availableNumericColumns = computed<ColumnDefinition[]>(() => {
      return props.availableColumns.filter(col => 
        col.columnProperties?.type === ColumnType.numeric
      );
    });
    
    return {
      availableStringColumns,
      availableNumericColumns,
      handleSliceByChange,
      handleValueColumnChange
    };
  }
});
</script>

<style scoped>
.pie-graph-controls {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.pie-info-text {
  background-color: #f0f7ff;
  border-left: 4px solid #3490dc;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  border-radius: 0 4px 4px 0;
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