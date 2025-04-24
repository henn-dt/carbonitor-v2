import type { Classification } from "lcax";


export class BuildupToBackend {
    id?: number
    status: string;
    user_id_created: number;
    user_id_updated: number;
    name: string;
    description?: string;
    unit?: string; // or your Unit type
    comment?: string;
    classification?: any;
    quantity?: number;
    meta_data: Record<string, any> | null;
    products?: Record<string, any>;
    results?: Record<string, any> | null;



    constructor(buildup: any) {
        if (buildup.id) this.id = buildup.id
        this.status = buildup.status;
        this.user_id_created = buildup.user_id_created;
        this.user_id_updated = buildup.user_id_updated;
        this.name = buildup.name;
        if (buildup.description) this.description = buildup.description;
        if (buildup.unit) this.unit = buildup.unit as string; // or handle properly
        if (buildup.comment) this.comment = buildup.comment;
        if (buildup.classification) this.classification = buildup.classification;
        if (buildup.quantity) this.quantity = buildup.quantity;
        console.log('frontend metaData')
        console.log(buildup.metaData)
        this.meta_data = buildup.metaData;
        console.log('meta_data to backend')
        console.log(this.meta_data)
        if (buildup.products) this.products = buildup.products;
        if (buildup.results) this.results = buildup.results;
        // do NOT include id on POST; only add it if required for PUT
      }
} 

function safeParsing(input: any): Classification[] | null {
    if (!input) return null;
    if (Array.isArray(input)) return input;
    if (typeof input === "object") return [input];
    if (typeof input === "string") {
      try {
        return JSON.parse(input);
      } catch (e) {
        try {
          const fixed = input.trim().replace(/'/g, '"');
          return JSON.parse(fixed);
        } catch {
          return null;
        }
      }
    }
    return null;
  }