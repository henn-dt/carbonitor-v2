<!-- frontend/src/views/shared/Modals/Modals.vue -->
<template>
    <BuildupModal
      v-if="modal?.name === 'buildup-detail'"
      :buildupId="modal.params.buildupId"
      :isNew="modal.params.isNew"
      @close="modal.params.onClose"
      @save="modal.params.onSave"
      @delete="modal.params.onDelete"
    />

    <!-- etc... -->
  </template>

<script setup lang="ts">
import { computed} from 'vue';
import { getUiModalStore } from "@/stores/storeAccessor";
import BuildupModal from '@/views/user/components/buildups/BuildupModal.vue';
import CategoryModal from '@/views/user/components/categories/CategoryModal.vue';


const modalStore = getUiModalStore();
const modal = computed(() => modalStore.activeModal); // or modalStore.modals for stack
</script>