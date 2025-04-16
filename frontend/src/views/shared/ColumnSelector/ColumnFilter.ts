import type { ColumnFilterOperator } from "@/views/shared/ColumnSelector/ColumnFilterOperator";

export interface ColumnFilter {
    operators?: ColumnFilterOperator[];
    defaultOperator: ColumnFilterOperator;
}