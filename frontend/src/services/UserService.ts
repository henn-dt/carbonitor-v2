// src/services/UserService.ts
import { injectable, inject } from 'inversify';
import type { IUserService } from '@/services/IUserService';
import type { IUserRepository } from '@/repositories/IUserRepository';
import type { IUser } from '@/types/user/IUser';
import type { ICreateUserRequest } from '@/types/user/ICreateUserRequest';
import type { IUpdateUserRequest } from '@/types/user/IUpdateUserRequest';
import type { IUpdateUserSystemRequest } from '@/types/user/IUpdateUserSystemRequest';
import type { IUpdatePasswordRequest } from '@/types/user/IUpdatePasswordRequest';
import type { IUserDetail } from '@/types/user/IUserDetail';
import { useUsersStore } from '@/stores/usersStore';
import { TYPES } from '@/di/types';
import { getUsersStore } from '@/stores/storeAccessor';

@injectable()
export class UserService implements IUserService {
    constructor(
        @inject(TYPES.UserRepository) private userRepository: IUserRepository
    ) {}

    async getAllUsers(): Promise<IUser[]> {
        const usersStore = getUsersStore();
        try {
            const users = await this.userRepository.getAllUsers();
            usersStore.setUsers(users);
            return users;
        } catch (error) {
            console.error('Error fetching users:', error);
            throw error;
        }
    }

    async getUserById(userId: number): Promise<IUser> {
        try {
            return await this.userRepository.getUserById(userId);
        } catch (error) {
            console.error(`Error fetching user with id ${userId}:`, error);
            throw error;
        }
    }

    async getUserDetail(userId: number): Promise<IUserDetail> {
        const usersStore = getUsersStore();
        try {
            const userDetail = await this.userRepository.getUserDetail(userId);
            usersStore.setCurrentUserDetail(userDetail);
            return userDetail;
        } catch (error) {
            console.error(`Error fetching user detail with id ${userId}:`, error);
            throw error;
        }
    }

    async createUser(userData: ICreateUserRequest): Promise<IUser> {
        const usersStore = getUsersStore();
        try {
            const newUser = await this.userRepository.createUser(userData);
            usersStore.addUser(newUser);
            return newUser;
        } catch (error) {
            console.error('Error creating user:', error);
            throw error;
        }
    }

    async updateUser(userId: number, userData: IUpdateUserRequest): Promise<IUser> {
        const usersStore = getUsersStore();
        try {
            const updatedUser = await this.userRepository.updateUser(userId, userData);
            usersStore.updateUser(updatedUser);
            return updatedUser;
        } catch (error) {
            console.error(`Error updating user with id ${userId}:`, error);
            throw error;
        }
    }

    async updateUserSystem(userId: number, systemData: IUpdateUserSystemRequest): Promise<IUserDetail> {
        const usersStore = getUsersStore();
        try {
            const updatedUserDetail = await this.userRepository.updateUserSystem(userId, systemData);
            usersStore.updateUserDetail(updatedUserDetail);
            return updatedUserDetail;
        } catch (error) {
            console.error(`Error updating user system data with id ${userId}:`, error);
            throw error;
        }
    }

    async updatePassword(userId: number, passwordData: IUpdatePasswordRequest): Promise<void> {
        try {
            await this.userRepository.updatePassword(userId, passwordData);
        } catch (error) {
            console.error(`Error updating password for user with id ${userId}:`, error);
            throw error;
        }
    }

    async deleteUser(userId: number): Promise<void> {
        const usersStore = getUsersStore();
        try {
            await this.userRepository.deleteUser(userId);
            usersStore.removeUser(userId);
        } catch (error) {
            console.error(`Error deleting user with id ${userId}:`, error);
            throw error;
        }
    }
}