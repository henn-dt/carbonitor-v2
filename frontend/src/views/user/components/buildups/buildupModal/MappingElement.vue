<!-- MappingElement.vue -->
<template>
  <div class="form-section mapping-element">
    <div class="section-header">
      <div class="content-title">
        <!-- Editable mapping name -->
        <input 
          type="text" 
          v-model="localMappingName" 
          @blur="updateMappingName"
          class="mapping-name-input"
          :disabled="disabled"
        />
      </div>
      <button 
        class="remove-button" 
        @click="$emit('remove')" 
        :disabled="disabled"
      >×</button>
    </div>
    
    <div class="form-section">
      <div v-if="mappedProducts.length === 0" class="no-products-message">
        No products in this mapping element. Click "Add Product" to add one.
      </div>
      
      <MappedProduct
        v-for="(product, index) in mappedProducts"
        :key="product.id || index"
        :product="product"
        :disabled="disabled"
        @update:quantity="updateProductQuantity(index, $event)"
        @remove="removeProduct(index)"
      />
      
      <button 
        class="save-button"
        @click="addProduct"
        :disabled="disabled"
      >
        + Add Product
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref, computed, watch } from 'vue'
import MappedProduct from './MappedProduct.vue'
import type { IProduct } from "@/types/product/IProduct";
import type { IProductWithCalculatedImpacts } from '@/types/epdx/IProductWithCalculatedImpacts';

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
    mappedProducts: {
      type: Array as PropType<(IProduct & IProductWithCalculatedImpacts)[]>,
      default: () => []
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  emits: ['remove', 'update:mappingName', 'update:products'],
  setup(props, { emit }) {
    // Local state for editing the mapping name
    const localMappingName = ref(props.mappingName);
    
    // Update local name when prop changes
    watch(() => props.mappingName, (newName) => {
      localMappingName.value = newName;
    });
    
    // Handle updating the mapping name
    const updateMappingName = () => {
      // Only emit if name has changed and isn't empty
      if (localMappingName.value !== props.mappingName && 
          localMappingName.value.trim() !== '') {
        emit('update:mappingName', localMappingName.value);
      } else {
        // Reset to original if empty
        localMappingName.value = props.mappingName;
      }
    };
    
    // Add a new placeholder product
    const addProduct = () => {
      // Create a copy of the current products
      const updatedProducts = [...props.mappedProducts];
      
      // Emit the updated products array
      emit('update:products', updatedProducts);
    };
    
    // Update a product's quantity
    const updateProductQuantity = (index: number, quantity: number) => {
      // Create a copy of the current products
      const updatedProducts = [...props.mappedProducts];
      
      // Update the quantity for the specified product
      if (updatedProducts[index]) {
        updatedProducts[index] = {
          ...updatedProducts[index],
          quantity
        };
        
        // Emit the updated products array
        emit('update:products', updatedProducts);
      }
    };
    
    // Remove a product
    const removeProduct = (index: number) => {
      // Create a copy without the specified product
      const updatedProducts = props.mappedProducts.filter((_, i) => i !== index);
      
      // Emit the updated products array
      emit('update:products', updatedProducts);
    };
    
    return {
      localMappingName,
      updateMappingName,
      addProduct,
      updateProductQuantity,
      removeProduct
    };
  }
});
</script>