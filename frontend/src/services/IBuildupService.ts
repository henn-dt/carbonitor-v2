// src/services/IBuildupService.ts
import type { IBuildup } from '@/types/buildup/IBuildup';

export interface IBuildupService {

  getBuildups(): Promise<IBuildup[]>;
  getBuildupById(id: number): Promise<IBuildup>;
  createBuildup(buildup: Partial<IBuildup>): Promise<IBuildup>;
  updateBuildup(id: number, buildup: Partial<IBuildup>): Promise<IBuildup>;
  deleteBuildup(id: number): Promise<boolean>;
  deleteMultipleBuildups(ids: number[]): Promise<{ success: number, failed: number }>;
  getBuildupByName(uri: string): Promise<IBuildup> ;
  subscribeToBuildups(callback: (buildups: IBuildup[]) => void): () => void;
}