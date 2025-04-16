<template>

    <div class="modal-backdrop" @click.self="closeModal">
            <!-- Overlay to capture clicks outside the confirm delete button -->
            <div v-if="showDeleteConfirm" class="delete-overlay" @click="cancelDelete"></div>
      <div class="card modal full-screen">
        <div class="sidebar-page">
          <div class="page-content">
            <div class="card-header">
              <input 
              id="buildup-name" 
              v-model="buildupData.name"
              type="text"  
              placeholder="Name of the Buildup"
              ref="buildupNameInput"/>
              <button class="close-button" @click="closeModal">×</button>
            </div>
            <div v-if="!isNameUnique" class="validation-error">{{ validationErrors.name }}</div>
        
            <div class="card-body">
              <!-- Buildup Main Information -->
              <div class="form-section" id="buildup-header">
                <div class="section-header"  @click="toggleSection(`buildup-header`)">
                  <a>Buildup key facts</a>
                  <div class="form-group static-size">
                    <label for="unit-type" class="form-label">Unit</label>
                    <select id="unit-type" 
                      v-model="buildupData.unit" >
                      <option v-for="unit in unitTypes" :key="unit" :value="unit" class="list element label">
                        {{ unit }}
                      </option>
                    </select>
                  <span class="chevron">▼</span>
                </div>

                  <!-- Header row with name and type -->
                  <div class="flex-row">


                    
              </div>
            
                    <!-- <div class="form-group static-size">
                    <label for="buildup-type" class="form-label">Unit</label>
                    <select id="buildup-type" 
                            v-model="buildupData.unit" >

                      <option v-for="type in buildupTypes" :key="type" :value="type" class="list element label">
                        {{ type }}
                      </option>
                      <option>m2</option>
                      <option>m3</option>
                    </select>
                  </div> -->
                </div>
            
                <div class="form-group">
                  <label for="buildup-description" class="form-label">Description</label>
                  <textarea 
                    id="buildup-description" 
                    v-model="buildupData.description" 
                    placeholder="Enter description"
                    rows="3"
                  ></textarea>
                </div>
              </div>
              <!-- Products Section -->
              <BuildupProductSection 
              :combinedData="combinedBuildup"
              @update:mappedProducts="handleMappedProductsUpdate"
              :disabled="isLoading || isSaving || isDeleting"
              />
              <!-- Classification Section -->
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
                @click="saveBuildup"
                :disabled="!isFormValid || isSaving || isDeleting"
              >
                <span v-if="isSaving">Saving...</span>
                <span v-else>{{ isNewBuildup ? 'Create' : 'Save Changes' }}</span>
              </button>

              <div class="delete-button-container" v-if="!isNewBuildup">
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

          <div class="page-content">
                    <!-- Speckle Viewer -->
                    <SpeckleViewer 
                     v-if="speckleModelData" 
                    :modelData="speckleModelData" 
                    class="entity-model-viewer"
                    />  
          </div> <!-- Page Content -->
          <SelectorBar>

            <!-- Impact Indicator Selector -->
            <div class="selector-items-container">
              <ImpactIndicatorSelector 
                class="buildup-indicator-selector" 
              />
            </div>

            <!-- Lifecycle Stage Selector -->
            <div class="selector-items-container">
              <LifeCycleSelector 
              class="buildup-lifecycle-selector" 
              />
            </div>
            </SelectorBar>
        </div>  <!-- Page Container -->
      </div>  <!-- Modal Container -->
    </div>  <!-- Backdrop-->
</template>
  
<script lang="ts">
import { defineComponent, ref, computed, watch , onMounted, onBeforeUnmount, nextTick} from 'vue';

import { units } from '@/types/epdx/unitsEnum'

import { Buildup } from '@/types/buildup/Buildup';
import type { IBuildup } from '@/types/buildup/IBuildup';
import type { IBuildupWithProcessedProducts } from '@/types/epdx/IBuildupWithProcessedProducts';

import type { IProduct } from "@/types/product/IProduct";
import type { IProductWithCalculatedImpacts } from '@/types/epdx/IProductWithCalculatedImpacts';
import { getBuildupStore } from '@/stores/storeAccessor';
import { getBuildupProcessService, getBuildupService } from '@/services/ServiceAccessor';
//import components
import SelectorBar from '@/views/shared/SelectorBar/SelectorBarSidebar.vue';
import SpeckleViewer , {type SpeckleModelData }from '@/views/shared/SpeckleViewer/SpeckleViewer.vue'
import ImpactIndicatorSelector from '@/views/shared/ImpactIndicator/ImpactIndicatorSelector.vue';
import LifeCycleSelector from '@/views/shared/LifeCycle/LifeCycleSelector.vue';
import BuildupProductSection from '@/views/user/components/buildups/buildupModal/BuildupProductSection.vue'


export default defineComponent({
  name: 'BuildupModal',
  components : {
    SpeckleViewer,
    SelectorBar,
    ImpactIndicatorSelector,
    LifeCycleSelector,
    BuildupProductSection
  },
  props: {
    buildupId : {
      type: Number,
      required: true
    },
    isNew: {
      type: Boolean,
      default: true
    }
  },
  emits: ['close', 'save', 'delete'],
  setup(props, { emit }) {

    //enums
    const unitTypes = Object.values(units)

    const buildupStore = getBuildupStore();
    const buildupProcessService = getBuildupProcessService()    
    const buildupService = getBuildupService()

    // Track if we're currently performing an operation
    const isSaving = computed(() => buildupStore.loading);
    const isDeleting = ref(false);
    const showDeleteConfirm = ref(false);
    const isLoading = ref(true);

    // Validation related refs
    const validationErrors = ref({
      name: ''
    });

    // Get the buildup from store using index
    const originalBuildup = computed<IBuildup | null>(() => {
      const buildups = buildupStore.buildups;
      return buildups.length > props.buildupId ? buildups[props.buildupId] : null;
    });
    
    // Get the buildup ID
    const buildupId = computed<number | null>(() => {
      return originalBuildup.value?.id || null;
    });
    
    // Get the processed data
    const processedData = computed(() => {
      if (!buildupId.value) return null;
      return buildupStore.findProcessedDataById(buildupId.value);
    });
    
    // Combined view for display - always returns a combined structure
    const combinedBuildup = computed<IBuildup & IBuildupWithProcessedProducts>(() => {
      if (buildupId.value) {
        // For existing buildups, try to get the combined view from the service
        try {
          return buildupProcessService.getCombinedBuildup(buildupId.value);
        } catch (err) {
          console.error('Error getting combined buildup:', err);
          // Fall back to combining manually
        }
      }

      // For new buildups or if the service call failed,
      // manually combine the current buildupData with empty processed structure
      return {
        ...buildupData.value,
        mappedProducts: {},
        processedProducts: [],
        isFullyProcessed: false
      };
    });
    
    // Create a default buildup with all required properties
    const createDefaultBuildup = (): Buildup => {
      return {
        id: 0,
        name: '',
        user_id_created: 0,
        user_id_updated: 0,
        status: 'draft',
        description: '',
        comment: '',
        quantity: 0,
        unit: 'unknown',
        products: {},
        results: {},
        classification: [],
        metaData: {}
      };
    };
    
    // Create a deep copy of the buildup or create a new one with all required fields
    const buildupData = ref<IBuildup>(createDefaultBuildup());
    
    // Initialize local copy from original when it changes
    watch(originalBuildup, (newValue) => {
      if (newValue) {
        buildupData.value = new Buildup(JSON.parse(JSON.stringify(newValue)));
        isLoading.value = false;
      }
    }, { immediate: true });



    // Speckle Model Data
    const speckleModelData = computed<SpeckleModelData | null>(() => {
        if (buildupData.value == null) {
          return null
        }
        console.log('checking model url')
        console.log(buildupData.value.metaData)

      if (buildupData.value.metaData?.model_url) {
        return {
          modelUrl: buildupData.value.metaData.model_url,
          modelMapping: buildupData.value.metaData.model_mapping || undefined
        };
      }
      return null;
    });

    // Get existing buildup names
    const existingBuildupNames = computed<string[]>(() => {
      return buildupStore.buildups
        .filter(b => !originalBuildup.value || b.id !== originalBuildup.value.id) // Exclude current buildup
        .map(b => b.name);
    });
    
    // Validation
    const isNameUnique = computed(() => {
      return !existingBuildupNames.value.includes(buildupData.value.name);
    });
    
    const validateName = (value: string): boolean => {
      // Add validation logic here
      return true;
    };
    
    const isNewBuildup = computed(() => props.isNew);
    
    const isFormValid = computed(() => {
      const nameToValidate = buildupData.value.name;
      
      // Skip name validation against itself for existing buildups
      if (!isNewBuildup.value && originalBuildup.value?.name === nameToValidate) {
        return nameToValidate.trim() !== '';
      }
      
      return nameToValidate.trim() !== '' && 
             validateName(nameToValidate) &&
             isNameUnique.value;
    });
    
    const closeModal = () => {
      showDeleteConfirm.value = false;
      emit('close');
    };
    

const saveBuildup = () => {
  if (!isFormValid.value || isSaving.value) return;
  
  // Create a copy but maintain the BuildupEntityType
  const buildupToSave = { ...buildupData.value };
  emit('save', new Buildup(buildupToSave));
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
        await emit('delete', buildupData.value.id);
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
      saveBuildup();
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
  }
};

    // Load processed data if needed
    const ensureProcessedData = () => {
      if (originalBuildup.value && (!processedData.value?.isFullyProcessed)) {
        try {
          isLoading.value = true;
          buildupProcessService.processBuildup(originalBuildup.value.id);
        } catch (err) {
          console.error('Error processing buildup:', err);
        } finally {
          isLoading.value = false;
        }
      }
    };
    
    // Set up event listeners and ensure data is loaded
    onMounted(() => {
      window.addEventListener('keydown', handleKeydown);
      ensureProcessedData();
    });
    
    // Clean up event listeners
    onBeforeUnmount(() => {
      window.removeEventListener('keydown', handleKeydown);
    });

    const toggleSection = (sectionId: string) => {
      const section = document.getElementById(sectionId);
      if (section) {
        section.classList.toggle('collapsed');
      }
    };

/**
 * Handle updates to mappedProducts from the BuildupProductSection component
 * This updates both the local buildupData (products/results) and triggers reprocessing
 */
 const handleMappedProductsUpdate = async (
  newMappings: Record<string, (IProduct & IProductWithCalculatedImpacts)[]>
) => {
  // 1. Convert the mapped products back to the format expected by buildupData
  const updatedProducts: Record<string, any> = {};
  const updatedResults: Record<string, any> = {};
  
  // Track all product IDs to ensure uniqueness
  let productCounter = 1;
  
  // Process each mapping group
  Object.entries(newMappings).forEach(([mappingId, products]) => {
    // For each product in this mapping
    products.forEach((product) => {
      // Create a unique ID for this product
      const productId = `product_${productCounter++}`;
      
      // Create the product reference
      updatedProducts[productId] = {
        overrides: {
          meta_data: {
            model_mapping_element_id: mappingId
          }
        }
      };
      
      // Create the corresponding result entry
      updatedResults[productId] = {
        quantity: product.quantity || 1
      };
    });
  });
  
  // 2. Create an updated copy of buildupData
  const updatedBuildupData = { 
    ...buildupData.value,
    products: updatedProducts,
    results: updatedResults
  };
  
  // 3. Update local buildupData
  buildupData.value = updatedBuildupData;
  
  // 4. If this is an existing buildup, trigger reprocessing
  if (buildupId.value && !isNewBuildup.value) {
    try {
      isLoading.value = true;
      
      // Update the buildup in the store first
      await buildupService.updateBuildup(buildupId.value, updatedBuildupData);
      
      // Then trigger reprocessing to refresh impacts
      await buildupProcessService.processBuildup(buildupId.value);
      
      console.log('Buildup updated and reprocessed with new mappings');
    } catch (err) {
      console.error('Error updating and reprocessing buildup:', err);
    } finally {
      isLoading.value = false;
    }
  } else {
    // For new buildups, just log the change - we'll process when saving
    console.log('Updated local buildup data with new mappings');
  }
};

return {
      //enums
      unitTypes,

      // data objects
      speckleModelData,
      buildupData,
      combinedBuildup,
      processedData,

      // state manager
      isNewBuildup,
      isFormValid,
      isNameUnique,
      validationErrors,
      isSaving,
      isDeleting,
      isLoading,
      showDeleteConfirm,

      //methods
      toggleSection,
      closeModal,
      saveBuildup,
      confirmDelete,
      cancelDelete,
      executeDelete,
      handleMappedProductsUpdate

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
