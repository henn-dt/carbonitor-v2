import axios from 'axios';
import type { AxiosInstance, AxiosResponse, AxiosError } from 'axios';
import type { IBaseRepository } from '@/repositories/IBaseRepository';
import type { IHttpClient } from '@/repositories/IHttpClient';
import { TYPES } from '@/di/types';
import { inject, injectable } from 'inversify';

@injectable()
export class BaseRepository implements IBaseRepository {
    protected axios: AxiosInstance;

    constructor(
        @inject(TYPES.HttpClient) httpClient: IHttpClient
    ) {
        this.axios = httpClient.getInstance();
    }

    // Generic methods like GET, POST, PUT, etc...
    async get<T>(url: string, params?: any): Promise<T> {
        try {
            const { data } = await this.axios.get<T>(url, { params });
            return data;
        } catch (error) {
            throw error;
        }
    }

    async post<T>(url: string, payload: any): Promise<T> {
        try {
            const { data } = await this.axios.post<T>(url, payload);
            return data;
        } catch (error) {
            throw error;
        }
    }

    async put<T>(url: string, payload: any): Promise<T> {
        try {
            const { data } = await this.axios.put<T>(url, payload);
            return data;
        } catch (error) {
            throw error;
        }
    }

    async delete<T>(url: string, params?: any): Promise<T> {
        try {
            const { data } = await this.axios.delete<T>(url, { params });
            return data;
        } catch (error) {
            throw error;
        }
    }
}