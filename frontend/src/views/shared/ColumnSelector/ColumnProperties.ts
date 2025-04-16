import type { ColumnFilter } from "@/views/shared/ColumnSelector/ColumnFilter";
import type { ColumnType } from "@/views/shared/ColumnSelector/ColumnType";

export interface ColumnProperties {
    type: ColumnType | null;
    minWidth: number; //in px
    maxWidth: number; //in px
    defaultValue: number | string | Date | null;
    filter?: ColumnFilter;
}