import type {
    IBuildup,
    ReferenceSourceForProduct,
} from '@/types/buildup/IBuildup';
import type { Classification, Unit, Reference } from 'lcax';

export class Buildup implements IBuildup {
    id: number;
    status: string;
    user_id_created: number;
    user_id_updated: number;
    created_at?: string; // ISO date string from backend
    updated_at?: string; // ISO date string from backend
    name: string;
    description: string;
    comment: string;
    quantity: number;
    unit: Unit;
    classification: Classification[] | null;
    products: Record<string, ReferenceSourceForProduct>;
    results: Record<string,  any> | null;
    metaData: Record<string,  any> | null;
  
    constructor(dto: any) {
      this.status = dto.status || '';
      this.user_id_created = dto.user_id_created;
      this.user_id_updated = dto.user_id_updated;
      this.created_at = dto.created_at; // ISO date string from backend
      this.updated_at = dto.updated_at; // ISO date string from backend
      this.id = dto.id;
      this.name = dto.name;
      this.description = dto.description || "";
      this.comment = dto.comment || "";
      this.quantity = dto.quantity;
      this.unit = dto.unit;
      this.classification = this.classification = dto.classification ? (typeof dto.classification === 'string' ? JSON.parse(dto.classification) : dto.classification) : null;
      this.results = dto.results || null;
      this.metaData = dto.meta_data || null; // Notice conversion from snake_case to camelCase 
      this.products = dto.products || {};
    }
}