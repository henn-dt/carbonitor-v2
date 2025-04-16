import type { CategoryEntityType } from "./CategoryEntityTypeEnum";
import type { ICategory } from "./ICategory";
import type { ICategoryProperty, ICategoryPropertySchema } from "./ICategoryProperty";

/**
 * Category class implementation
 */
export class Category implements ICategory {
    id: number;
    name: string;
    type: CategoryEntityType;
    user_id_created?: number;
    user_id_updated?: number;
    status: string;
    description?: string;
    property_schema?: Record<string, ICategoryPropertySchema>;
    private _properties?: ICategoryProperty[];
  
    constructor(data: ICategory) {
      this.id = data.id;
      this.name = data.name || '';;
      this.type = data.type || '';;
      this.user_id_created = data.user_id_created;
      this.user_id_updated = data.user_id_updated;
      this.status = data.status || "";
      this.description = data.description || "";
      this.property_schema = data.property_schema;

      this._properties = data.properties;
    }

    get properties(): ICategoryProperty[] {
      if (this._properties) return this._properties;
      if (!this.property_schema) return [];
      
      return Object.entries(this.property_schema).map(([id, schema]) => {
          return {
              id,
              name: schema.name,
              format: schema.format,
              description: schema.description,
              default: schema.default,
              required: schema.required,
              enum: schema.enum
          };
      });
  }

    // Setter to update properties
    set properties(newProperties: ICategoryProperty[]) {
      this._properties = newProperties;
      
      // Optionally update property_schema too if needed
      this.property_schema = newProperties.reduce((schema, prop) => {
        schema[prop.id] = {
          name: prop.name,
          format: prop.format,
          description: prop.description,
          default: prop.default,
          required: prop.required,
          enum: prop.enum
        };
        return schema;
      }, {} as Record<string, ICategoryPropertySchema>);
    }
}