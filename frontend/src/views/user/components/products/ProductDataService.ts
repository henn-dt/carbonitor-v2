import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import type { ColumnValue } from '@/views/shared/ColumnSelector/ColumnValue';
import type { IProductWithCalculatedImpacts } from '@/types/epdx/IProductWithCalculatedImpacts';
import type { ImpactCategoryKey } from 'lcax';
import type { ICalculatedImpact } from '@/types/epdx/ICalculatedImpact';
import { SharedDataService } from '@/views/shared/DataTable/DataService';

/**
 * Service responsible for transforming product data for the ProductsView
 */
export class ProductDataService {
  /**
   * Transforms product data and selected columns into a flat table structure
   * with dynamic columns for indicators and lifecycle stages
   */
  static preparePrecalculatedTable(
    products: IProductWithCalculatedImpacts[],
    selectedProductColumns: ColumnDefinition[],
    selectedIndicators: ColumnDefinition[],
    selectedLifeCycles: ColumnDefinition[]
  ): ColumnDefinition[] {
    // Reset columnValues arrays for all columns
    SharedDataService.resetColumnValues(selectedProductColumns);
    // Pre-check if Reuse is included in the lifecycle stages
    const hasReuse = selectedLifeCycles.some(lc => lc.key === 'Reuse');
    const nonReuseCycles = hasReuse ? selectedLifeCycles.filter(lc => lc.key !== 'Reuse') : selectedLifeCycles;
    // Create dynamic columns with pre-initialized columnValues arrays
    const dynamicColumns = SharedDataService.createDynamicColumns(selectedIndicators, selectedLifeCycles);
    // Process all products in a single loop
    products.forEach((product, index) => {
      // Handle product columns
      selectedProductColumns.forEach(column => {
        column.columnValues?.push({rowId: index, value: product[column.key as keyof typeof product]});
      });
      // Handle indicator columns (optimization: avoid nested loops)
      selectedIndicators.forEach(indicator => {
        const indicatorKey = indicator.key as ImpactCategoryKey;
        // Process non-reuse lifecycle stages (total)
        if (nonReuseCycles.length > 0) {
          const totalKey = `${indicatorKey}-Total`;
          const totalValue = this.calculateTotal(product, indicatorKey, nonReuseCycles.map(lc => lc.key));
          // Find and update the corresponding column (using object lookup instead of find)
          const totalColumnIndex = dynamicColumns.findIndex(col => col.key === totalKey);
          if (totalColumnIndex !== -1 && dynamicColumns[totalColumnIndex].columnValues) {
            dynamicColumns[totalColumnIndex].columnValues!.push({rowId: index, value: totalValue});
          }
          nonReuseCycles.forEach(cycle => {
            const cycleValue = product.calculatedImpacts[indicatorKey][cycle.key as keyof ICalculatedImpact];
            const cycleKey = `${indicatorKey}-${cycle.key}`;
            const cycleColumnIndex = dynamicColumns.findIndex(col => col.key === cycleKey);
            dynamicColumns[cycleColumnIndex].columnValues!.push({rowId: index, value: cycleValue});
          });
          
        }
        // Process Reuse lifecycle stage if selected
        if (hasReuse) {
          const reuseKey = `${indicatorKey}-Reuse`;
          const reuseValue = this.getImpactValue(product, indicatorKey, 'Reuse');
          // Find and update the corresponding column (using object lookup instead of find)
          const reuseColumnIndex = dynamicColumns.findIndex(col => col.key === reuseKey);
          if (reuseColumnIndex !== -1 && dynamicColumns[reuseColumnIndex].columnValues) {
            dynamicColumns[reuseColumnIndex].columnValues!.push({rowId: index, value: reuseValue});
          }
        }
      });
    });
    return [...selectedProductColumns, ...dynamicColumns];
  }

  /**
   * Gets a specific impact value from a product
   */
  static getImpactValue(
    product: IProductWithCalculatedImpacts, 
    indicatorKey: ImpactCategoryKey, 
    lifecycleKey: string
  ): number | null {
    if (!product.calculatedImpacts || !product.calculatedImpacts[indicatorKey]) {
      return null;
    }
    // Use a set of valid lifecycle keys for cleaner validation
    if (['Production', 'Construction', 'Operation', 'Disassembly', 'Disposal', 'Reuse'].includes(lifecycleKey)) {
      const value = product.calculatedImpacts[indicatorKey][lifecycleKey as keyof ICalculatedImpact];
      return typeof value === 'number' ? value : null;
    }
    return null;
  }
  
  /**
   * Calculates total impact for multiple lifecycle stages
   */
  static calculateTotal(
    product: IProductWithCalculatedImpacts,
    indicatorKey: ImpactCategoryKey,
    lifecycleKeys: string[]
  ): number | null {
    if (!product.calculatedImpacts || !product.calculatedImpacts[indicatorKey]) {
      return null;
    }
    // Define valid lifecycle keys
    const validLifecycleKeys = new Set(['Production', 'Construction', 'Operation', 'Disassembly', 'Disposal', 'Reuse']);
    // Filter and reduce in one go
    const result = lifecycleKeys
      .filter(key => validLifecycleKeys.has(key))
      .reduce(
        (acc, lcKey) => {
          const value = product.calculatedImpacts[indicatorKey][lcKey as keyof ICalculatedImpact];
          if (typeof value === 'number') { acc.sum += value; acc.hasValue = true; }
          return acc;
        }, 
        { sum: 0, hasValue: false }
      );
    return result.hasValue ? result.sum : null;
  }
}