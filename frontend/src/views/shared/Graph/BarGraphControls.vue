<template>
  <div class="bar-graph-controls">
    <div class="control-row">
      <!-- X-Axis (string columns only) -->
      <div class="control-group">
        <label for="xAxis">X-Axis:</label>
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
      
      <!-- Y-Axis (any column) -->
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
      <!-- Unit Filter -->
      <div v-if="showLifecycleOption" class="control-group">
        <label for="unitFilter">Filter by Unit:</label>
        <select 
          id="unitFilter"
          :value="selectedUnit"
          @change="handleUnitChange"
        >
          <option value="">All Units</option>
          <option 
            v-for="unit in availableUnits" 
            :key="unit" 
            :value="unit"
          >
            {{ unit }}
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
          <option v-if="showLifecycleOption" value="lifecycles">LifeCycles</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';

export default defineComponent({
  name: 'BarGraphControls',
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
    colorBy: {
      type: String,
      required: true
    },
    availableUnits: {
      type: Array as () => string[],
      required: true
    },
    selectedUnit: {
      type: String,
      required: true
    },
    showLifecycleOption: {
      type: Boolean,
      required: true
    }
  },
  emits: [
    'update:xAxis',
    'update:yAxis',
    'update:colorBy',
    'update:unit'
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

    const handleColorByChange = (event: Event) => {
      const target = event.target as HTMLSelectElement;
      emit('update:colorBy', target.value);
    };

    const handleUnitChange = (event: Event) => {
      const target = event.target as HTMLSelectElement;
      emit('update:unit', target.value);
    };

    return {
      handleXAxisChange,
      handleYAxisChange,
      handleColorByChange,
      handleUnitChange
    };
  }
});
</script>

<style scoped>
.bar-graph-controls {
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
  margin-top: 0.5rem;
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