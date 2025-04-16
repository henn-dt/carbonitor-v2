<template>
    <dialog class="fixed inset-0 z-50 rounded-lg shadow-lg w-full max-w-md p-6 bg-white">
        <h2 class="text-xl font-bold mb-4">User Details</h2>
        <div v-if="loading" class="text-center py-4">
            <p>Loading user details...</p>
        </div>
        <div v-else-if="user">
            <div class="space-y-4">
                <div class="border-b pb-2">
                    <p class="text-gray-600">Username</p>
                    <p class="font-medium">{{ user.username }}</p>
                </div>
                <div class="border-b pb-2">
                    <p class="text-gray-600">Email</p>
                    <p class="font-medium">{{ user.email }}</p>
                </div>
                <div class="border-b pb-2">
                    <p class="text-gray-600">Status</p>
                    <p class="font-medium">{{ user.is_active ? 'Active' : 'Inactive' }}</p>
                </div>
                <div class="border-b pb-2">
                    <p class="text-gray-600">Email Verified</p>
                    <p class="font-medium">{{ user.is_verified ? 'Yes' : 'No' }}</p>
                </div>
                <div class="border-b pb-2">
                    <p class="text-gray-600">Auth Method</p>
                    <p class="font-medium">{{ user.auth_method || 'Standard' }}</p>
                </div>
                <div class="border-b pb-2">
                    <p class="text-gray-600">Last Login</p>
                    <p class="font-medium">{{ formatDate(user.last_login_at) }}</p>
                </div>
                <div class="border-b pb-2">
                    <p class="text-gray-600">Created</p>
                    <p class="font-medium">{{ formatDate(user.created_at) }}</p>
                </div>
                <div class="border-b pb-2">
                    <p class="text-gray-600">Last Updated</p>
                    <p class="font-medium">{{ formatDate(user.updated_at) }}</p>
                </div>
            </div>
            <div class="mt-6 text-right">
                <button 
                    @click="$emit('close')" 
                    class="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
                >
                    Close
                </button>
            </div>
        </div>
    </dialog>
</template>
  
<script setup lang="ts">
    import type { IUserDetail } from '@/types/user/IUserDetail';
    // Props and emits
    const props = defineProps<{
        user: IUserDetail | null;
        loading: boolean;
    }>();
    const emit = defineEmits<{
        (e: 'close'): void;
    }>();
    // Helper Functions
    function formatDate(dateString: string | null | undefined): string {
        if (!dateString) return 'N/A';
        return new Date(dateString).toLocaleString();
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