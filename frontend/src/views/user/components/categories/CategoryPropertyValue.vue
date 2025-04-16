<template>
  <div class="form-group">
    <!-- STRING input -->
    <input
      v-if="format === 'STRING'"
      :value="modelValue"
      @input="updateValue($event)"
      @blur="handleBlur"
      type="text"
      :placeholder="placeholder || 'Enter string value'"
    />
    <!-- NUMBER input -->
    <input
      v-else-if="format === 'NUMBER'"
      :value="displayValue"
      @input="updateNumberValue($event)"
      @blur="handleBlur"
      type="text"
      inputmode="decimal"
      :placeholder="placeholder || 'Enter number value'"
    />
    <!-- BOOLEAN input -->
    <select
      v-else-if="format === 'BOOLEAN'"
      :value="modelValue === true ? 'true' : modelValue === false ? 'false' : ''"
      @change="updateBooleanValue($event)"
    >
      <option v-if="allowEmpty" value="" class="list element label">{{ emptyOptionLabel }}</option>
      <option value="true" class="list element label">True</option>
      <option value="false" class="list element label">False</option>
    </select>
    <!-- DATE input -->
    <input
      v-else-if="format === 'DATE'"
      :value="modelValue"
      @input="updateValue($event)"
      @blur="handleBlur"
      type="date"
      :placeholder="placeholder || 'Enter date value'"
    />
    <!-- Validation error message -->
    <div v-if="error" class="validation-error">{{ error }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch, computed, nextTick, type PropType } from 'vue';
import { CategoryPropertyFormat } from '@/types/category/CategoryPropertyFormatEnum';
import { validateCategoryPropertyValue} from '@/views/user/components/categories/CategoryPropertyValidation'

export default defineComponent({
  name: 'CategoryPropertyValue',
  props: {
    modelValue: {
      type: [String, Number, Boolean, Object, null] as PropType<string | number | boolean | null>,
      default: null
    },
    format: {
      type: String as PropType<CategoryPropertyFormat>,
      required: true
    },
    placeholder: {
      type: String,
      default: ''
    },
    allowEmpty: {
      type: Boolean,
      default: true
    },
    emptyOptionLabel: {
      type: String,
      default: 'Select a value'
    },
    validateUnique: {
      type: Boolean,
      default: false
    },
    existingValues: {
      type: Array as PropType<Array<string | number | boolean | null>>,
      default: () => []
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit, expose }) {
    const error = ref('');
    const isCurrentlyValid = ref(true);

    const displayValue = computed(() => {
      if (props.format === CategoryPropertyFormat.NUMBER && props.modelValue !== null) {
        return props.modelValue.toString();
      }
      return props.modelValue === null ? '' : props.modelValue;
    });

    // Validation from external module
    const validateValue = (value: any): boolean => {
      const result = validateCategoryPropertyValue(
        value, 
        props.format, 
        props.allowEmpty, 
        props.validateUnique, 
        props.existingValues
      );
      
      error.value = result.error;
      return result.isValid;
    };

    // Only the input value is updated here, without emitting validation
    const updateValue = (event: Event) => {
      const target = event.target as HTMLInputElement | null;
      if (!target) return;
      
      const value = target.value === '' ? null : target.value;
      validateValue(value); // Just validate internally
      
      // Only update the model value
      emit('update:modelValue', value);
    };

    const handleBlur = () => {
      // Just validate internally on blur
      validateValue(props.modelValue);
    };

    const updateNumberValue = (event: Event) => {
  const target = event.target as HTMLInputElement | null;
  if (!target) return;
  
  const originalValue = target.value;
  
  // Handle empty value
  if (originalValue === '') {
    error.value = '';
    emit('update:modelValue', null);
    return;
  }
  
  // Check if input contains only valid number characters
  // Accept digits, one decimal point, and optional minus at start
  const isValidNumberFormat = /^-?\d*\.?\d*$/.test(originalValue);
  
  if (!isValidNumberFormat) {
    // Invalid character detected - show error but don't update input yet
    error.value = 'Please enter a valid number';
    
    // IMPORTANT: Revert the input value to the last valid value
    // This is the key step that fixes the stuck input issue
    nextTick(() => {
      target.value = props.modelValue === null ? '' : String(props.modelValue);
    });
    return;
  }
  
  // Handle comma as decimal separator
  if (originalValue.includes(',')) {
    const correctedValue = originalValue.replace(',', '.');
    error.value = 'Please use a decimal point (.) instead of a comma';
    
    // Update the input field with corrected value
    nextTick(() => {
      target.value = correctedValue;
    });
    
    // Process the corrected value
    const numValue = Number(correctedValue);
    emit('update:modelValue', numValue);
    return;
  }
  
  // For valid input, convert to number and emit
  const numValue = originalValue === '-' ? originalValue : Number(originalValue);
  
  // Special case: Keep the minus sign while typing
  if (originalValue === '-') {
    // Just update the display but don't update the model yet
    error.value = '';
    return;
  }
  
  // Validate the numeric value
  const result = validateCategoryPropertyValue(
    numValue,
    props.format,
    props.allowEmpty,
    props.validateUnique,
    props.existingValues
  );
  
  error.value = result.error;
  
  if (result.isValid) {
    emit('update:modelValue', numValue);
  }
};




    // Special handler for boolean inputs
    const updateBooleanValue = (event: Event) => {
      const target = event.target as HTMLSelectElement | null;
      if (!target) return;
      
      let value: boolean | null = null;
      if (target.value === 'true') value = true;
      else if (target.value === 'false') value = false;
      
      validateValue(value);
      
      if (isCurrentlyValid.value || (target.value === '' && props.allowEmpty)) {
        emit('update:modelValue', value);
      }
    };

    // Watch for changes in format to validate current value
    watch(() => props.format, () => {
      validateValue(props.modelValue);
      
      // If invalid after format change, clear the value
      if (!isCurrentlyValid.value) {
        emit('update:modelValue', null);
      }
    });

    // Revalidate when existing values change (for uniqueness check)
    watch(() => props.existingValues, () => {
      if (props.validateUnique && props.modelValue !== null) {
        validateValue(props.modelValue);
      }
    }, { deep: true });

    // Expose methods/properties for parent component to access
    expose({
      validate: () => {
        const isValid = validateValue(props.modelValue);
        return { 
          isValid, 
          error: error.value 
        };
      },
      isValid: () => isCurrentlyValid.value,
      getError: () => error.value
    });

    return {
      error,
      updateValue,
      updateNumberValue,
      updateBooleanValue,
      validateValue,
      handleBlur,
      displayValue,
    };
  }
});
</script>
  
  <style scoped>

  
  .validation-error {
    color: var(--color-error);
    font-size: var(--font-size-small);
    margin-top: var(--spacing-tiny);
  }
  </style>