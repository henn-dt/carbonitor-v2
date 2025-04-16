import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';
import { ColumnFilterOperator } from '@/views/shared/ColumnSelector/ColumnFilterOperator';


/**
 * Simple service responsible for shared transforming data operations for the entity views
 */
export class SharedDataService {   
  /**
   * Creates dynamic columns for indicator + lifecycle stage combinations
   */
  static createDynamicColumns(
    indicators: ColumnDefinition[],
    lifecycles: ColumnDefinition[]
  ): ColumnDefinition[] {
    // Pre-check if Reuse is included in the lifecycle stages
    const hasReuse = lifecycles.some(lc => lc.key === 'Reuse');
    const nonReuseCycles = hasReuse ? lifecycles.filter(lc => lc.key !== 'Reuse') : lifecycles;
    const columns: ColumnDefinition[] = [];
    // Create all dynamic columns in a single loop
    indicators.forEach(indicator => {
      // Add non-reuse lifecycle stages group (sum) if applicable
      if (nonReuseCycles.length > 0) {
        const label = nonReuseCycles.length === 1 ? `${indicator.label} (${nonReuseCycles[0].label})` : `${indicator.label} (Total)`;
        columns.push(this.getDynamicColumnDefinition(`${indicator.key}-Total`, label, `Sum of ${indicator.label} for selected lifecycle stages`, true));
        nonReuseCycles.forEach(cycle => {
          columns.push(this.getDynamicColumnDefinition(`${indicator.key}-${cycle.key}`, `${indicator.label}(${cycle.label})`, `${cycle.label} for selected lifecycle stages`));
        })
      }
      // Add Reuse lifecycle stage if selected
      if (hasReuse) {
        columns.push(this.getDynamicColumnDefinition(`${indicator.key}-Reuse`,`${indicator.label} (Reuse)`, `${indicator.label} for Reuse lifecycle stage`, true));
      }
    });
    return columns;
  }

  static getDynamicColumnDefinition(key: string, label: string, tooltip: string, visible: boolean = false): ColumnDefinition {
    return {
      key: key,
      label: label,
      default: false,
      visible: visible,
      tooltip: tooltip,
      columnProperties: {
        type: ColumnType.numeric,
        minWidth: 75,
        maxWidth: 200,
        defaultValue: 0,
        filter: { operators: [ColumnFilterOperator.gt, ColumnFilterOperator.lt], defaultOperator: ColumnFilterOperator.gt }
      },
      columnValues: []
    }
  }
  
  /**
   * Gets all columns for the table, including dynamic ones
   */
  static getAllTableColumns(
    selectedProductColumns: ColumnDefinition[],
    selectedIndicators: ColumnDefinition[],
    selectedLifeCycles: ColumnDefinition[]
  ): ColumnDefinition[] {
    return [
      ...selectedProductColumns,
      ...this.createDynamicColumns(selectedIndicators, selectedLifeCycles)
    ];
  }
  
  /**
   * Resets columnValues arrays for all columns
   */
  static resetColumnValues(columns: ColumnDefinition[]): void {
    columns.forEach(column => {
      column.columnValues = column.columnValues ? [] : [];
    });
  }
  
}