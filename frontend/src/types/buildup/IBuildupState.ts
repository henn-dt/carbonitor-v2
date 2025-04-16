import type { IBuildup } from "@/types/buildup/IBuildup";
import type { IBuildupWithProcessedProducts } from "../epdx/IBuildupWithProcessedProducts";

export interface IBuildupState {
    buildups: IBuildup[];
    selectedBuildup: IBuildup | null;
    
    loading: boolean;
    error: string | null;
    needsRefresh: boolean;
    lastFetchTimestamp: number | null;

    processedBuildups: IBuildupWithProcessedProducts[],
    processingStatus: Record<number, boolean>;
    processingErrors: Record<number, string | null>;
    processingAll: boolean;
}