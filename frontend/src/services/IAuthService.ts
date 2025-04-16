// src/interfaces/IAuthService.ts
import type { ILoginCredentials } from '@/types/auth/ILoginCredentials';
import type { IRegisterCredentials } from '@/types/auth/IRegisterCredentials';

export interface IAuthService {
    login(credentials: ILoginCredentials): Promise<void>;
    register(credentials: IRegisterCredentials): Promise<void>;
    logout(): Promise<void>;
    refreshToken(): Promise<void>;
    initAuthData(): void;
}