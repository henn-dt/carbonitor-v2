// src/repositories/IBuildupRepository.ts
import type { BuildupToBackend } from '@/types/buildup/BuildupToBackend';
import type { IBuildup } from '@/types/buildup/IBuildup';

export interface IBuildupRepository {
    getBuildups(): Promise<IBuildup[]>;
    getBuildupById(id: number): Promise<IBuildup>;
    getBuildupByName(uri: string): Promise<IBuildup>;
    createBuildup(dto: Partial<BuildupToBackend>): Promise<IBuildup>;
    updateBuildup(id: number, dto: Partial<BuildupToBackend>): Promise<IBuildup>;
    deleteBuildup(id: number): Promise<boolean>;
}