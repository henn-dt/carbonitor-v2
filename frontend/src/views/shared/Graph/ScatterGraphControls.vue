<template>
  <div class="scatter-graph-controls">
    <div class="control-row">
      <!-- X-Axis -->
      <div class="control-group">
        <label for="xAxis">X-Axis:</label>
        <select 
          id="xAxis"
          :value="xAxisColumn"
          @change="handleXAxisChange"
        >
          <option 
            v-for="col in availableColumns" 
            :key="col.key" 
            :value="col.key"
          >
            {{ col.label }}
          </option>
        </select>
      </div>
      
      <!-- Y-Axis -->
      <div class="control-group">
        <label for="yAxis">Y-Axis:</label>
        <select 
          id="yAxis"
          :value="yAxisColumn"
          @change="handleYAxisChange"
        >
          <option 
            v-for="col in availableColumns" 
            :key="col.key" 
            :value="col.key"
          >
            {{ col.label }}
          </option>
        </select>
      </div>
    </div>
    
    <div class="control-row">
      <!-- Z-Axis (for 3D representation) -->
      <div class="control-group">
        <label for="zAxis">Size By (3D):</label>
        <select 
          id="zAxis"
          :value="zAxisColumn"
          @change="handleZAxisChange"
        >
          <option value="">None (2D)</option>
          <option 
            v-for="col in availableColumns" 
            :key="col.key" 
            :value="col.key"
          >
            {{ col.label }}
          </option>
        </select>
      </div>
      
      <!-- Color By -->
      <div class="control-group">
        <label for="colorBy">Color By:</label>
        <select 
          id="colorBy"
          :value="colorBy"
          @change="handleColorByChange"
        >
          <option value="none">No Grouping</option>
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
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';

export default defineComponent({
  name: 'ScatterGraphControls',
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
    zAxisColumn: {
      type: String,
      required: true
    },
    colorBy: {
      type: String,
      required: true
    }
  },
  emits: [
    'update:xAxis',
    'update:yAxis',
    'update:zAxis',
    'update:colorBy'
  ],
  setup(props, { emit }) {
    // Handle the various select changes with explicit typecasting
    const handleXAxisChange = (event: Event) => {
      const target = event.target as HTMLSelectElement;
      emit('update:xAxis', target.value);
    };

    const handleYAxisChange = (event: Event) => {
      const target = event.target as HTMLSelectElement;
      emit('update:yAxis', target.value);
    };

    const handleZAxisChange = (event: Event) => {
      const target = event.target as HTMLSelectElement;
      emit('update:zAxis', target.value);
    };

    const handleColorByChange = (event: Event) => {
      const target = event.target as HTMLSelectElement;
      emit('update:colorBy', target.value);
    };

    return {
      handleXAxisChange,
      handleYAxisChange,
      handleZAxisChange,
      handleColorByChange
    };
  }
});
</script>

<style scoped>
.scatter-graph-controls {
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