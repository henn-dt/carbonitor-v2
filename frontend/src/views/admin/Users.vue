<template>
    <div class="users-page p-4">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">User Management</h1>
        <button 
          @click="openCreateUserModal" 
          class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Add New User
        </button>
      </div>
  
      <!-- Loading and error states -->
      <div v-if="loading" class="text-center py-8">
        <p>Loading users...</p>
      </div>
  
      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        <p>{{ error }}</p>
      </div>
  
      <!-- Users Table -->
      <div v-else-if="users.length > 0" class="overflow-x-auto">
        <table class="min-w-full bg-white border border-gray-200">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-2 text-left">#</th>
              <th class="px-4 py-2 text-left">Username</th>
              <th class="px-4 py-2 text-left">Email</th>
              <th class="px-4 py-2 text-left">Status</th>
              <th class="px-4 py-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id" class="border-t border-gray-200 hover:bg-gray-50">
              <td class="px-4 py-2">{{ user.id }}</td>
              <td class="px-4 py-2 font-medium">{{ user.username }}</td>
              <td class="px-4 py-2">{{ user.email }}</td>
              <td class="px-4 py-2">
                <span v-if="userDetails[user.id]?.is_active" class="inline-block px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">
                  Active
                </span>
                <span v-else class="inline-block px-2 py-1 text-xs rounded-full bg-red-100 text-red-800">
                  Inactive
                </span>
              </td>
              <td class="px-4 py-2">
                <div class="flex space-x-2">
                  <button @click="viewUserDetails(user.id)" class="text-blue-600 hover:text-blue-800">View</button>
                  <button @click="openEditUserModal(user.id)" class="text-green-600 hover:text-green-800">Edit</button>
                  <button @click="confirmDelete(user.id)" class="text-red-600 hover:text-red-800">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <div v-else class="text-center py-8 bg-gray-50 rounded">
        <p class="text-gray-600">No users found. Add a new user to get started.</p>
      </div>
  
      <!-- Modals -->
      <CreateUserModal
        v-if="showCreateModal"
        :loading="createLoading"
        @submit="createUser"
        @close="showCreateModal = false"
      />
  
      <EditUserModal
        v-if="showEditModal"
        :user-data="editForm"
        :loading="editLoading"
        :submitting="updateLoading"
        @submit="updateUser"
        @close="showEditModal = false"
      />
  
      <UserDetailsModal
        v-if="showDetailsModal"
        :user="selectedUserDetail"
        :loading="detailsLoading"
        @close="showDetailsModal = false"
      />
  
      <DeleteUserModal
        v-if="showDeleteModal"
        :loading="deleteLoading"
        @confirm="deleteUser"
        @close="showDeleteModal = false"
      />
    </div>
  </template>
  
<script setup lang="ts">
    import { ref, onMounted, computed } from 'vue';
    import { useUsersStore } from '@/stores/usersStore';
    import { container } from '@/di/container';
    import { TYPES } from '@/di/types';
    import type { IUserService } from '@/services/IUserService';
    import type { IUser } from '@/types/user/IUser';
    import type { IUserDetail } from '@/types/user/IUserDetail';
    import type { ICreateUserRequest } from '@/types/user/ICreateUserRequest';
    import type { IUpdateUserRequest } from '@/types/user/IUpdateUserRequest';
    import type { IUpdateUserSystemRequest } from '@/types/user/IUpdateUserSystemRequest';
    // Import modal components
    import CreateUserModal from '@/views/admin/components/users/CreateUserModal.vue';
    import EditUserModal from '@/views/admin/components/users/EditUserModal.vue';
    import UserDetailsModal from '@/views/admin/components/users/UserDetailsModal.vue';
    import DeleteUserModal from '@/views/admin/components/users/DeleteUserModal.vue';
import { getUsersStore } from '@/stores/storeAccessor';
    // Store
    const usersStore = getUsersStore();
    const userService = container.get<IUserService>(TYPES.UserService);
    // State
    const loading = ref(false);
    const error = ref<string | null>(null);
    const users = computed(() => usersStore.getUsers);
    const userDetails = ref<Record<number, IUserDetail>>({});
    // Modal visibility state
    const showCreateModal = ref(false);
    const showEditModal = ref(false);
    const showDetailsModal = ref(false);
    const showDeleteModal = ref(false);
    // Form state for edit
    const editForm = ref({
    username: '',
    email: '',
    is_active: true,
    is_verified: false
    });
    const selectedUserId = ref<number | null>(null);
    const selectedUserDetail = ref<IUserDetail | null>(null);
    // Loading states
    const createLoading = ref(false);
    const editLoading = ref(false);
    const updateLoading = ref(false);
    const detailsLoading = ref(false);
    const deleteLoading = ref(false);
    // Fetch users on mount
    onMounted(async () => {
        loading.value = true;
        try {
            await userService.getAllUsers();
        } catch (err: any) {
            error.value = err.message || 'Failed to load users';
        } finally {
            loading.value = false;
        }
    });

    // Create User
    function openCreateUserModal() {
        showCreateModal.value = true;
    }

    async function createUser(userData: ICreateUserRequest) {
        createLoading.value = true;
        try {
            await userService.createUser(userData);
            showCreateModal.value = false;
            // Refresh user list
            await userService.getAllUsers();
        } catch (err: any) {
            error.value = err.message || 'Failed to create user';
        } finally {
            createLoading.value = false;
        }
    }

    // View User Details
    async function viewUserDetails(userId: number) {
        selectedUserId.value = userId;
        detailsLoading.value = true;
        showDetailsModal.value = true;
        try {
            const details = await userService.getUserDetail(userId);
            selectedUserDetail.value = details;
            userDetails.value[userId] = details;
        } catch (err: any) {
            error.value = err.message || 'Failed to load user details';
        } finally {
            detailsLoading.value = false;
        }
    }

    // Edit User
    async function openEditUserModal(userId: number) {
        selectedUserId.value = userId;
        editLoading.value = true;
        showEditModal.value = true;
        try {
            // Get user details for editing
            let details: IUserDetail;
            if (userDetails.value[userId]) {
                details = userDetails.value[userId];
            } else {
                details = await userService.getUserDetail(userId);
                userDetails.value[userId] = details;
            }
            // Populate edit form
            editForm.value = {
                username: details.username,
                email: details.email,
                is_active: details.is_active,
                is_verified: details.is_verified
            };
        } catch (err: any) {
            error.value = err.message || 'Failed to load user for editing';
            showEditModal.value = false;
        } finally {
            editLoading.value = false;
        }
    }

    async function updateUser(
    userUpdate: IUpdateUserRequest, 
    systemUpdate: IUpdateUserSystemRequest
    ) {
        if (!selectedUserId.value) return;
        updateLoading.value = true;
        try {
            // Update basic user info
            await userService.updateUser(selectedUserId.value, userUpdate);
            // Update system settings
            await userService.updateUserSystem(selectedUserId.value, systemUpdate);
            // Refresh user list and close modal
            await userService.getAllUsers();
            showEditModal.value = false;
        } catch (err: any) {
            error.value = err.message || 'Failed to update user';
        } finally {
            updateLoading.value = false;
        }
    }

    // Delete User
    function confirmDelete(userId: number) {
        selectedUserId.value = userId;
        showDeleteModal.value = true;
    }

    async function deleteUser() {
        if (!selectedUserId.value) return;
        deleteLoading.value = true;
        try {
            await userService.deleteUser(selectedUserId.value);
            showDeleteModal.value = false;
            // Remove from local cache
            if (userDetails.value[selectedUserId.value]) {
                delete userDetails.value[selectedUserId.value];
            }
        } catch (err: any) {
            error.value = err.message || 'Failed to delete user';
        } finally {
            deleteLoading.value = false;
        }
    }
</script>