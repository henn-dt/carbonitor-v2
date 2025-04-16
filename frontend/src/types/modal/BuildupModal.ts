import type { IBuildup } from "@/types/buildup/IBuildup";

export type SaveBuildupHandler = (entityDTO: IBuildup) => Promise<void>;
export type DeleteBuildupHandler = (entityId: number) => Promise<void>;
export type CloseBuildupHandler = () => void;

export interface BuildupDetailParams {
    buildupId: number;
    isNew?: boolean;
    onSave: SaveBuildupHandler;
    onDelete: DeleteBuildupHandler;
    onClose: CloseBuildupHandler}