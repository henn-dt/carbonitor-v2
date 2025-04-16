export interface IProduct {
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
    epdx: string;
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
}