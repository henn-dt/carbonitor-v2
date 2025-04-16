import type { IAuthRepository } from './IAuthRepository';
import { BaseRepository } from './BaseRepository';
import type { ILoginCredentials } from '@/types/auth/ILoginCredentials';
import type { IAuthResponse } from '@/types/auth/IAuthResponse';
import type { IRegisterCredentials } from '@/types/auth/IRegisterCredentials';
import { inject, injectable } from 'inversify';
import type { IHttpClient } from './IHttpClient';
import { TYPES } from '@/di/types';

@injectable()
export class AuthRepository extends BaseRepository implements IAuthRepository {
    private authUrl: string;

    constructor(
        @inject(TYPES.HttpClient) httpClient: IHttpClient
    ) {
        super(httpClient);
        this.authUrl = `${this.axios.defaults.baseURL}/auth`; 
    }

    async login(credentials: ILoginCredentials): Promise<IAuthResponse> {
        const { data } = await this.axios.post<IAuthResponse>(`${this.authUrl}/login`, credentials);
        return data;
    }

    async register(credentials: IRegisterCredentials): Promise<IAuthResponse> {
        const { data } = await this.axios.post<IAuthResponse>(`${this.authUrl}/register`, credentials);
        return data;
    }

    async refresh(refreshToken: string): Promise<IAuthResponse> {
        const { data } = await this.axios.post<IAuthResponse>(`${this.authUrl}/refresh`, { refresh_token: refreshToken });
        return data;
    }

    async logout(userId: number): Promise<void> {
        await this.axios.post(`${this.authUrl}/logout`, { user_id: userId });
    }
}