<template>

    <div class="modal-backdrop" @click.self="closeModal">
            <!-- Overlay to capture clicks outside the confirm delete button -->
            <div v-if="showDeleteConfirm" class="delete-overlay" @click="cancelDelete"></div>
      <div class="card modal">
        <div class="card-header">
          <h2 class="title">{{ isNewCategory ? 'Create New Category' : 'Edit Category' }}</h2>
          <button class="close-button" @click="closeModal">×</button>
        </div>
        
        <div class="card-body">
          <!-- Category Main Information -->
          <div class="form-section">

            <!-- Header row with name and type -->
             <div class="flex-row">
            <div class="form-group">
              <label  for="category-name" class="form-label">Category Name</label>
              <input 
                id="category-name" 
                v-model="categoryData.name" 
                type="text" 
                placeholder="Enter category name" 
                ref="categoryNameInput"
              />
              <div v-if="!isNameUnique" class="validation-error">{{ validationErrors.name }}</div>
            </div>
            
            <div class="form-group static-size">
              <label for="category-type" class="form-label">Type</label>
              <select id="category-type" 
                      v-model="categoryData.type" >

                <option v-for="type in categoryTypes" :key="type" :value="type" class="list element label">
                  {{ type }}
                </option>
              </select>
            </div>
          </div>
            
            <div class="form-group">
              <label for="category-description" class="form-label">Description</label>
              <textarea 
                id="category-description" 
                v-model="categoryData.description" 
                placeholder="Enter description"
                rows="3"
              ></textarea>
            </div>
          </div>
          
          <!-- Properties Section -->
          <CategoryProperties 
          v-model:properties="categoryData.properties" 
          class="form-section"
          >
          </CategoryProperties>
        </div>


        <div class="card-footer">
          <button 
            class="cancel-button" 
              @click="closeModal"
              :disabled="isSaving || isDeleting"
          >
            Cancel
          </button>
          <button 
            class="save-button" 
            @click="saveCategory"
            :disabled="!isFormValid || isSaving || isDeleting"

          >
          <span v-if="isSaving">Saving...</span>
          <span v-else>{{ isNewCategory ? 'Create' : 'Save Changes' }}</span>
          </button>

          <div class="delete-button-container" v-if="!isNewCategory">
          <!-- Normal delete button when not in confirmation mode -->
          <button
            v-if="!showDeleteConfirm"
            class="delete-button"
            @click="confirmDelete"
            :disabled="isSaving || isDeleting"
          >
            Delete
          </button>
          
          <!-- Confirmation button when in confirmation mode -->
          <button
            v-else
            class="delete-confirm-button"
            @click="executeDelete"
            :disabled="isDeleting"
          >
            <span v-if="isDeleting">Deleting...</span>
            <span v-else>Confirm Delete</span>
          </button>
        </div>

        </div>
      </div>
    </div>

  </template>
  
  <script lang="ts">
import { defineComponent, ref, computed, watch , onMounted, onBeforeUnmount, nextTick} from 'vue';
import { Category } from '@/types/category/Category';
import { CategoryEntityType } from '@/types/category/CategoryEntityTypeEnum';
import type { ICategory } from '@/types/category/ICategory';
import CategoryProperties from '@/views/user//components/categories/CategoryProperties.vue';
import CategoryPropertyItem from '@/views/user//components/categories/CategoryPropertyItem.vue';
import type { CategoryProperty } from '@/types/category/CategoryProperty';
import { getCategoryStore } from '@/stores/storeAccessor';
import { CategoryPropertyFormat } from '@/types/category/CategoryPropertyFormatEnum';
import { validateCategoryPropertyValue} from '@/views/user/components/categories/CategoryPropertyValidation'

export default defineComponent({
  name: 'CategoryModal',
  components : {
    CategoryProperties,
    CategoryPropertyItem,
  },
  props: {
     data: {
      type: Object as () => ICategory | null,
      default: null
    },
    isNew: {
      type: Boolean,
      default: true
    },
    sectionType: {
      type: String as () => CategoryEntityType,
      default: CategoryEntityType.Other
    },
    existingCategories: {
    type: Array,
    default: () => []
    }
  },
  emits: ['close', 'save', 'delete'],
  setup(props, { emit }) {

    

    const categoryStore = getCategoryStore();
    
    // Track if we're currently performing an operation
    const isSaving = computed(() => categoryStore.getLoading);
    const isDeleting = ref(false);
    const showDeleteConfirm = ref(false);

    // Validation related refs
    const validationErrors = ref({
      name: ''
    });
    const categoryNameInput = ref<HTMLInputElement | null>(null);


    
    // Create a deep copy of the category or create a new one
    // Create a default category with all required properties
    const createDefaultCategory = (): Category => {
      return {
        id: 0,
        name: '',
        type: props.sectionType,
        user_id_created: 0,
        user_id_updated: 0,
        status: 'draft',
        description: '',
        properties: []
      };
    };
    
    // Create a deep copy of the category or create a new one with all required fields
    const categoryData = ref(new Category(props.data || createDefaultCategory()));
    
    // Watch for changes to props.category to update our local state
    watch(() => props.data, (newCategory) => {
      if (newCategory) {
        categoryData.value = new Category(newCategory);
      }
    });


  
    const existingCategoryNamesOfType = computed<string[]>(() => {
      // Filter categories by the current sectionType, then extract their names
      return props.existingCategories
      .filter((category: any) => category.type === categoryData.value.type)
      .map((category: any) => category.name);
      });

    const isNameUnique = ref(true)

    // Validation from external module
    const validateName = (value: any): boolean => {
      const result = validateCategoryPropertyValue(
        value, 
        CategoryPropertyFormat.STRING, 
        false, 
        true, 
        existingCategoryNamesOfType.value
      );
      
      validationErrors.value.name = result.error;
      if (validationErrors.value?.name == 'This value already exists') {
        isNameUnique.value = false
      }
      else {
        isNameUnique.value = true
      }
      return result.isValid;
    };

    const updateProperties = (newProperties: CategoryProperty[]) => {
      // Create a new reference to ensure reactivity
      categoryData.value = {
        ...categoryData.value,
        properties: [...newProperties]
      };
    };

    
    const isNewCategory = computed(() => props.isNew);
    
    const categoryTypes = Object.values(CategoryEntityType);
    
    const isFormValid = computed(() => {
      const nameToValidate = categoryData.value.name;

      let nameValidation = true;
      //skip name validation against itself
      if (!props.isNew && props.data?.name === nameToValidate) {
        
      }
      else{
        nameValidation = validateName(nameToValidate)
      }
      
      return nameToValidate.trim() !== '' && 
             categoryData.value.type !== undefined &&
             categoryData.value.type !== null &&
             nameValidation;
    });
    
    const closeModal = () => {
      showDeleteConfirm.value = false;
      emit('close');
    };
    

const saveCategory = () => {
  if (!isFormValid.value || isSaving.value) return;
  
  // Create a copy but maintain the CategoryEntityType
  const categoryToSave = { ...categoryData.value };
  emit('save', new Category(categoryToSave));
};
    
// delete workflow with confirm and state update
const confirmDelete = () => {
      showDeleteConfirm.value = true;
    };
    
const cancelDelete = () => {
      showDeleteConfirm.value = false;
    };
    
const executeDelete = async () => {
      if (isSaving.value || isDeleting.value) return;
      
      try {
        isDeleting.value = true;
        await emit('delete', categoryData.value.id);
        showDeleteConfirm.value = false;
        closeModal();
      } catch (error) {
        console.error('Error during deletion:', error);
      } finally {
        isDeleting.value = false;
      }
    };

// Keyboard event handler
const handleKeydown = (event: KeyboardEvent) => {
  switch (event.key) {
    case 'Enter':
    event.preventDefault();
    if (showDeleteConfirm.value){
        executeDelete();
      }
    else{
      saveCategory();
      }    
      break;
    case 'Escape':
    event.preventDefault();
      if (showDeleteConfirm.value){        
        cancelDelete();      
      }
      else{      
      closeModal();
    }
      break;
    case 'Delete':
    event.preventDefault();
      if (!showDeleteConfirm.value){
        confirmDelete();       
      }
      break;
  }
};

// Set up event listeners
onMounted(() => {
  window.addEventListener('keydown', handleKeydown);
});

// Clean up event listeners
onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown);
});

return {
      categoryData,
      isNewCategory,
      categoryTypes,
      isFormValid,
      isNameUnique,
      validationErrors,
      isSaving,
      isDeleting,
      showDeleteConfirm,
      closeModal,
      saveCategory,
      updateProperties,
      confirmDelete,
      cancelDelete,
      executeDelete
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
