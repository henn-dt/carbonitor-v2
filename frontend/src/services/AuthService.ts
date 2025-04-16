// src/services/AuthService.ts
import { injectable, inject } from 'inversify';
import type { IAuthService } from '@/services/IAuthService';
import type { IAuthRepository } from '@/repositories/IAuthRepository';
import type { IStorageService } from '@/services/IStorageService';
import type { ILoginCredentials } from '@/types/auth/ILoginCredentials';
import type { IRegisterCredentials } from '@/types/auth/IRegisterCredentials';
import { TYPES } from '@/di/types';
import type { IAuthResponse } from '@/types/auth/IAuthResponse';
import { AuthUser } from '@/types/auth/AuthUser';
import { getAuthStore } from '@/stores/storeAccessor';

@injectable()
export class AuthService implements IAuthService {
    constructor(
        @inject(TYPES.AuthRepository) private authRepository: IAuthRepository,
        @inject(TYPES.StorageService.Persistent) private persistentStorage: IStorageService,
        @inject(TYPES.StorageService.Session) private sessionStorage: IStorageService
    ) {}
    
    private setAuthData(authResponse: IAuthResponse, rememberMe: boolean): void {
        const authStore = getAuthStore();
        const storage = rememberMe ? this.persistentStorage : this.sessionStorage;
		 const {
			user_id, username, email, permissions, access_token,
			refresh_token, access_token_expires, refresh_token_expires
		} = authResponse
        const user = new AuthUser(user_id, email, username);
        storage.setAllStorageKeys({
            access_token, refresh_token, access_token_expires,
            refresh_token_expires, user, permissions
        })
        authStore.updateAuthenticationData({
            user: user,
            accessToken: access_token,
            refreshToken: refresh_token,
            permissions: permissions,
            rememberMe,
            accessTokenExpires: new Date(access_token_expires),
            refreshTokenExpires: new Date(refresh_token_expires)
        });
        authStore.setAuthenticated(true);
    }

    initAuthData(): void {
        const rememberMe = this.persistentStorage.getAccessToken() ? true : false;
        const storage = rememberMe ? this.persistentStorage : this.sessionStorage;
        const authStore = getAuthStore();
        const storageData = storage.getAllStorageKeys();
        const accessTokenExpires = storageData.access_token_expires ? new Date(storageData.access_token_expires) : null
        const refreshTokenExpires = storageData.refresh_token_expires ? new Date(storageData.refresh_token_expires) : null
        if (!storageData.access_token) {
            authStore.setAuthenticated(false);
        } else {
            authStore.setAuthenticated(true);
        }
        authStore.updateAuthenticationData({
            user: storageData.user,
            accessToken: storageData.access_token,
            refreshToken: storageData.refresh_token,
            permissions: storageData.permissions,
            rememberMe,
            accessTokenExpires: accessTokenExpires,
            refreshTokenExpires: refreshTokenExpires
        });
    }

    async login(credentials: ILoginCredentials): Promise<void> {
        const response = await this.authRepository.login(credentials);
		if (response) 
        	this.setAuthData(response, credentials.rememberMe || false);
    }

    async register(credentials: IRegisterCredentials): Promise<void> {
        const response = await this.authRepository.register(credentials);
		if (response)
        	this.setAuthData(response, false);
    }

    async logout(): Promise<void> {
        const authStore = getAuthStore();
        const userId = authStore.getUser?.id;

        if (userId) {
            try {
                await this.authRepository.logout(userId);
            } finally {
                this.clearAuthData();
                authStore.logout();
            }
        }
    }

    private clearAuthData(): void {
        this.sessionStorage.clear();
        this.persistentStorage.clear();
    }

    async refreshToken(): Promise<void> {
        const authStore = getAuthStore();
        const refreshToken = authStore.getRefreshToken;

        if (!refreshToken) {
            throw new Error('No refresh token available');
        }

        try {
            const response = await this.authRepository.refresh(refreshToken);
            this.setAuthData(response, authStore.isRememberMe);
        } catch (error) {
            this.clearAuthData();
            authStore.logout();
            throw error;
        }
    }
}