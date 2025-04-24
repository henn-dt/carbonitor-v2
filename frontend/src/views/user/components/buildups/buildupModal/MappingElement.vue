<!-- MappingElement.vue -->
<template>
  <div class="property-item mapping-item" @click="emitSelection">
    <div class="flex-row">
      <input 
        type="text" 
        v-model="mappingName" 
        class="mapping-name-input"
        :disabled="disabled"
      />
      <div class="form-checkbox">        
        <span class="icon new":disabled="disabled"></span>
        <label for="buildup-name" >Add product</label>
      </div>
      <span 
        class="icon remove" 
        @click="$emit('remove')" 
        :disabled="disabled"
      ></span>
    </div>
    
    <div class="products-container">
      <div v-if="buildupData.length === 0" class="no-products-message">
        No products in this mapping element. Click "Add Product" to add one.
      </div>
      
      <div v-else>
        <!-- Header Row -->
        <div class="product-table">
        <div class="product-table-row product-table-header">
          <div class="name-col"></div>
          <div class="unit-col">Unit</div>
          <div class="qty-col">Quantity</div>
          <div class="kpi-col">{{ $props.selectedIndicatorKey }}</div>
          <div class="remove-col"></div>   
        </div>
        <!-- Products -->
        <MappedProduct
          v-for="rowId in rowIds"
          :disabled="disabled"
          :selectedIndicatorKey="$props.selectedIndicatorKey"
          :selectedLifeCycle="$props.selectedLifeCycle"
          :key="rowId"
          :rowId="rowId"
          :buildupData="buildupData"
          @update:quantity="emitQuantityUpdate"
        />
      </div>
      </div>
      

    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref, computed, watch } from 'vue'

import { getDefaultLifeCycleStages } from '@/views/shared/LifeCycle/LifeCycleDefinitons';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import type { ImpactCategoryKey } from 'lcax';

import MappedProduct from './MappedProduct.vue'

export default defineComponent({
  name: 'MappingElement',
  components: {
    MappedProduct
  },
  props: {
    mappingName: {
      type: String,
      required: true
    },
    buildupData: {
      type: Array as PropType<ColumnDefinition[]>,
      default: () => []
    },
    rowIds: {
      type: Array as PropType<number[]>
    },
    disabled: {
      type: Boolean,
      default: false
    },
    selectedIndicatorKey: {
      type: String as PropType<ImpactCategoryKey>,
      default: "gwp"
    },
    selectedLifeCycle: {
      type: Object as PropType<ColumnDefinition[]>,
      default: getDefaultLifeCycleStages()
    }
  },
  emits: ['selectMappingElement','remove', 'update:mappingName', "update:quantity", "update:products"],
  setup(props, { emit }) {

    const productMapIdCol = computed(() =>
    props.buildupData.find((c) => c.key === "productMapId")
    );

    
    function emitQuantityUpdate(payload: {productMapId: string, newQuantity: number}) {
      console.log(`mapping element emitting quantity update ${payload.productMapId} to ${payload.newQuantity}`)
    emit("update:quantity", payload );
    }
 
    function emitSelection() {
  emit('selectMappingElement', props.mappingName);
}
    
    return {
      productMapIdCol,
      emitQuantityUpdate,
      emitSelection,
    };
  }
});
</script>

<style scoped>

.mapping-name-input {
  padding: var(--spacing-sm)
}

.mapping-item {
  border: 1px solid var(--color-grey);
  border-radius: var(--rad-small);
  padding: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
  background-color: var(--color-light);
}

.products-container {
  width: 100%;
  min-width: 0; /* Important for ellipsis to work within flex/grid parents */
}
.product-table-header,
.mapped-product {
  display: flex;
  flex-direction: row;
  align-items: center;
}
.product-table-cell {
  flex: 1 1 5rem;
  padding: 0 0.5rem;
  font-size: 0.9em;
  color: #888;
  text-align: left;
}
.product-name-header {
  flex: 2 1 9rem; /* wider for name */
}

.products-container,
.product-table {
  width: 100%;
  min-width: 0;
}

.product-table {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-width: 0;
}

.product-table-row {
  display: grid;
  grid-template-columns:
    minmax(0,2.2fr)    /* name: takes at least half, grows */
    minmax(2rem,.7fr)  /* unit */
    minmax(3rem,.8fr)  /* qty */
    minmax(5.5rem,1fr) /* gwp */
    min-content;       /* remove button */
  gap: 0.5rem;
  width: 100%;
  min-width: 0;       /* for ellipsis! */
  align-items: center;
}

.product-table-header {
  color: var(--color-text-grey);
  background: none;
  margin-top: var(--spacing-tiny);
  margin-bottom: var(--spacing-tiny);
  min-height: 1.2em;
  font-size: var(--font-size-small);
  user-select: none;
}

.mapped-product {
  min-height: 2em;
}

/* Ensure cells do not overflow, especially name ellipsis */
.name-col, .unit-col, .qty-col, .kpi-col {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-name-ellipsis {
  display: inline-block;
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.remove-col {
  justify-self: end;
}

.quantity-input::-webkit-outer-spin-button,
.quantity-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.quantity-input {
  -moz-appearance: textfield;
  appearance: textfield;
}


</style>


