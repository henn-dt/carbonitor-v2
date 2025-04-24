<!-- MappedProduct.vue -->
<template>
  <div class="product-table-row mapped-product">
    <!-- NAME CELL -->
    <div class="name-col">
      <span class="product-name-ellipsis">
        {{ getValue('productName') || 'Unnamed Product' }}
      </span>
    </div>
    <!-- UNIT -->
    <div class="unit-col">
      {{ getValue('declaredUnit') }}
    </div>
    <!-- QUANTITY -->
    <div class="qty-col">
      <input
        type="number"
        class="quantity-input"
        :value="getValue('quantity').toFixed(2)"
        @input="onQuantityChange"
        placeholder="Quantity"
        min="0.001"
        step="0.001"
        :disabled="disabled"
      />
    </div>
    <!-- GWP -->
    <div class="kpi-col">
      <span>{{ getImpactSum() !== null ? getImpactSum()?.toFixed(2) : 0 }}</span>
    </div>
    <!-- REMOVE -->
    <div class="remove-col">
      <span 
        class="icon remove" 
        :disabled="disabled"
        aria-label="Remove product"
        title="Remove product"
        @click="$emit('remove')"
      ></span>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType, computed } from 'vue'

import { getDefaultLifeCycleStages } from '@/views/shared/LifeCycle/LifeCycleDefinitons';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import type { ImpactCategoryKey } from 'lcax';
import type { LifeCycleGroups } from '@/types/epdx/ICalculatedImpact';

export default defineComponent({
  name: 'MappedProduct',
  props: {
    rowId: { type: Number, required: true },
    buildupData: { type: Array as PropType<ColumnDefinition[]>, required: true },
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
  emits: ['update:quantity', 'remove'],
  setup(props, { emit }) {
    function getValue(key: string) {
    return props.buildupData
      .find(col => col.key === key)?.columnValues
      ?.find(r => r.rowId === props.rowId)?.value;
    }

    function getImpactSum() {
  if (!props.selectedIndicatorKey || !Array.isArray(props.selectedLifeCycle)) return null;
  const qty = getValue("quantity")
  const normQty = getValue("normalizedQuantity")
  const keys = props.selectedLifeCycle.map(
    lc => `${props.selectedIndicatorKey}-${lc.key}`
  );
  return keys.reduce((sum, k) => {
    const val = getValue(k) * (qty/normQty);
    return sum + (typeof val === "number" ? val : 0);
  }, 0);
}


  function onQuantityChange(event: Event) {
    const value = parseFloat((event.target as HTMLInputElement).value);
    if (!isNaN(value)) {
      console.log(`mapped product changed quantity of product id ${getValue("productMapId")} to ${value}`)
      emit("update:quantity", {productMapId : getValue("productMapId") as string, newQuantity : value});
    }
  }
  
  return { getValue, getImpactSum, onQuantityChange };
  }
});
</script>

<style scoped>
/* Grid Layout to align everything perfectly */
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
  font-weight: 600;
  color: #999;
  background: none;
  margin-bottom: 2px;
  min-height: 1.5em;
  font-size: 0.95em;
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

/* Sticky remove button: always at end, align with mapping remove */
.remove-col {
  justify-self: end;
  align-self: center;
}
.remove-button {
  border: none;
  background: none;
  color: #b33;
  font-size: 1.2em;
  cursor: pointer;
  line-height: 1;
  padding: 0 0.2em;
  font-weight: bold;
}
.remove-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>