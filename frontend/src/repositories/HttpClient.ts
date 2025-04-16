// src/services/HttpClient.ts
import { injectable } from 'inversify';
import axios, { type AxiosInstance, type AxiosResponse, type AxiosError } from 'axios';
import type { IHttpClient } from '@/repositories/IHttpClient';


@injectable()
export class HttpClient implements IHttpClient {
    private axiosInstance: AxiosInstance;
    private isProduction: boolean;
    private nestedPath: string = import.meta.env.VITE_BASE_PATH ?? ""

    constructor() {
        const baseURL = import.meta.env.VITE_API_BASE_URL;
        this.isProduction = import.meta.env.NODE_ENV === 'production' || !baseURL;
        this.axiosInstance = axios.create({
            baseURL,
            headers: {
                'Content-Type': 'application/json',
            },
        });

        this.setupInterceptors();

        this.axiosInstance.interceptors.request.use(config => {
            if (this.isProduction && config.url) {
                
                const originalUrl = config.url;
                // In production, prefix all URLs with /api
                // But ensure we don't duplicate if it already starts with /api
                if (!config.url.startsWith(`${this.nestedPath}/api/`)) {
                    config.url = `${this.nestedPath}/api/${config.url.replace(/^\//, '')}`;
                }
            }
            return config;
        });

    }



    private setupInterceptors(): void {
        this.axiosInstance.interceptors.response.use(
            (response: AxiosResponse) => response,
            (error: AxiosError) => {
                return Promise.reject(error.response?.data || error.message);
            }
        );
    }

    getInstance(): AxiosInstance {
        return this.axiosInstance;
    }
}