<template>
    <div class="modal-backdrop" @click.self="closeModal">
            <!-- Overlay to capture clicks outside the confirm delete button -->
            <div v-if="showDeleteConfirm" class="delete-overlay" @click="cancelDelete"></div>
      <div class="card modal full-screen">
        <div class="sidebar-page">
          <div class="page-content">

            <div class="sidebar-header" id="buildup-header">
              <div class="flex-row">
                <h2 class="content-label">{{ isNewBuildup ? 'Create New Buildup' : 'Edit Buildup' }}</h2>
                <span class="icon close" @click="closeModal"></span>
              </div>
              <div class="flex-row">
                <div class="form-group cozy">
                  <label for="buildup-name" >Name</label>
                    <input 
                  class="sidebar-title"
                  id="buildup-name" 
                  v-model="buildupData.name"
                  type="text"  
                  placeholder="Name of the Buildup"
                  ref="buildupNameInput"/>
                </div>
                <div class="form-group cozy small-size">
                  <label for="unit-type" >Unit</label>
                  <select id="unit-type" 
                    v-model="buildupData.unit" >
                    <option v-for="unit in unitTypes" :key="unit" :value="unit" class="list element label">
                      {{ unit }}
                    </option>
                  </select>                  
                </div>
                <div class="form-group cozy small-size">
                  <label for="buildup-quantity" >Quantity</label>
                    <input 
                  class="quantity-input"
                  id="buildup-quantity" 
                  v-model="buildupData.quantity"
                  type="number"  
                  placeholder="Quantity of the Buildup"
                  ref="buildupQuantityInput"
                  min="0.001"
                  step="0.001"
                  />
                </div>
                <div class="form-group cozy small-size">
                  <label for="buildup-quantity" >{{ selectedIndicatorLabel }}</label>
                  <span> {{ selectedIndicatorTotalImpact.toFixed(2) }} </span>

                </div>

              </div>
              <div v-if="!isNameUnique" class="validation-error">{{ validationErrors.name }}</div>
            </div>
            
            <div class="sidebar-body">
              <div class="filter-groups-container">
              <div class="description-container">
                <label for="buildup-description">Description</label>
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
                :selectedIndicatorKey="selectedIndicatorKey"
                :selectedLifeCycle="selectedLifeCycles"
                :buildupData="productTableColumns"
                :disabled="isLoading || isSaving || isDeleting"
                @update:quantity="handleProductQuantityUpdate"
                @update:products="handleProductsUpdate"
                @selectMappingElement="onMappingElementSelected"
                />
                <!-- Classification Section -->
              </div>

            <div class="sidebar-footer">
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

          <div 

          
          class="page-content">

          <div class="flex-row">
                <div class="form-group cozy">
                  <label for="buildup-name" >Speckle model url</label>
                    <input 
                  class="sidebar-title"
                  id="model-url" 
                  v-model="modelUrl"
                  type="text"  
                  placeholder="url of the speckle model"
                  ref="speckleModelInput"/>
                </div>
          </div>
          <div class="sidebar-body">
          <!-- Speckle Viewer  Parent Modal window--> 
                    <SpeckleViewer 
                     v-if="speckleModelData" 
                    :modelData="speckleModelData" 
                    :selectedCollections="selectedMappingElement"
                    class="entity-model-viewer"
                    @update:modelSelect="onModelSelect"
                    >  
                      <template #controls="{viewer}">
                        <BuildupControlBar v-if="viewer" :viewer="viewer" />
                      </template>
                </SpeckleViewer>

                <BuildupModalGraph
                  :precalculatedTable="productTableColumns"
                  :filteredIndices="allRowIndices"
                  :selectedIndices="allRowIndices"
                  :selectedIndicator="selectedIndicatorKey"
                  @selectMappingElement="onMappingElementSelected"
                  ></BuildupModalGraph>
            </div>       
                

              
          </div> <!-- Page Content -->
          <SelectorBar>

            <!-- Impact Indicator Selector -->
            <div class="selector-items-container">
              <ImpactIndicatorSelector 
                :selected="selectedIndicators"
                :singleSelection="true"
                class="buildup-indicator-selector" 
                @columnsChanged="onMoreIndicatorsChanged"

              />
            </div>

            <!-- Lifecycle Stage Selector -->
            <div class="selector-items-container">
              <LifeCycleSelector 
              class="buildup-lifecycle-selector" 
              :singleReuse="true"
              @lifeCycleChanged="onLifeCycleChanged"
              />
            </div>
            </SelectorBar>
        </div>  <!-- Page Container -->
      </div>  <!-- Modal Container -->
    </div>  <!-- Backdrop-->
</template>
  
<script lang="ts">
import { defineComponent, ref, computed, watch , onMounted, onBeforeUnmount, nextTick} from 'vue';

//import enums
import { units } from '@/types/epdx/unitsEnum'
import { getDefaultLifeCycleStages } from '@/views/shared/LifeCycle/LifeCycleDefinitons';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import { getImpactCategoryDefinitionsByKeys } from '@/views/shared/ImpactIndicator/ImpactIndicatorDefinitions';
import type { ImpactCategoryKey } from 'lcax';
import type { LifeCycleGroups } from '@/types/epdx/ICalculatedImpact';

// import types
import { Buildup } from '@/types/buildup/Buildup';
import type { IBuildup } from '@/types/buildup/IBuildup';
import type { IBuildupWithProcessedProducts } from '@/types/epdx/IBuildupWithProcessedProducts';

// import store and services
import { getBuildupStore } from '@/stores/storeAccessor';
import { getBuildupProcessService, getBuildupService, getImpactCalculationService } from '@/services/ServiceAccessor';
import { BuildupDataService } from './BuildupDataService';


//import components
import SelectorBar from '@/views/shared/SelectorBar/SelectorBarSidebar.vue';
import SpeckleViewer , {type SpeckleModelData }from '@/views/shared/SpeckleViewer/SpeckleViewer.vue'
import ImpactIndicatorSelector from '@/views/shared/ImpactIndicator/ImpactIndicatorSelector.vue';
import LifeCycleSelector from '@/views/shared/LifeCycle/LifeCycleSelector.vue';
import BuildupProductSection from '@/views/user/components/buildups/buildupModal/BuildupProductSection.vue'
import BuildupControlBar from '@/views/user/components/buildups/speckleViewer/BuildupControlBar.vue';
import BuildupModalGraph from '@/views/user/components/buildups/buildupModal/BuildupModalGraph.vue';



export default defineComponent({
  name: 'BuildupModal',
  components : {
    SpeckleViewer,
    SelectorBar,
    ImpactIndicatorSelector,
    LifeCycleSelector,
    BuildupProductSection,
    BuildupControlBar,
    BuildupModalGraph
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
  emits: ['close', 'save', 'delete', 'onMappingElementSelected'],
  setup(props, { emit }) {

    //enums
    const unitTypes = Object.values(units)

    //stores and services
    const buildupStore = getBuildupStore();
    const buildupProcessService = getBuildupProcessService()    
    const impactCalculationService = getImpactCalculationService()

    
    // state
    // Track if we're currently performing an operation
    const isSaving = computed(() => buildupStore.loading);
    const isDeleting = ref(false);
    const showDeleteConfirm = ref(false);
    const isLoading = ref(true);

    const selectedIndicators = ref(getImpactCategoryDefinitionsByKeys(["gwp"]));
    const selectedLifeCycles = ref(getDefaultLifeCycleStages());

    const treemapGrouping = ref<'mapping' | 'product'>('mapping');
    const showLifeCycleBreakdown = ref(false);

    // Validation related refs
    const validationErrors = ref({
      name: ''
    });


    // Logic
    // Get the buildup from store using index
    const originalBuildup = computed<IBuildup | null>(() => {
      const buildups = buildupStore.buildups;
      return buildups.length > props.buildupId ? buildups[props.buildupId] : null;
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
        metaData: {"model_url": "", "model_mapping": ""}
      };
    };

    // Create a deep copy of the buildup or create a new one with all required fields
    const buildupData = ref<IBuildup>(originalBuildup.value || createDefaultBuildup());
      watch(
      buildupData,
        () => { processLocalBuildup(); },
        { deep: true }
        );

    const localProcessed = ref<IBuildupWithProcessedProducts | null>(null);

    async function processLocalBuildup() {
      isLoading.value = true
      localProcessed.value = await impactCalculationService.processSingleBuildupImpacts(buildupData.value);
      isLoading.value = false
    }

    const combinedBuildup = computed<IBuildup & IBuildupWithProcessedProducts>(() => {
      if (localProcessed.value) {
          return { ...buildupData.value,
                  ...localProcessed.value
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

    })
    const productTableColumns = computed<ColumnDefinition[]> (() => {
      const buildupDataTable = BuildupDataService.prepareProductsInBuildupTable(combinedBuildup.value, selectedIndicators.value, selectedLifeCycles.value)
      return buildupDataTable
    })

    const allRowIndices = computed(() => {
      const anyCol = productTableColumns.value.length > 0 ? productTableColumns.value[0] : undefined;
      return anyCol && anyCol.columnValues ? anyCol.columnValues.map(x => x.rowId) : [];
    })



    // Speckle Model Data
    const modelUrl = computed({
      get() {
        return buildupData.value.metaData?.model_url || '';
      },
      set(val) {
        // Create the metaData object if it doesn't exist
        if (!buildupData.value.metaData) {
          buildupData.value.metaData = {};
        }
        buildupData.value.metaData.model_url = val;
      }
    });

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
  emit('save', buildupToSave);
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


    // Set up event listeners and ensure data is loaded
    onMounted(() => {
      if (originalBuildup.value) {
        buildupData.value = new Buildup(originalBuildup.value);
      }

      window.addEventListener('keydown', handleKeydown);
      processLocalBuildup()
      isLoading.value = false
    });
    
    // Clean up event listeners
    onBeforeUnmount(() => {
      window.removeEventListener('keydown', handleKeydown);
    });


  const handleProductQuantityUpdate = (payload : {productMapId: string, newQuantity: number}) => {  
    console.log(`modal receiving quantity update  ${payload.productMapId} to ${payload.newQuantity}`)
    if (!buildupData.value.results) return
    if (buildupData.value.results[payload.productMapId]['quantity']) {
      buildupData.value.results[payload.productMapId]['quantity'] = payload.newQuantity 
    }

  }
  


  const handleProductsUpdate= () => {}

 
    
    const onMoreIndicatorsChanged = (columns: ColumnDefinition[]) => {
      selectedIndicators.value = columns;
    };
    
    const onLifeCycleChanged = (stages: ColumnDefinition[]) => {
      selectedLifeCycles.value = stages;
    };


    const selectedMappingElement = ref<string[]>([])

    function onMappingElementSelected(mappingName : string) {
      selectedMappingElement.value = [mappingName]
    }

    function onModelSelect() {}   

    const selectedIndicator = computed(() =>
      selectedIndicators.value && selectedIndicators.value.length > 0
        ? selectedIndicators.value[0]
        : { key: 'gwp', label: 'GWP total', tooltip: 'Global Warming Potential (kg CO2 eq.)' }
    );

    const selectedIndicatorLabel = computed(() => selectedIndicator.value.label );
    const selectedIndicatorKey = computed(() => selectedIndicator.value.key as ImpactCategoryKey);

    const selectedIndicatorTotalImpact = computed (() => {
      const products = combinedBuildup.value?.processedProducts || [];
      const indicator = selectedIndicatorKey.value
      const phases = selectedLifeCycles.value

      let total = 0;
      products.forEach(prod => {
        if (!prod.calculatedImpacts || !prod.calculatedImpacts[indicator]) return;
        const impacts = prod.calculatedImpacts[indicator];
        // phases is an array like ['Production', 'Operation', ...], sum values
        phases.forEach(phase => {
          const phaseKey = phase.key as LifeCycleGroups;
          if (typeof impacts[phaseKey] === 'number') {
            total += impacts[phaseKey];
          }
        });
      });
      return total;

    })

return {
      //enums
      unitTypes,

      // data objects
      speckleModelData,
      selectedMappingElement,
      modelUrl,
      productTableColumns,
      buildupData,
      combinedBuildup,
      selectedIndicatorKey,
      selectedIndicators,    //not to have to refactor the side selector
      selectedLifeCycles,
      allRowIndices,

      //indicator data for ease of use
      selectedIndicatorLabel,
      selectedIndicatorTotalImpact,

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
      closeModal,
      saveBuildup,
      confirmDelete,
      cancelDelete,
      executeDelete,

      // state handlers methods
      onMoreIndicatorsChanged,
      onLifeCycleChanged,
      handleProductQuantityUpdate,
      handleProductsUpdate,

      //selection handlers methods
      onMappingElementSelected,
      onModelSelect

    };
  }
});
  </script>
  
  <style scoped>

.small-size {
  max-width: 3.5rem;
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

.page-content {
  display: flex;
  flex-direction: column;
  height: 100vh;   /* or 100% if parent has fixed height */
  width: 100%;
  box-sizing: border-box;
}

.mapping-item {
  border: 1px solid var(--color-grey);
  border-radius: var(--rad-small);
  padding: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
  background-color: var(--color-light);
}

  .validation-error {
    color: var(--color-error);
    font-size: var(--font-size-small);
    margin-top: var(--spacing-tiny);
  }

  .sidebar-header,
.sidebar-body,
.sidebar-footer {
  width: 100%;
  box-sizing: border-box;
  padding: var(--spacing-sm);
}

.sidebar-header {
  flex: 0 0 auto;          /* Sticks to top */
}

.sidebar-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
  flex: 0 0 auto;    
  margin-bottom: var(--spacing-sm);
  margin-top: var(--spacing-sm)      /* Sticks to bottom */
}

.sidebar-body {
  flex: 1 1 0;             /* Take up all available vertical space */
  min-height: 0;           /* Needed for scrollbars to work in flexbox children */
  overflow-y: auto;        /* Scroll vertically if content overflows */
  gap: var(--spacing-sm);
  display: flex;
  flex-direction: column;

  /* Optional: overflow-x: hidden; */
}
  </style>
