import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import { ColumnFilterOperator } from '@/views/shared/ColumnSelector/ColumnFilterOperator';
import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';
import { createCommandColumn } from '@/views/shared/ColumnSelector/CommandColumnFactory';
import BuildupsCommands from '@/views/user/components/buildups/BuildupsCommands.vue';
import { markRaw } from 'vue';

// Define product columns for the column selector
export const buildupColumns: ColumnDefinition[] = [
	// Command column
		  createCommandColumn({ 
			tooltip: 'Buildup actions', 
			key: 'buildup-actions',
			commandComponent: markRaw(BuildupsCommands)
		  }),
  // Core product information
	{
		key: 'id',
		label: 'ID',
		default: false,
		visible: false,
		tooltip: 'Buildup database ID',
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
		key: 'name',
		label: 'Name',
		default: true,
		visible: true,
		tooltip: 'Name of the buildup',
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
		key: 'unit',
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
		default: false,
		visible: true,
		tooltip: 'Current buildup status',
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
		key: 'comment',
		label: 'Comments',
		default: false,
		visible: false,
		tooltip: 'Additional comments',
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
		key: 'quantity',
		label: 'Quantity',
		default: false,
		visible: false,
		tooltip: 'Reference quantity of the buildup',
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
	},


];
export function getAllBuildupColumns(): ColumnDefinition[] { return buildupColumns };
// Helper function to get default product columns
export function getDefaultBuildupColumns(): ColumnDefinition[] {
  return buildupColumns.filter(col => col.default);
}

// Helper function to get a column definition by key
export function getBuildupColumnByKey(key: string): ColumnDefinition | undefined {
  return buildupColumns.find(col => col.key === key);
}

// Helper function to convert a product property value to a display value
export function formatProductValue(key: string, value: any): string {
  if (value === null || value === undefined) {
    return 'N/A';
  }
  
  // Format dates
  if (
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
    key === 'quantity'
  ) {
    if (typeof value === 'number') {
      return value.toFixed(2);
    }
  }
  
  // Default string conversion
  return String(value);
}