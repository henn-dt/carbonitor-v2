import type { IUser } from '@/types/user/IUser';
import type { ICreateUserRequest } from '@/types/user/ICreateUserRequest';
import type { IUpdateUserRequest } from '@/types/user/IUpdateUserRequest';
import type { IUpdateUserSystemRequest } from '@/types/user/IUpdateUserSystemRequest';
import type { IUpdatePasswordRequest } from '@/types/user/IUpdatePasswordRequest';
import type { IUserDetail } from '@/types/user/IUserDetail';

export interface IUserService {
    getAllUsers(): Promise<IUser[]>;
    getUserById(userId: number): Promise<IUser>;
    getUserDetail(userId: number): Promise<IUserDetail>;
    createUser(userData: ICreateUserRequest): Promise<IUser>;
    updateUser(userId: number, userData: IUpdateUserRequest): Promise<IUser>;
    updateUserSystem(userId: number, systemData: IUpdateUserSystemRequest): Promise<IUserDetail>;
    updatePassword(userId: number, passwordData: IUpdatePasswordRequest): Promise<void>;
    deleteUser(userId: number): Promise<void>;
}