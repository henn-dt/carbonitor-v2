<template>
    <dialog class="fixed inset-0 z-50 rounded-lg shadow-lg w-full max-w-md p-6 bg-white">
        <h2 class="text-xl font-bold mb-4">Confirm Delete</h2>
        <p class="mb-6">Are you sure you want to delete this user? This action cannot be undone.</p>
        <div class="flex justify-end space-x-3">
            <button 
                @click="$emit('close')" 
                class="px-4 py-2 border border-gray-300 rounded text-gray-700 hover:bg-gray-100"
            >
                Cancel
            </button>
            <button 
                @click="$emit('confirm')" 
                class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                :disabled="loading"
            >
                {{ loading ? 'Deleting...' : 'Delete' }}
            </button>
        </div>
    </dialog>
</template>
  
<script setup lang="ts">
  // Props and emits
    const props = defineProps<{
        loading: boolean;
    }>();
    const emit = defineEmits<{
        (e: 'confirm'): void;
        (e: 'close'): void;
    }>();
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