<template>
    <div class="property-item">
      <!-- Header row with name and type -->
      <div class="flex-row">
          <div class="form-group">
            <input 
              ref = "propertyNameInput"
              v-model="propertyData.name" 
              type="text" 
              placeholder="Property name" 
            />
          </div>
          <div class="form-group static-size">
            <select v-model="propertyData.format" >
              <option v-for="format in propertyFormats" :key="format" :value="format">
                {{ format }}
              </option>
            </select>
          </div>
          <label class="form-checkbox">
            <input 
              id="required-checkbox" 
              v-model="propertyData.required" 
              type="checkbox"
              />
            <label for="required-checkbox" class="form-label">Required</label>
          </label>
          <button @click="$emit('remove')" class="remove-button" title="Remove property">×</button>
      </div>

      
      <div class="form-group">
        <input 
          v-model="propertyData.description" 
          type="text" 
          placeholder="Add description" 
          title="Property description"
          class="description"
        />
      </div>
      

      <div class="flex-row">

      
      <div class="form-group">
        <label class="form-label">Allowed values:</label>
        <div class="collection-container no-margin no-padding">
          <div class="clickable" v-for="(value, index) in propertyData.enum" :key="index">
            {{ value }}
            <button @click="removeAllowedValue(index)" class="remove-button">×</button>
          </div>
          
          <div v-if="showAddValue" class="form-group">
            <CategoryPropertyValue
              v-model="newAllowedValue"
              :format="propertyData.format"
              placeholder="Add value"
              :allow-empty="false"
              :validate-unique="true"
              :existing-values="propertyData.enum || []"
              ref="newValueInput"
          />
          <div class="form-footer">
            <button 
              @click="addAllowedValue" 
              class="save-button"
              :disabled="!enumValidation.isValid"
            >
              Add
            </button>
            <button @click="cancelAddValue" class="cancel-button">Cancel</button>
          </div>
        </div>
          
          <button v-else @click="showAddValue = true" class="save-button">Add</button>
        </div>
      </div>
      <div class="form-group static-size default-value">

<label class="form-label">Default value:</label>
<div v-if="editingDefault" class="form-group">
  <CategoryPropertyValue
    v-model="tempDefaultValue"
    :format="propertyData.format"
    placeholder="Default value"
    :allow-empty="true"
    :validate-unique="false"
    ref="defaultValueInput"
  />
  <div class="form-footer">
    <button 
    @click="setDefaultValue" 
    class="save-button"
    :disabled="!defaultValidation.isValid"
  >
    Set
    </button>
    <button @click="cancelEditDefault" class="cancel-button">Cancel</button>
  </div>
</div>
<div 
v-else 
class="default-value-display" 
:class="{'has-value': propertyData.default !== null && propertyData.default !== '' && propertyData.default !== undefined}"
@click="startEditDefault"
>
  <span class="clickable" v-if="propertyData.default !== null && propertyData.default !== '' && propertyData.default !== undefined">
    {{ propertyData.default }}
    <button class="remove-button" @click.stop="removeDefaultValue">×</button>
  </span>
  <span v-else class="empty-value clickable">No default value</span>
</div>


</div>
    </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted, computed, type PropType, nextTick, watch } from 'vue';
  import { CategoryProperty } from '@/types/category/CategoryProperty';
  import { CategoryPropertyFormat } from '@/types/category/CategoryPropertyFormatEnum';
  import  CategoryPropertyValue  from './CategoryPropertyValue.vue';
  import { validateCategoryPropertyValue} from '@/views/user/components/categories/CategoryPropertyValidation'
  
  export default defineComponent({
    name: 'CategoryPropertyItem',
    components: {
        CategoryPropertyValue
    },
    props: {
      property: {
        type: Object as PropType<CategoryProperty>,
        required: true
      },
      isNew: {
        type: Boolean,
        default: false
      }
    },
    emits: ['update:property', 'remove'],
    setup(props, { emit }) {
    const propertyData = ref({...props.property});
    const propertyNameInput = ref<HTMLInputElement | null>(null);

    const propertyFormats = Object.values(CategoryPropertyFormat);
    const showAddValue = ref(false);
    const newAllowedValue = ref<string | number | boolean | null>(null);
    const newValueInput = ref<InstanceType<typeof CategoryPropertyValue> | null>(null);

    const editingDefault = ref(false);
    const tempDefaultValue = ref<string | number | boolean | null>(null);
    const defaultValueInput = ref<InstanceType<typeof CategoryPropertyValue> | null>(null);
    
    // Validation states
    const defaultValidation = ref({ isValid: true, error: '' });
    const enumValidation = ref({ isValid: true, error: '' });

    // Watch for format changes to clear default and enum values
    watch(() => propertyData.value.format, (newFormat, oldFormat) => {
      if (newFormat !== oldFormat) {
        propertyData.value.default = null;
        propertyData.value.enum = [];
        newAllowedValue.value = null;
      }
    });
    // Watch propertyData changes and emit updates
    watch(propertyData, (newVal) => {
      emit('update:property', new CategoryProperty(newVal));
    }, { deep: true });

/*     // Watch for prop changes
    watch(() => props.property, (newVal) => {
      propertyData.value = {...newVal};
    }, { deep: true }); */
      
    // check validation before saving
    const validateBeforeSave = () => {
    // If default value is invalid, clear it
    if (!defaultValidation.value.isValid && propertyData.value.default !== null) {
    propertyData.value.default = null;
    }
  
    emit('update:property', new CategoryProperty(propertyData.value));
    };


// Start editing default value
const startEditDefault = () => {
  tempDefaultValue.value = propertyData.value.default;
  editingDefault.value = true;
  nextTick(() => {
    defaultValueInput.value?.$el.querySelector('input,select')?.focus();
  });
};

// Set the default value
const setDefaultValue = () => {
  if (defaultValidation.value.isValid) {
    propertyData.value.default = tempDefaultValue.value;
    editingDefault.value = false;
  }
};

// Cancel editing default value
const cancelEditDefault = () => {
  editingDefault.value = false;
  tempDefaultValue.value = null;
};

const removeDefaultValue = (event: { stopPropagation: () => void; }) => {
  event.stopPropagation(); // Prevent triggering edit mode
  propertyData.value.default = null;
};
      
const addAllowedValue = () => {
      // Validate directly using the utility
      const validationResult = validateCategoryPropertyValue(
        newAllowedValue.value, 
        propertyData.value.format, 
        false, // allowEmpty
        true,  // validateUnique
        propertyData.value.enum || []
      );
      
      if (validationResult.isValid && newAllowedValue.value !== null && newAllowedValue.value !== '') {
        // Add the value to the enum array
        const updatedEnum = [...(propertyData.value.enum || []), newAllowedValue.value];
        propertyData.value.enum = updatedEnum;
        
        // Reset state
        newAllowedValue.value = null;
        showAddValue.value = false;
      }
    };
      
    // Cancel adding a new value
    const cancelAddValue = () => {
      showAddValue.value = false;
      newAllowedValue.value = null;
    };
      
/*     old method for immutability pattern, but doesn´t follow with current logic of prop mutations
// Remove an allowed value by index
    const removeAllowedValue = (index: number) => {
      const updatedEnum = [...(propertyData.value.enum || [])];
      updatedEnum.splice(index, 1);
      const updatedProperty = new CategoryProperty({
        ...propertyData.value,
        enum: updatedEnum
      });
      emit('update:property', updatedProperty);
    }; */

    // Remove an allowed value by index
const removeAllowedValue = (index: number) => {
  const updatedEnum = [...(propertyData.value.enum || [])];
  updatedEnum.splice(index, 1);
  
  // Update the local propertyData ref first
  propertyData.value.enum = updatedEnum;
  
  // Then emit the update event (this is already handled by the watch on propertyData)
  // The watch will emit: emit('update:property', new CategoryProperty(newVal));
};
      
    // Focus the input when the add value form appears
    watch(showAddValue, (newVal) => {
      if (newVal) {
        nextTick(() => {
          // Access the underlying input element if needed
          newValueInput.value?.$el.querySelector('input,select')?.focus();
        });
      }
    });

    onMounted(() => {
      propertyNameInput.value?.focus();
    });
      
      return {
        
        propertyData,
        propertyFormats,

        // default value 
        defaultValidation,
        editingDefault,
        tempDefaultValue,
        defaultValueInput,
        startEditDefault,
        setDefaultValue,
        cancelEditDefault,
        removeDefaultValue,
        //enum value list
        showAddValue,
        newAllowedValue,
        newValueInput,
        addAllowedValue,
        cancelAddValue,
        removeAllowedValue,
        //validation
        validateBeforeSave,
        enumValidation,

      };
    }
  });
  </script>
  
  <style scoped>
  .property-item {
    border: 1px solid var(--color-grey);
    border-radius: var(--rad-small);
    padding: var(--spacing-cozy);
    margin-bottom: var(--spacing-md);
    background-color: var(--color-light);
  }

  .default-value {
    min-width: 8rem; 
  }

  </style>