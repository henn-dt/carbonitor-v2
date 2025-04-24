<template>
  <div class="graph-type-selector">
    <div class="selector-label">Graph Type:</div>
    <div class="type-buttons">
      <button 
        v-for="type in graphTypes" 
        :key="type.key"
        :class="['type-button', { active: graphType === type.key }]"
        @click="$emit('update:graphType', type.key)"
      >
        <span class="icon">{{ type.icon }}</span>
        <span class="label">{{ type.label }}</span>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'BuildupGraphTypeSelector',
  props: {
    graphType: {
      type: String,
      required: true
    }
  },
  emits: ['update:graphType'],
  setup() {
    const graphTypes = [
      { key: 'bar', label: 'Bar', icon: '📊' },
      { key: 'scatter', label: 'Scatter', icon: '📈' },
      { key: 'lifeCycleComparison', label: 'GWP Lifecycle', icon: '🔄' }
    ];
    
    return {
      graphTypes
    };
  }
});
</script>

<style scoped>
.graph-type-selector {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.selector-label {
  font-weight: 600;
}

.type-buttons {
  display: flex;
  gap: 0.5rem;
}

.type-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.type-button:hover {
  background-color: #f0f0f0;
}

.type-button.active {
  background-color: #e0f0ff;
  border-color: #3490dc;
  color: #3490dc;
}

.icon {
  font-size: 1.2rem;
}
</style>