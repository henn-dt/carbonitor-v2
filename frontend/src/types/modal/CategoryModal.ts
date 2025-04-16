import type { ICategory } from "../category/ICategory";

export type SaveCategoryHandler = (entityDTO: ICategory) => Promise<void>;
export type DeleteCategoryHandler = (entityId: number) => Promise<void>;


export interface CategoryDetailParams {
    data: ICategory;
    isNew?: boolean;
    isSaving: boolean;
    sectionType: string;
    existingCategories: ICategory[];
    onSave: SaveCategoryHandler;
    onDelete: DeleteCategoryHandler;}