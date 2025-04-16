// src/services/CookieStorageService.ts
import { injectable } from 'inversify';
import type { IStorageService } from '@/services/IStorageService';
import { StorageKeys } from '@/types/storage/StorageEnum';
import type { IAuthUser } from '@/types/auth/IAuthUser';
import type { Permission } from '@/types/permissions/PermissionEnum';
import type { IStorage } from '@/types/storage/IStorage';

@injectable()
export class CookieStorageService implements IStorageService {
    private accessTokenDays = 7;
    private refreshTokenDays = 7;

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
            const accessTokenExpiry = new Date(accessTokenExpires);
            this.accessTokenDays = Math.ceil((accessTokenExpiry.getTime() - Date.now()) / (1000 * 60 * 60 * 24));
            this.set(StorageKeys.ACCESS_TOKEN_EXPIRES, accessTokenExpires.toString(), this.accessTokenDays);
        }
    }

    setRefreshTokenExpiry(refreshTokenExpires: string | null | undefined): void {
        if (refreshTokenExpires) {
            const refreshTokenExpiry = new Date(refreshTokenExpires);
            this.refreshTokenDays = Math.ceil((refreshTokenExpiry.getTime() - Date.now()) / (1000 * 60 * 60 * 24));
            this.set(StorageKeys.REFRESH_TOKEN_EXPIRES, refreshTokenExpires.toString(), this.refreshTokenDays);
        }
    } 

    setAccessToken(accessToken: string | null | undefined): void {
        if (accessToken) {
            this.set(StorageKeys.ACCESS_TOKEN, accessToken, this.accessTokenDays);
        }
    }

    setRefreshToken(refreshToken: string | null | undefined): void {
        if (refreshToken) {
            this.set(StorageKeys.REFRESH_TOKEN, refreshToken, this.refreshTokenDays);
        }
    }

    setUser(user: IAuthUser | null | undefined): void {
        if (user) {
            this.set(StorageKeys.USER, JSON.stringify(user), this.refreshTokenDays);
        }
    }

    setPermissions(permissions: Permission[] | null | undefined): void {
        if (permissions) {
            this.set(StorageKeys.PERMISSIONS, JSON.stringify(permissions), this.refreshTokenDays);
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
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const name = cookie.split('=')[0].trim();
            this.remove(name);
        }
    }

    // PRIVATE METHODS
    private set(name: string, value: string, days?: number | null): void {
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            const expires = `expires=${date.toUTCString()}`;
            document.cookie = `${name}=${value};${expires};path=/;SameSite=Strict;Secure`;
        } else {
            document.cookie = `${name}=${value};path=/;SameSite=Strict;Secure`;
        }
    }

    private get(name: string): string | null {
        const value = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return value ? value.pop()! : null;
    }

    private remove(name: string): void {
        document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;SameSite=Strict;Secure`;
    }
}