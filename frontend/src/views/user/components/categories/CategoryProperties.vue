<template>
    <div class="form-section">
      <h2>Properties</h2>
      
      <div v-if="propertyList.length === 0" class="empty-value">
        No properties defined yet.
      </div>
      
      <div v-else>
        <CategoryPropertyItem
    v-for="(property, index) in propertyList"
    :key="property.id"
    :property="property"
    @update:property="(updatedProperty) => updateProperty(index, updatedProperty)"
    @remove="removeProperty(index)"
  />
      </div>
      
      <div v-if="showAddProperty">
            <!-- Simplified new property form -->
            <CategoryPropertyItem
              :property="newProperty"
              :is-new="true"
              @update:property="newProperty = $event"
  />
  <div class="form-footer">
    <button @click="saveNewProperty" class="save-button">Add Property</button>
    <button @click="cancelAddProperty" class="cancel-button">Cancel</button>
  </div>
      </div>
      
      <button 
        v-if="!showAddProperty" 
        @click="initializeAddProperty" 
        class="save-button"
      >
        + Add Property
      </button>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, computed, type PropType, watch } from 'vue';
  import { CategoryProperty } from '@/types/category/CategoryProperty';
  import { CategoryPropertyFormat } from '@/types/category/CategoryPropertyFormatEnum';
  import CategoryPropertyItem from './CategoryPropertyItem.vue';
  
  export default defineComponent({
    name: 'CategoryProperties',
    components: {
      CategoryPropertyItem
    },
    props: {
      properties: {
        type: Array as PropType<CategoryProperty[]>,
        default: () => []
      }
    },
    emits: ['update:properties'],
    setup(props, { emit }) {
      const propertyList = ref<CategoryProperty[]>([...props.properties]);
      const showAddProperty = ref(false);
      const newProperty = ref(new CategoryProperty({
        id: crypto.randomUUID(),
        name: '',
        format: CategoryPropertyFormat.STRING,
        required: false
      }));
      
      // Update the parent when our properties change
      watch(propertyList, (newValue) => {
        emit('update:properties', newValue);
      }, { deep: true });
      
      // Update our local copy when props change
      watch(
          () => props.properties,
          (newProps) => {
            // Only update if there's an actual difference
            if (JSON.stringify(propertyList.value) !== JSON.stringify(newProps)) {
              propertyList.value = [...newProps];
            }
          },
          { immediate: true }
        );
      
      const updateProperty = (index: number, updatedProperty: CategoryProperty) => {
        const updatedList = [...propertyList.value];
        updatedList[index] = updatedProperty;
        propertyList.value = updatedList;
      };
      
      const removeProperty = (index: number) => {
        const updatedList = [...propertyList.value];
        updatedList.splice(index, 1);
        propertyList.value = updatedList;
      };
      
      const initializeAddProperty = () => {
        newProperty.value = new CategoryProperty({
          id: crypto.randomUUID(),
          name: '',
          format: CategoryPropertyFormat.STRING,
          required: false
        });
        showAddProperty.value = true;
      };
      
      const saveNewProperty = () => {
        if (newProperty.value.name.trim()) {
            // Create a new array to ensure reactivity
            const updatedList = [...propertyList.value, new CategoryProperty(newProperty.value)];
            propertyList.value = updatedList;
            emit('update:properties', updatedList);
            showAddProperty.value = false;
        }
      };
      
      const cancelAddProperty = () => {
        showAddProperty.value = false;
      };
      
      return {
        propertyList,
        showAddProperty,
        newProperty,
        updateProperty,
        removeProperty,
        initializeAddProperty,
        saveNewProperty,
        cancelAddProperty
      };
    }
  });
  </script>
  
  <style scoped>



  </style>