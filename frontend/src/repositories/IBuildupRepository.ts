// src/repositories/IBuildupRepository.ts
import type { IBuildup } from '@/types/buildup/IBuildup';

export interface IBuildupRepository {
    getBuildups(): Promise<IBuildup[]>;
    getBuildupById(id: number): Promise<IBuildup>;
    getBuildupByName(uri: string): Promise<IBuildup>;
    createBuildup(product: Partial<IBuildup>): Promise<IBuildup>;
    updateBuildup(id: number, product: Partial<IBuildup>): Promise<IBuildup>;
    deleteBuildup(id: number): Promise<boolean>;
}