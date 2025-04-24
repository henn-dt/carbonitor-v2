//frontend/src/repositories/BuildupRepository.ts

import type { IBuildupRepository } from './IBuildupRepository';
import { BaseRepository } from './BaseRepository';
import type { IBuildup } from '@/types/buildup/IBuildup';
import { inject, injectable } from 'inversify';
import type { IHttpClient } from './IHttpClient';
import { TYPES } from '@/di/types';
import type { BuildupToBackend } from '@/types/buildup/BuildupToBackend';


@injectable()
export class BuildupRepository extends BaseRepository implements IBuildupRepository {
    private buildupUrl: string;

    constructor(
        @inject(TYPES.HttpClient) httpClient: IHttpClient
    ) {
        super(httpClient);
        this.buildupUrl = `${this.axios.defaults.baseURL}/buildups/`;
    }

    async getBuildups(): Promise<IBuildup[]> {
        try {
            const { data } = await this.axios.get<IBuildup[]>(this.buildupUrl);
            return data;
        } catch (error) {
            console.error('Error fetching buildups:', error);
            throw error;
        }
    }

    async getBuildupById(id: number): Promise<IBuildup> {
        try {
            const { data } = await this.axios.get<IBuildup>(`${this.buildupUrl}${id}`);
            return data;
        } catch (error) {
            console.error(`Error fetching buildup with id ${id}:`, error);
            throw error;
        }
    }

    async getBuildupByName(name: string): Promise<IBuildup> {
        try {
            const { data } = await this.axios.get<IBuildup>(`${this.buildupUrl}name/${name}`);
            return data;
        } catch (error) {
            console.error(`Error fetching buildup with name ${name}:`, error);
            throw error;
        }
    }

    async createBuildup(buildup: Partial<BuildupToBackend>): Promise<IBuildup> {
        try {
            const { data } = await this.axios.post<IBuildup>(this.buildupUrl, buildup);
            return data;
        } catch (error) {
            console.error('Error creating buildup:', error);
            throw error;
        }
    }

    async updateBuildup(id: number, buildup: Partial<BuildupToBackend>): Promise<IBuildup> {
        try {
        // Create a copy to work with
        const processedBuildup = { ...buildup };
        
        const { data } = await this.axios.put<IBuildup>(`${this.buildupUrl}${id}`, processedBuildup);
            return data;
        } catch (error) {
            console.error(`Error updating buildup with id ${id}:`, error);
            throw error;
        }
    }

    async deleteBuildup(id: number): Promise<boolean> {
        try {
            await this.axios.delete(`${this.buildupUrl}${id}`);
            return true;
        } catch (error) {
            console.error(`Error deleting buildup with id ${id}:`, error);
            throw error;
        }
    }
}