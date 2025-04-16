<!-- BuildupProductsSection.vue -->
<template>
  <div class="products-section form-section">
    <div class="section-header">
      <h2>Composition</h2>
      <button class="save-button" @click="addMappingElement">
        + Add Mapping Element
      </button>
    </div>

    <div class="form-group">
      <div v-if="!hasMappings" class="no-mappings-message">
        No mapping elements found. Click "Add Mapping Element" to create one.
      </div>
      
      <MappingElement
        v-for="(products, mappingName) in mappedProducts"
        :mappingName="mappingName"
        :mappedProducts="products"
        @remove="removeMappingElement(mappingName)"
        @update:products="updateMappingProducts(mappingName, $event)"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType, computed, watch } from 'vue'
import MappingElement from '@/views/user/components/buildups/buildupModal/MappingElement.vue'
import type { IProduct } from "@/types/product/IProduct";
import type { IProductWithCalculatedImpacts } from '@/types/epdx/IProductWithCalculatedImpacts';
import type { IBuildup } from '@/types/buildup/IBuildup';
import type { IBuildupWithProcessedProducts } from '@/types/epdx/IBuildupWithProcessedProducts';

export default defineComponent({
  components: { MappingElement },
  props: {
    combinedData: {
      type: Object as PropType<IBuildup & IBuildupWithProcessedProducts>,
      required: true
    }
  },
  emits: ['update:mappedProducts'],
  setup(props, { emit }) {
    // Directly access the mappedProducts from combinedData
    const mappedProducts = computed(() => {
      return props.combinedData.mappedProducts || {};
    });
    
    // Check if there are any mappings
    const hasMappings = computed(() => {
      return Object.keys(mappedProducts.value).length > 0;
    });
    
    // Add a new mapping element
    const addMappingElement = () => {
      // Create a new mapping with a default name
      const newName = `New Element ${Object.keys(mappedProducts.value).length + 1}`;
      
      // Create a copy of the current mappings
      const updatedMappings = { 
        ...mappedProducts.value,
        [newName]: [] 
      };
      
      // Update the parent
      updateMappings(updatedMappings);
    };
    
    // Remove a mapping element
    const removeMappingElement = (mappingName: string) => {
      // Create a copy of current mappings
      const updatedMappings = { ...mappedProducts.value };
      
      // Remove the specified mapping
      delete updatedMappings[mappingName];
      
      // Update the parent
      updateMappings(updatedMappings);
    };
    
    // Update products for a specific mapping
    const updateMappingProducts = (
      mappingName: string, 
      products: (IProduct & IProductWithCalculatedImpacts)[]
    ) => {
      // Create a copy of current mappings
      const updatedMappings = { 
        ...mappedProducts.value,
        [mappingName]: products 
      };
      
      // Update the parent
      updateMappings(updatedMappings);
    };
    
    // Helper to emit updates to parent
    const updateMappings = (newMappings: Record<string, (IProduct & IProductWithCalculatedImpacts)[]>) => {
      emit('update:mappedProducts', newMappings);
    };
    
    // Watch for changes to combinedData for debugging
    watch(() => props.combinedData, (newValue) => {
      console.log('Combined data updated in ProductSection:', newValue);
    }, { deep: true });
    
    return { 
      mappedProducts, 
      hasMappings,
      addMappingElement, 
      removeMappingElement,
      updateMappingProducts
    };
  }
});
</script>

<style scoped>
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