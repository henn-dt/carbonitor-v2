import type { CategoryPropertyFormat } from "./CategoryPropertyFormatEnum";

/**
 * Interface for category property schema
 */
export interface ICategoryPropertySchema {
    name: string;
    description?: string;
    format: CategoryPropertyFormat;
    default?: any;
    required?: boolean;
    enum?: any[];
  }

/**
 * Interface for category property extending schema with ID
 */
export interface ICategoryProperty extends ICategoryPropertySchema {
  id: string;
}