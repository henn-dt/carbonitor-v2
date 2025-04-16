<template>
    <dialog class="fixed inset-0 z-50 rounded-lg shadow-lg w-full max-w-md p-6 bg-white">
        <h2 class="text-xl font-bold mb-4">Create New User</h2>
        <form @submit.prevent="handleSubmit">
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
                <label class="block text-gray-700 mb-1">Password</label>
                <input 
                v-model="form.password" 
                type="password" 
                class="w-full border border-gray-300 rounded px-3 py-2"
                required
                >
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
                class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                :disabled="loading"
                >
                {{ loading ? 'Creating...' : 'Create User' }}
                </button>
            </div>
        </form>
    </dialog>
</template>
  
<script setup lang="ts">
    import { ref } from 'vue';
    import type { ICreateUserRequest } from '@/types/user/ICreateUserRequest';
        const props = defineProps<{
        loading: boolean;
    }>();

    const emit = defineEmits<{
        (e: 'submit', form: ICreateUserRequest): void;
        (e: 'close'): void;
    }>();

    // Form state
    const form = ref<ICreateUserRequest>({
        username: '',
        email: '',
        password: ''
    });

    // Methods
    function handleSubmit() {
        emit('submit', { ...form.value });
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