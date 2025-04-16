import type { AxiosInstance } from 'axios';

export interface IHttpClient {
    getInstance(): AxiosInstance;
}