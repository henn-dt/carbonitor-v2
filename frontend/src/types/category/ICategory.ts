import type { CategoryEntityType } from "./CategoryEntityTypeEnum";
import type { ICategoryProperty, ICategoryPropertySchema } from "./ICategoryProperty";


/**
 * Base interface for category
 */
export interface ICategory {
    id: number;
    name: string;
    type: CategoryEntityType;
    user_id_created?: number;
    user_id_updated?: number;
    status: string;
    description?: string;
    property_schema?: Record<string, ICategoryPropertySchema>;
    properties? : ICategoryProperty[]
  }