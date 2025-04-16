import type { IProduct } from "@/types/product/IProduct";

export class Product implements IProduct {
    id: number;
    status: string;
    user_created: string;
    user_updated: string;
    epd_name: string;
    epd_declaredUnit: string;
    epd_version: string;
    epd_publishedDate: string;
    epd_validUntil: string;
    epd_standard: string;
    epd_comment: string;
    epd_location: string;
    epd_formatVersion: string;
    epd_id: string;
    epdx: any;
    epd_sourceName: string;
    epd_sourceUrl: string;
    epd_linear_density: number | null;
    epd_gross_density: number | null;
    epd_grammage: number | null;
    epd_layer_thickness: number | null;
    epd_subtype: string;
    epd_bulk_density: number | null;
    date_created: string;
    date_updated: string;
  
    constructor(data: Partial<IProduct>) {
      this.id = data.id || 0;
      this.status = data.status || '';
      this.user_created = data.user_created || '';
      this.user_updated = data.user_updated || '';
      this.epd_name = data.epd_name || '';
      this.epd_declaredUnit = data.epd_declaredUnit || '';
      this.epd_version = data.epd_version || '';
      this.epd_publishedDate = data.epd_publishedDate || '';
      this.epd_validUntil = data.epd_validUntil || '';
      this.epd_standard = data.epd_standard || '';
      this.epd_comment = data.epd_comment || '';
      this.epd_location = data.epd_location || '';
      this.epd_formatVersion = data.epd_formatVersion || '';
      this.epd_id = data.epd_id || '';
      this.epdx = data.epdx || null;
      this.epd_sourceName = data.epd_sourceName || '';
      this.epd_sourceUrl = data.epd_sourceUrl || '';
      this.epd_linear_density = data.epd_linear_density || null;
      this.epd_gross_density = data.epd_gross_density || null;
      this.epd_grammage = data.epd_grammage || null;
      this.epd_layer_thickness = data.epd_layer_thickness || null;
      this.epd_subtype = data.epd_subtype || '';
      this.epd_bulk_density = data.epd_bulk_density || null;
      this.date_created = data.date_created || '';
      this.date_updated = data.date_updated || '';
    }
}