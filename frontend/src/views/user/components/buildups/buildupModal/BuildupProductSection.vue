<!-- BuildupProductsSection.vue -->
<template>
  <div class="products-section mapping-item">
    <div class="mapping-header">
      <div class="flex-row">
      <h2 class="form-group cozy">Buildup Composition</h2>
      <div class="form-checkbox">        
        <span class="icon new":disabled="disabled"></span>
        <label for="buildup-name" >Add group</label>
      </div>
    </div>
    </div>
    <div class="mapping-section">
      <div v-if="!mappingNames" class="no-mappings-message">
        No mapping elements found. Click "Add Mapping Element" to create one.
      </div>
      
      <MappingElement
        v-for="mappingName in mappingNames"
        :key="mappingName"
        :mappingName="mappingName"
        :buildupData="buildupData"
        :rowIds="productRowIdsForMapping(mappingName)"
        :disabled="disabled"
        :selectedIndicatorKey="$props.selectedIndicatorKey"
        :selectedLifeCycle="$props.selectedLifeCycle"
        @update:quantity="emitQuantityUpdate"
        @update:products="(payload) => $emit('update:products', payload)"
        @selectMappingElement="emitMappingSelection"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType, computed, watch } from 'vue'


import { getDefaultLifeCycleStages } from '@/views/shared/LifeCycle/LifeCycleDefinitons';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import type { ImpactCategoryKey } from 'lcax';


import MappingElement from '@/views/user/components/buildups/buildupModal/MappingElement.vue'

export default defineComponent({
  components: { MappingElement },
  props: {
    buildupData: {
      type: Array as PropType<ColumnDefinition[]>,
      required: true
    },
    selectedIndicatorKey: {
      type: String as PropType<ImpactCategoryKey>,
      default: "gwp"
    },
    selectedLifeCycle: {
      type: Object as PropType<ColumnDefinition[]>,
      default: getDefaultLifeCycleStages()
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  emits: [ "selectMappingElement", "update:quantity", "update:products"],
  setup(props, { emit }) {
    // Get all mapping element names
    const mappingCol = computed(
    () => props.buildupData.find(c => c.key === "mappingElement")
  );
  const mappingNames = computed(() =>
    mappingCol.value
      ? [
          ...new Set(
            mappingCol.value.columnValues!.map((row) => row.value)
          ),
        ]
      : []
  );

  // Helper for getting all rowIds for a mapping
  function productRowIdsForMapping(mappingName: string) {
    return mappingCol.value
      ? mappingCol.value.columnValues!
          .filter((row) => row.value === mappingName)
          .map((row) => row.rowId)
      : [];
  }

  function emitQuantityUpdate(payload: {productMapId: string, newQuantity: number}) {
      console.log(`product section emitting quantity update  ${payload.productMapId} to ${payload.newQuantity}`)
    emit("update:quantity", payload);
    }
  // You can pass either rowIds or objects to MappingElement.
  // Here we pass rowIds to avoid defining a ProductRow type.

  function emitMappingSelection(mappingElementId : string) {
  emit('selectMappingElement', mappingElementId); 
}
  return {
    mappingNames,
    productRowIdsForMapping,
    emitQuantityUpdate,
    emitMappingSelection
  };
  }




});
</script>

<style scoped>

.mapping-header {
    background-color: var(--color-light);
    padding: var(--spacing-sm) var(--spacing-md);
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.form-section {
    border-bottom: 1px solid var(--color-light);
}

.mapping-item {
  border: 1px solid var(--color-grey);
  border-radius: var(--rad-small);
  padding: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
  background-color: var(--color-light);
}

.no-mappings-message {
  padding: 1rem;
  color: var(--color-text-muted);
  font-style: italic;
  text-align: center;
  border: 1px dashed var(--color-border);
  border-radius: var(--border-radius);
  margin: 1rem 0;
}
</style>