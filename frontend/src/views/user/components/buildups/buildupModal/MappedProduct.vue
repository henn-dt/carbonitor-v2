<!-- MappedProduct.vue -->
<template>
  <div class="mapped-product">
    <div class="product-header">
      <div class="product-name">
        {{ product.epd_name || 'Unnamed Product' }}
      </div>
      
      <div class="product-unit">
        {{ product.epd_declaredUnit || 'unit' }}
      </div>
    </div>

    <div class="product-details">
      <div class="quantity-container">
        <label for="quantity">Quantity:</label>
        <input
          id="quantity"
          type="number"
          class="quantity-input"
          :value="product.quantity"
          @input="updateQuantity"
          placeholder="Quantity"
          min="0.001"
          step="0.001"
          :disabled="disabled"
        />
      </div>
      
      <div class="impact-container" v-if="hasImpacts">
        <div class="impact-label">Total GWP:</div>
        <div class="impact-value">
          {{ formattedTotalGWP }}
        </div>
      </div>
      
      <button 
        class="remove-button" 
        @click="$emit('remove')"
        :disabled="disabled"
      >×</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType, computed } from 'vue'
import type { IProduct } from '@/types/product/IProduct';
import type { IProductWithCalculatedImpacts } from '@/types/epdx/IProductWithCalculatedImpacts';

export default defineComponent({
  name: 'MappedProduct',
  props: {
    product: {
      type: Object as PropType<IProduct & IProductWithCalculatedImpacts>,
      required: true
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:quantity', 'remove'],
  setup(props, { emit }) {
    // Check if the product has calculated impacts
    const hasImpacts = computed(() => {
      return props.product.calculatedImpacts && 
             Object.keys(props.product.calculatedImpacts).length > 0;
    });
    
    // Format the GWP impact value (or any other primary impact)
    const formattedTotalGWP = computed(() => {
      if (!hasImpacts.value || !props.product.calculatedImpacts?.gwp) {
        return 'N/A';
      }
      
      // Sum up GWP impacts across life cycle stages
      const gwpImpact = props.product.calculatedImpacts.gwp;
      const totalGWP = Object.values(gwpImpact).reduce((sum, value) => sum + value, 0);
      
      // Format with 2 decimal places and the unit
      return `${totalGWP.toFixed(2)} kg CO₂ eq.`;
    });
    
    // Update the product quantity
    const updateQuantity = (event: Event) => {
      const input = event.target as HTMLInputElement;
      const newQuantity = parseFloat(input.value);
      
      if (!isNaN(newQuantity) && newQuantity > 0) {
        emit('update:quantity', newQuantity);
      }
    };
    
    return {
      hasImpacts,
      formattedTotalGWP,
      updateQuantity
    };
  }
});
</script>