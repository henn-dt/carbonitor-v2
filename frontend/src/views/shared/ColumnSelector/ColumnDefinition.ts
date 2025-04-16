// Using the SelectorItem interface from the ColumnSelector component

import type { ColumnProperties } from "@/views/shared/ColumnSelector/ColumnProperties";
import type { ColumnValue } from "@/views/shared/ColumnSelector/ColumnValue";

// for consistency and reusability
export interface ColumnDefinition {
    key: string;      // Property name in the data object
    label: string;    // Display label for the column header
    default: boolean; // Whether this column should be shown by default
    visible: boolean;
    tooltip?: string;
    columnProperties?: ColumnProperties;
    columnValues?: ColumnValue[];
    metadata?: Record<string, any>; // For custom data
}