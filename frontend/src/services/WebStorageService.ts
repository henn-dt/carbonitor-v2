// src/services/WebStorageService.ts
import { injectable, inject } from 'inversify';
import type { IStorageService } from '@/services/IStorageService';
import { StorageKeys } from '@/types/storage/StorageEnum';
import type { IAuthUser } from '@/types/auth/IAuthUser';
import type { Permission } from '@/types/permissions/PermissionEnum';
import type { IStorage } from '@/types/storage/IStorage';

export type StorageType = 'local' | 'session';

@injectable()
export class WebStorageService implements IStorageService {
    private storage: Storage;

    constructor(@inject('StorageType') storageType: StorageType = 'session') {
        this.storage = storageType === 'local' ? localStorage : sessionStorage;
    }

    // GETTERS
    getAccessToken(): string | null {
        return this.get(StorageKeys.ACCESS_TOKEN);
    }

    getRefreshToken(): string | null {
        return this.get(StorageKeys.REFRESH_TOKEN);
    }

    getAccessTokenExpiry(): string | null {
        return this.get(StorageKeys.ACCESS_TOKEN_EXPIRES);
    }

    getRefreshTokenExpiry(): string | null {
        return this.get(StorageKeys.REFRESH_TOKEN_EXPIRES);
    }

    getUser(): IAuthUser | null {
        const user = this.get(StorageKeys.USER);
        return user ? JSON.parse(user) : null;
    }

    getPermissions(): Permission[] | null {
        const permissions = this.get(StorageKeys.PERMISSIONS);
        return permissions ? JSON.parse(permissions) : null;
    }

    getAllStorageKeys(): IStorage {
        return {
            access_token: this.getAccessToken(),
            refresh_token: this.getRefreshToken(),
            access_token_expires: this.getAccessTokenExpiry(),
            refresh_token_expires: this.getRefreshTokenExpiry(),
            user: this.getUser(),
            permissions: this.getPermissions()
        }
    }

    // SETTERS
    setAccessTokenExpiry(accessTokenExpires: string | null | undefined): void {
        if (accessTokenExpires) {
            this.set(StorageKeys.ACCESS_TOKEN_EXPIRES, accessTokenExpires.toString());
        }
    }

    setRefreshTokenExpiry(refreshTokenExpires: string | null | undefined): void {
        if (refreshTokenExpires) {
            this.set(StorageKeys.REFRESH_TOKEN_EXPIRES, refreshTokenExpires.toString());
        }
    } 

    setAccessToken(accessToken: string | null | undefined): void {
        if (accessToken) {
            this.set(StorageKeys.ACCESS_TOKEN, accessToken);
        }
    }

    setRefreshToken(refreshToken: string | null | undefined): void {
        if (refreshToken) {
            this.set(StorageKeys.REFRESH_TOKEN, refreshToken);
        }
    }

    setUser(user: IAuthUser | null | undefined): void {
        if (user) {
            this.set(StorageKeys.USER, JSON.stringify(user));
        }
    }

    setPermissions(permissions: Permission[] | null | undefined): void {
        if (permissions) {
            this.set(StorageKeys.PERMISSIONS, JSON.stringify(permissions));
        }
    }

    setAllStorageKeys(storage: IStorage | undefined): void {
        if (storage) {
            this.setUser(storage?.user);
            this.setAccessTokenExpiry(storage?.access_token_expires);
            this.setRefreshTokenExpiry(storage?.refresh_token_expires);
            this.setAccessToken(storage?.access_token);
            this.setRefreshToken(storage?.refresh_token);
            this.setPermissions(storage?.permissions);
        }
    }

    // DELETE
    clear(): void {
        this.storage.clear();
    }

    // PRIVATE METHODS
    private set(key: string, value: string): void {
        this.storage.setItem(key, value);
    }

    private get(key: string): string | null {
        return this.storage.getItem(key);
    }

    private remove(key: string): void {
        this.storage.removeItem(key);
    }
}