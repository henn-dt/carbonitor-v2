// Create this file: src/types/category/ICreateCategory.ts
import type { CategoryEntityType } from "./CategoryEntityTypeEnum";
import type { ICategoryPropertySchema } from "./ICategoryProperty";

/**
 * Interface for creating a new category (without ID)
 */
export interface ICreateCategory {
    name: string;
    type: CategoryEntityType;
    status: string;
    description?: string;
    property_schema?: Record<string, ICategoryPropertySchema>;
}