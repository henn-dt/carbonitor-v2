<template>
    <dialog class="fixed inset-0 z-50 rounded-lg shadow-lg w-full max-w-md p-6 bg-white">
      <h2 class="text-xl font-bold mb-4">Edit User</h2>
      <div v-if="loading" class="text-center py-4">
        <p>Loading user details...</p>
      </div>
      <form v-else @submit.prevent="handleSubmit">
        <div class="mb-4">
          <label class="block text-gray-700 mb-1">Username</label>
          <input 
            v-model="form.username" 
            type="text" 
            class="w-full border border-gray-300 rounded px-3 py-2"
            required
          >
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 mb-1">Email</label>
          <input 
            v-model="form.email" 
            type="email" 
            class="w-full border border-gray-300 rounded px-3 py-2"
            required
          >
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 mb-1">Status</label>
          <div class="flex items-center space-x-2">
            <input 
              v-model="form.is_active" 
              type="checkbox" 
              id="status-toggle"
              class="h-4 w-4"
            >
            <label for="status-toggle" class="text-gray-700">
              {{ form.is_active ? 'Active' : 'Inactive' }}
            </label>
          </div>
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 mb-1">Email Verified</label>
          <div class="flex items-center space-x-2">
            <input 
              v-model="form.is_verified" 
              type="checkbox" 
              id="verified-toggle"
              class="h-4 w-4"
            >
            <label for="verified-toggle" class="text-gray-700">
              {{ form.is_verified ? 'Verified' : 'Not Verified' }}
            </label>
          </div>
        </div>
  
        <div class="flex justify-end space-x-3 mt-6">
          <button 
            type="button" 
            @click="$emit('close')" 
            class="px-4 py-2 border border-gray-300 rounded text-gray-700 hover:bg-gray-100"
          >
            Cancel
          </button>
          <button 
            type="submit" 
            class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            :disabled="submitting"
          >
            {{ submitting ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </form>
    </dialog>
  </template>
  
<script setup lang="ts">
    import { ref, watch } from 'vue';
    import type { IUpdateUserRequest } from '@/types/user/IUpdateUserRequest';
    import type { IUpdateUserSystemRequest } from '@/types/user/IUpdateUserSystemRequest';

    // Define the combined form type
    interface EditUserForm extends IUpdateUserRequest, IUpdateUserSystemRequest {
        username: string;
        email: string;
        is_active: boolean;
        is_verified: boolean;
    }

    // Props and emits
    const props = defineProps<{
        userData: EditUserForm;
        loading: boolean;
        submitting: boolean;
    }>();

    const emit = defineEmits<{
        (e: 'submit', userUpdate: IUpdateUserRequest, systemUpdate: IUpdateUserSystemRequest): void;
        (e: 'close'): void;
    }>();

    // Form state 
    const form = ref<EditUserForm>({
        username: '',
        email: '',
        is_active: true,
        is_verified: false
    });

    // Watch for changes to the userData prop
    watch(() => props.userData, (newValue) => {
        if (newValue) {
            form.value = { ...newValue };
        }
    }, { immediate: true });

    // Methods
    function handleSubmit() {
        // Split the form into user and system updates
        const userUpdate: IUpdateUserRequest = {
            username: form.value.username,
            email: form.value.email
        };
        const systemUpdate: IUpdateUserSystemRequest = {
            is_active: form.value.is_active,
            is_verified: form.value.is_verified
        };
        emit('submit', userUpdate, systemUpdate);
    }
</script>
  
<style scoped>
    dialog {
        border: none;
        display: block;
    }

    dialog::backdrop {
        background-color: rgba(0, 0, 0, 0.5);
    }
</style>