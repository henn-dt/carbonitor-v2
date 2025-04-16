import type { IUserRepository } from './IUserRepository';
import { BaseRepository } from './BaseRepository';
import type { IUser } from '@/types/user/IUser';
import type { ICreateUserRequest } from '@/types/user/ICreateUserRequest';
import type { IUpdateUserRequest } from '@/types/user/IUpdateUserRequest';
import type { IUpdateUserSystemRequest } from '@/types/user/IUpdateUserSystemRequest';
import type { IUpdatePasswordRequest } from '@/types/user/IUpdatePasswordRequest';
import type { IUserDetail } from '@/types/user/IUserDetail';
import { inject, injectable } from 'inversify';
import type { IHttpClient } from './IHttpClient';
import { TYPES } from '@/di/types';

@injectable()
export class UserRepository extends BaseRepository implements IUserRepository {
    private usersUrl: string;

    constructor(
        @inject(TYPES.HttpClient) httpClient: IHttpClient
    ) {
        super(httpClient);
        this.usersUrl = `${this.axios.defaults.baseURL}/users/`;
    }

    async getAllUsers(): Promise<IUser[]> {
        const { data } = await this.axios.get<{ data: IUser[] }>(this.usersUrl);
        return data.data;
    }

    async getUserById(userId: number): Promise<IUser> {
        const { data } = await this.axios.get<IUser>(`${this.usersUrl}/${userId}`);
        return data;
    }

    async getUserDetail(userId: number): Promise<IUserDetail> {
        const { data } = await this.axios.get<IUserDetail>(`${this.usersUrl}/${userId}/system`);
        return data;
    }

    async createUser(userData: ICreateUserRequest): Promise<IUser> {
        const { data } = await this.axios.post<IUser>(`${this.usersUrl}/create`, userData);
        return data;
    }

    async updateUser(userId: number, userData: IUpdateUserRequest): Promise<IUser> {
        const { data } = await this.axios.put<IUser>(`${this.usersUrl}/${userId}`, userData);
        return data;
    }

    async updateUserSystem(userId: number, systemData: IUpdateUserSystemRequest): Promise<IUserDetail> {
        const { data } = await this.axios.put<IUserDetail>(`${this.usersUrl}/${userId}/system`, systemData);
        return data;
    }

    async updatePassword(userId: number, passwordData: IUpdatePasswordRequest): Promise<void> {
        await this.axios.put(`${this.usersUrl}/${userId}/password`, passwordData);
    }

    async deleteUser(userId: number): Promise<void> {
        await this.axios.delete(`${this.usersUrl}/${userId}`);
    }
}