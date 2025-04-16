import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import { ColumnFilterOperator } from '@/views/shared/ColumnSelector/ColumnFilterOperator';
import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';

// Define product columns for the column selector
export const productColumns: ColumnDefinition[] = [
  // Core product information
	{
		key: 'id',
		label: 'ID',
		default: false,
		visible: false,
		tooltip: 'Product database ID',
		columnProperties: { 
			type: ColumnType.numeric,
			minWidth: 50,
			maxWidth: 100,
			defaultValue: 0,
			filter: { 
				operators: [ColumnFilterOperator.gt, ColumnFilterOperator.lt],
				defaultOperator: ColumnFilterOperator.gt 
			}
		},
    	columnValues: []
	},
	{
		key: 'epd_name',
		label: 'Product Name',
		default: true,
		visible: true,
		tooltip: 'Product name from EPD',
		columnProperties: { 
			type: ColumnType.string,
			minWidth: 100,
			maxWidth: 500,
			defaultValue: "",
			filter: {
				defaultOperator: ColumnFilterOperator.consists
			}
		},
    	columnValues: []
	},
	{
		key: 'epd_id',
		label: 'EPD ID',
		default: true,
		visible: true,
		tooltip: 'Environmental Product Declaration ID',
		columnProperties: { 
			type: ColumnType.string,
			minWidth: 100,
			maxWidth: 250,
			defaultValue: "",
			filter: {
				defaultOperator: ColumnFilterOperator.consists
			}
		},
    	columnValues: []
	},
  	{
		key: 'epd_declaredUnit',
		label: 'Unit',
		default: true,
		visible: true,
		tooltip: 'Declared unit of measurement',
		columnProperties: { 
			type: ColumnType.string,
			minWidth: 50,
			maxWidth: 100,
			defaultValue: "",
			filter: {
				defaultOperator: ColumnFilterOperator.consists 
			}
		},
    	columnValues: []
	},
  	{
		key: 'status',
		label: 'Status',
		default: true,
		visible: true,
		tooltip: 'Current product status',
		columnProperties: { 
			type: ColumnType.string,
			minWidth: 50,
			maxWidth: 150,
			defaultValue: null,
			filter: {
				defaultOperator: ColumnFilterOperator.consists
			}
		},
    	columnValues: []
	},
  
	// EPD Information
	{
		key: 'epd_version',
		label: 'Version',
		default: false,
		visible: false,
		tooltip: 'EPD version number',
		columnProperties: { 
			type: ColumnType.string,
			minWidth: 50,
			maxWidth: 150,
			defaultValue: null,
			filter: {
				defaultOperator: ColumnFilterOperator.consists
			}
		},
    	columnValues: []
	},
	{
		key: 'epd_publishedDate',
		label: 'Published',
		default: false,
		visible: false,
		tooltip: 'Publication date of the EPD',
		columnProperties: { 
			type: ColumnType.date,
			minWidth: 100,
			maxWidth: 200,
			defaultValue: new Date('1970-01-01T00:00:00Z'),
			filter: { 
				operators: [ColumnFilterOperator.gt, ColumnFilterOperator.lt],
				defaultOperator: ColumnFilterOperator.gt 
			}
		},
    	columnValues: []
	},
	{
		key: 'epd_validUntil',
		label: 'Valid Until',
		default: false,
		visible: false,
		tooltip: 'Expiration date of the EPD',
		columnProperties: { 
			type: ColumnType.date,
			minWidth: 100,
			maxWidth: 200,
			defaultValue: new Date('1970-01-01T00:00:00Z'),
			filter: { 
				operators: [ColumnFilterOperator.gt, ColumnFilterOperator.lt],
				defaultOperator: ColumnFilterOperator.gt 
			}
		},
    	columnValues: []
	},
	{
		key: 'epd_standard',
		label: 'Standard',
		default: false,
		visible: false,
		tooltip: 'EPD standard or norm',
		columnProperties: { 
			type: ColumnType.string,
			minWidth: 50,
			maxWidth: 150,
			defaultValue: null,
			filter: {
				defaultOperator: ColumnFilterOperator.consists
			}
		},
    	columnValues: []
	},
	{
		key: 'epd_location',
		label: 'Location',
		default: false,
		visible: false,
		tooltip: 'Geographical location',
		columnProperties: { 
			type: ColumnType.string,
			minWidth: 100,
			maxWidth: 200,
			defaultValue: null,
			filter: {
				defaultOperator: ColumnFilterOperator.consists
			}
		},
    	columnValues: []
	},
	{
		key: 'epd_formatVersion',
		label: 'Format Version',
		default: false,
		visible: false,
		tooltip: 'EPD format version',
		columnProperties: { 
			type: ColumnType.string,
			minWidth: 100,
			maxWidth: 200,
			defaultValue: null,
			filter: {
				defaultOperator: ColumnFilterOperator.consists
			}
		},
    	columnValues: []
	},
	{
		key: 'epd_subtype',
		label: 'Subtype',
		default: false,
		visible: false,
		tooltip: 'Product subtype classification',
		columnProperties: { 
			type: ColumnType.string,
			minWidth: 100,
			maxWidth: 200,
			defaultValue: null,
			filter: {
				defaultOperator: ColumnFilterOperator.consists
			}
		},
    	columnValues: []
	},
	
	// Physical properties
	{
		key: 'epd_linear_density',
		label: 'Linear Density',
		default: false,
		visible: false,
		tooltip: 'Linear density of the product',
		columnProperties: { 
			type: ColumnType.numeric,
			minWidth: 100,
			maxWidth: 200,
			defaultValue: null,
			filter: { 
				operators: [ColumnFilterOperator.gt, ColumnFilterOperator.lt],
				defaultOperator: ColumnFilterOperator.gt 
			}
		},
    	columnValues: []
	},
	{
		key: 'epd_gross_density',
		label: 'Gross Density',
		default: false,
		visible: false,
		tooltip: 'Gross density of the product',
		columnProperties: { 
			type: ColumnType.numeric,
			minWidth: 100,
			maxWidth: 200,
			defaultValue: null,
			filter: { 
				operators: [ColumnFilterOperator.gt, ColumnFilterOperator.lt],
				defaultOperator: ColumnFilterOperator.gt 
			}
		},
    	columnValues: []
	},
	{
		key: 'epd_bulk_density',
		label: 'Bulk Density',
		default: false,
		visible: false,
		tooltip: 'Bulk density of the product',
		columnProperties: { 
			type: ColumnType.numeric,
			minWidth: 100,
			maxWidth: 200,
			defaultValue: null,
			filter: { 
				operators: [ColumnFilterOperator.gt, ColumnFilterOperator.lt],
				defaultOperator: ColumnFilterOperator.gt 
			}
		},
    	columnValues: []
	},
	{
		key: 'epd_grammage',
		label: 'Grammage',
		default: false,
		visible: false,
		tooltip: 'Grammage of the product',
		columnProperties: { 
			type: ColumnType.numeric,
			minWidth: 100,
			maxWidth: 200,
			defaultValue: null,
			filter: { 
				operators: [ColumnFilterOperator.gt, ColumnFilterOperator.lt],
				defaultOperator: ColumnFilterOperator.gt 
			}
		},
    	columnValues: []
	},
	{
		key: 'epd_layer_thickness',
		label: 'Layer Thickness',
		default: false,
		visible: false,
		tooltip: 'Layer thickness of the product',
		columnProperties: { 
			type: ColumnType.numeric,
			minWidth: 100,
			maxWidth: 200,
			defaultValue: null,
			filter: { 
				operators: [ColumnFilterOperator.gt, ColumnFilterOperator.lt],
				defaultOperator: ColumnFilterOperator.gt 
			}
		},
    	columnValues: []
	},
	
	// Source information
	{
		key: 'epd_sourceName',
		label: 'Source',
		default: false,
		visible: false,
		tooltip: 'Name of the data source',
		columnProperties: { 
			type: ColumnType.string,
			minWidth: 100,
			maxWidth: 200,
			defaultValue: null,
			filter: {
				defaultOperator: ColumnFilterOperator.consists
			}
		},
    	columnValues: []
	},
	{
		key: 'epd_sourceUrl',
		label: 'Source URL',
		default: false,
		visible: false,
		tooltip: 'URL of the data source',
		columnProperties: { 
			type: ColumnType.string,
			minWidth: 100,
			maxWidth: 200,
			defaultValue: null,
			filter: {
				defaultOperator: ColumnFilterOperator.consists
			}
		},
    	columnValues: []
	},
	{
		key: 'epd_comment',
		label: 'Comment',
		default: false,
		visible: false,
		tooltip: 'Additional comments about the product',
		columnProperties: { 
			type: ColumnType.string,
			minWidth: 10,
			maxWidth: 20,
			defaultValue: null,
			filter: {
				defaultOperator: ColumnFilterOperator.consists 
			}
		},
    	columnValues: []
	},
	
	// Metadata
	{
		key: 'date_created',
		label: 'Created',
		default: false,
		visible: false,
		tooltip: 'Date the product was created in the system',
		columnProperties: { 
			type: ColumnType.date,
			minWidth: 10,
			maxWidth: 20,
			defaultValue: null,
			filter: { 
				operators: [ColumnFilterOperator.gt, ColumnFilterOperator.lt],
				defaultOperator: ColumnFilterOperator.gt 
			}
		},
    	columnValues: []
	},
	{
		key: 'date_updated',
		label: 'Updated',
		default: false,
		visible: false,
		tooltip: 'Date the product was last updated',
		columnProperties: { 
			type: ColumnType.date,
			minWidth: 10,
			maxWidth: 20,
			defaultValue: null,
			filter: { 
				operators: [ColumnFilterOperator.gt, ColumnFilterOperator.lt],
				defaultOperator: ColumnFilterOperator.gt 
			}
		},
    	columnValues: []
	},
	{
		key: 'user_created',
		label: 'Created By',
		default: false,
		visible: false,
		tooltip: 'User who created the product',
		columnProperties: { 
			type: ColumnType.string,
			minWidth: 10,
			maxWidth: 20,
			defaultValue: null,
			filter: {
				defaultOperator: ColumnFilterOperator.consists
			}
		},
    	columnValues: []
	},
	{
		key: 'user_updated',
		label: 'Updated By',
		default: false,
		visible: false,
		tooltip: 'User who last updated the product',
		columnProperties: { 
			type: ColumnType.string,
			minWidth: 10,
			maxWidth: 20,
			defaultValue: null,
			filter: {
				defaultOperator: ColumnFilterOperator.consists
			}
		},
    	columnValues: []
	}
];
export function getAllProductColumns(): ColumnDefinition[] { return productColumns };
// Helper function to get default product columns
export function getDefaultProductColumns(): ColumnDefinition[] {
  return productColumns.filter(col => col.default);
}

// Helper function to get a column definition by key
export function getProductColumnByKey(key: string): ColumnDefinition | undefined {
  return productColumns.find(col => col.key === key);
}

// Helper function to convert a product property value to a display value
export function formatProductValue(key: string, value: any): string {
  if (value === null || value === undefined) {
    return 'N/A';
  }
  
  // Format dates
  if (
    key === 'epd_publishedDate' ||
    key === 'epd_validUntil' ||
    key === 'date_created' ||
    key === 'date_updated'
  ) {
    try {
      return new Date(value).toLocaleDateString();
    } catch (e) {
      return String(value);
    }
  }
  
  // Format numeric values with appropriate precision
  if (
    key === 'epd_linear_density' ||
    key === 'epd_gross_density' ||
    key === 'epd_bulk_density' ||
    key === 'epd_grammage' ||
    key === 'epd_layer_thickness'
  ) {
    if (typeof value === 'number') {
      return value.toFixed(2);
    }
  }
  
  // Default string conversion
  return String(value);
}