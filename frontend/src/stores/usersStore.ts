// src/stores/usersStore.ts
import { defineStore } from 'pinia';
import type { IUser } from '@/types/user/IUser';
import type { IUserDetail } from '@/types/user/IUserDetail';

interface UsersState {
    users: IUser[];
    currentUser: IUser | null;
    currentUserDetail: IUserDetail | null;
    loading: boolean;
    error: string | null;
}

export const useUsersStore = defineStore('users', {
    state: (): UsersState => ({
        users: [],
        currentUser: null,
        currentUserDetail: null,
        loading: false,
        error: null
    }),

    getters: {
        getUsers: (state) => state.users,
        getUserById: (state) => (id: number) => state.users.find(user => user.id === id),
        getCurrentUser: (state) => state.currentUser,
        getCurrentUserDetail: (state) => state.currentUserDetail,
        isLoading: (state) => state.loading,
        getError: (state) => state.error
    },

    actions: {
        setUsers(users: IUser[]): void {
            this.users = users;
        },

        setCurrentUser(user: IUser | null): void {
            this.currentUser = user;
        },

        setCurrentUserDetail(userDetail: IUserDetail | null): void {
            this.currentUserDetail = userDetail;
        },

        addUser(user: IUser): void {
            const index = this.users.findIndex(u => u.id === user.id);
            if (index === -1) {
                this.users.push(user);
            }
        },

        updateUser(updatedUser: IUser): void {
            const index = this.users.findIndex(user => user.id === updatedUser.id);
            if (index !== -1) {
                this.users[index] = { ...this.users[index], ...updatedUser };
            }
            
            // Also update currentUser if it's the same user
            if (this.currentUser && this.currentUser.id === updatedUser.id) {
                this.currentUser = { ...this.currentUser, ...updatedUser };
            }
        },

        updateUserDetail(updatedUserDetail: IUserDetail): void {
            // Update in the users array
            const index = this.users.findIndex(user => user.id === updatedUserDetail.id);
            if (index !== -1) {
                // Update basic user properties
                this.users[index] = { 
                    ...this.users[index], 
                    email: updatedUserDetail.email, 
                    username: updatedUserDetail.username 
                };
            }
            
            // Update currentUser if it's the same user
            if (this.currentUser && this.currentUser.id === updatedUserDetail.id) {
                this.currentUser = { 
                    ...this.currentUser, 
                    email: updatedUserDetail.email, 
                    username: updatedUserDetail.username 
                };
            }
            
            // Update currentUserDetail if it's the same user
            if (this.currentUserDetail && this.currentUserDetail.id === updatedUserDetail.id) {
                this.currentUserDetail = updatedUserDetail;
            }
        },

        removeUser(userId: number): void {
            this.users = this.users.filter(user => user.id !== userId);
            
            // If the deleted user is the current user, clear it
            if (this.currentUser && this.currentUser.id === userId) {
                this.currentUser = null;
            }
            
            if (this.currentUserDetail && this.currentUserDetail.id === userId) {
                this.currentUserDetail = null;
            }
        },

        setLoading(status: boolean): void {
            this.loading = status;
        },

        setError(error: string | null): void {
            this.error = error;
        },

        resetState(): void {
            this.users = [];
            this.currentUser = null;
            this.currentUserDetail = null;
            this.loading = false;
            this.error = null;
        }
    }
});