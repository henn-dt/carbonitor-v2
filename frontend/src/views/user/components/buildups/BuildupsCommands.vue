<!-- // frontend/src/views/user/components/buildups/BuildupsCommands.vue -->

<!-- BuildupCommands.vue -->
<template>
  <div class="collection-container cozy no-margin no-padding">
    <span 
      class="icon show" 
      @click="openEditModal()"
      title="View buildup details"
    >
      <i class="icon-view"></i>
    </span>
<!--     <span 
      class="icon edit" 
      @click="editBuildup"
      title="Edit buildup"
    >
      <i class="icon-edit"></i>
    </span> -->
<!--     <span 
      class="icon remove" 
      @click="confirmDelete"
      title="Delete buildup"
    >
      <i class="icon-delete"></i>
    </span> -->
  </div>


</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

import { getBuildupService } from '@/services/ServiceAccessor';
import { getUiModalStore , getBuildupStore} from '@/stores/storeAccessor';

import type { IBuildup } from '@/types/buildup/IBuildup';


export default defineComponent({
  name: 'BuildupCommands',  
  props: {
    rowIndex: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const buildupService = getBuildupService()
    const uiModalStore = getUiModalStore()
    const buildupStore = getBuildupStore()

    // State management
    const saving = ref(false);
    const showModal = ref(false);
    const isNewBuildup = ref(true);
    const selectedBuildupId = ref<number>(-1)

    // Open modal handler - simplified and fixed double-click issue
    const openEditModal = () => {
      const rowId = props.rowIndex;

      uiModalStore.openModal({
        name: 'buildup-detail',
        params: {
          buildupId: rowId,
          isNew: false,
          onSave: handleSaveBuildup,
          onDelete: handleDeleteBuildup,
          onClose: handleCloseBuildup
        }
      });
    };

          
    const editBuildup = () => {
        console.log('edit buildup')
    };
    
    const confirmDelete = async () => {
        console.log('delete buildup')
    };

    const handleCloseBuildup = () => {
      buildupStore.setSelectedBuildup(null)
      uiModalStore.closeModal();
    }

    const handleSaveBuildup = async (entityDTO: IBuildup) => {
      try {
        if (isNewBuildup.value) {
          // Create new buildup
          await buildupService.createBuildup(entityDTO);
        } else {
          // Update existing category
          await buildupService.updateBuildup(entityDTO.id, entityDTO);
        }

        handleCloseBuildup()
      } catch (err) {
        console.error('Error saving buildup:', err);
      }
    };
    
    const handleDeleteBuildup = async (entityID: number) => {
      try {
        await buildupService.deleteBuildup(entityID);

        handleCloseBuildup()
      } catch (err) {
        console.error('Error deleting buildup:', err);
      }
    };
    
    return {
    // state
    showModal,
    isNewBuildup,
    saving,
    selectedBuildupId,
    //methods
    openEditModal,
    editBuildup,
    confirmDelete

    };
  }
});
</script>

<style scoped>
/* Same styling as before */
</style>