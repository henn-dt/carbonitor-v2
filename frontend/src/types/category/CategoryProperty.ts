import type { CategoryPropertyFormat } from "./CategoryPropertyFormatEnum";
import type { ICategoryProperty } from "./ICategoryProperty";

/**
 * CategoryProperty class implementation
 */
export class CategoryProperty implements ICategoryProperty {
    id: string;
    name: string;
    description?: string;
    format: CategoryPropertyFormat;
    default?: any;
    required?: boolean;
    enum?: any[];
  
    constructor(data: ICategoryProperty) {
      this.id = data.id;
      this.name = data.name;
      this.description = data.description;
      this.format = data.format;
      this.default = data.default;
      this.required = data.required || false;
      this.enum = data.enum;
    }
}