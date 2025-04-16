import type { IBuildup } from "@/types/buildup/IBuildup";
import type { IBuildupWithProcessedProducts } from "@/types/epdx/IBuildupWithProcessedProducts";

export interface IBuildupProcessService {

    processBuildup(buildupId: number): Promise<IBuildupWithProcessedProducts>
    getCombinedBuildup(buildupId: number): (IBuildup & IBuildupWithProcessedProducts)
    getAllCombinedBuildups(): (IBuildup & IBuildupWithProcessedProducts)[]
    processAllBuildups(): Promise<IBuildupWithProcessedProducts[]>
    subscribeToBuildupProcess(callback: (processedBuildups: IBuildupWithProcessedProducts[]) => void): () => void
}