import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import type { IProductWithCalculatedImpacts } from '@/types/epdx/IProductWithCalculatedImpacts';
import type { ImpactCategoryKey } from 'lcax';
import { ProductDataService } from '@/views/user/components/products/ProductDataService';
import type { IBuildupWithProcessedProducts } from '@/types/epdx/IBuildupWithProcessedProducts';
import type { IBuildup } from '@/types/buildup/IBuildup';
import { SharedDataService } from '@/views/shared/DataTable/DataService';
import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';

/**
 * Service responsible for transforming buildup data for the BuildupsView
 */
export class BuildupDataService {
  /**
   * Transforms buildup data and selected columns into a flat table structure
   * with dynamic columns for indicators and lifecycle stages
   */
  static prepareBuildupTable(
    buildups: (IBuildup & IBuildupWithProcessedProducts)[],
    selectedBuildupColumns: ColumnDefinition[],
    selectedIndicators: ColumnDefinition[],
    selectedLifeCycles: ColumnDefinition[]
  ): ColumnDefinition[] {
    // Reset columnValues arrays for all columns
    SharedDataService.resetColumnValues(selectedBuildupColumns);
    
    // Create dynamic columns with pre-initialized columnValues arrays
    const dynamicColumns = SharedDataService.createDynamicColumns(
      selectedIndicators, 
      selectedLifeCycles
    );
    
    // Process all buildups in a single loop
    buildups.forEach((buildup, index) => {
      // Handle buildup columns
      selectedBuildupColumns.forEach(column => {
        column.columnValues?.push({
          rowId: index, 
          value: buildup[column.key as keyof typeof buildup]
        });
      });
      
      // Handle indicator columns for the buildup totals
      this.processBuildupIndicators(
        buildup,
        index,
        selectedIndicators,
        selectedLifeCycles,
        dynamicColumns
      );
    });
    
    return [...selectedBuildupColumns, ...dynamicColumns];
  }
  
  /**
   * Prepares a table showing products within a specific buildup
   */
  static prepareProductsInBuildupTable(
    buildup: IBuildup & IBuildupWithProcessedProducts,
    selectedIndicators: ColumnDefinition[],
    selectedLifeCycles: ColumnDefinition[]
  ): ColumnDefinition[] {
  // Canonical base columns
  const baseColumns: ColumnDefinition[] = [
    {
      key: 'mappingElement',
      label: 'Mapping Element',
      columnProperties: {type: ColumnType.string, minWidth: 10, maxWidth: 10, defaultValue: "mapping_id"},
      visible: true,
      columnValues: [],
      default: true
    },
    {
      key: 'productName',
      label: 'Product Name',
      columnProperties: {type: ColumnType.string, minWidth: 10, maxWidth: 10, defaultValue: ""},
      visible: true,
      columnValues: [],
      default: true
    },
    {
      key: 'productMapId',
      label: 'ID of product in buildup',
      columnProperties: {type: ColumnType.string, minWidth: 10, maxWidth: 10, defaultValue: "product_id"},
      visible: true,
      columnValues: [],
      default: true
    },
    {
      key: 'productId',
      label: 'Product ID',
      columnProperties: {type: ColumnType.numeric, minWidth: 10, maxWidth: 10, defaultValue: -1},
      visible: false,
      columnValues: [],
      default: false
    },
    {
      key: 'declaredUnit',
      label: 'Declared Unit',
      columnProperties: {type: ColumnType.string, minWidth: 10, maxWidth: 10, defaultValue: "unknown"},
      visible: false,
      columnValues: [],
      default: false
    },
    {
      key: 'normalizedQuantity',
      label: 'Normalized Quantity',
      columnProperties: {type: ColumnType.numeric, minWidth: 10, maxWidth: 10, defaultValue: 1},
      visible: true,
      columnValues: [],
      default: false
    },
    {
      key: 'quantity',
      label: 'Full Quantity',
      columnProperties: {type: ColumnType.numeric, minWidth: 10, maxWidth: 10, defaultValue: 1},
      visible: false,
      columnValues: [],
      default: false
    }
  ];

    // 2. Generate Indicator x Phase columns using helper
    const dynamicColumns = SharedDataService.createDynamicColumns(
      selectedIndicators,
      selectedLifeCycles
    );
    SharedDataService.resetColumnValues(dynamicColumns);

    // Iterate through mappings and products
    let rowIdx = 0;
    for (const [mappingName, products] of Object.entries(buildup.mappedProducts)) {
      for (const product of products) {
        const normalizedQuantity = buildup.quantity ? (product.quantity / buildup.quantity) : 0;

    // Base columns
    baseColumns.find(c => c.key === 'mappingElement')!.columnValues!.push({ rowId: rowIdx, value: mappingName });
    baseColumns.find(c => c.key === 'productName')!.columnValues!.push({ rowId: rowIdx, value: product.epd_name });
    baseColumns.find(c => c.key === 'declaredUnit')!.columnValues!.push({ rowId: rowIdx, value: product.epd_declaredUnit });
    baseColumns.find(c => c.key === 'productMapId')!.columnValues!.push({ rowId: rowIdx, value: product.elementMapId });
    baseColumns.find(c => c.key === 'productId')!.columnValues!.push({ rowId: rowIdx, value: product.id });
    baseColumns.find(c => c.key === 'normalizedQuantity')!.columnValues!.push({ rowId: rowIdx, value: normalizedQuantity });
    baseColumns.find(c => c.key === 'quantity')!.columnValues!.push({ rowId: rowIdx, value: product.quantity });

    // Indicators/phases: use your preferred helper
    this.processProductIndicatorsInBuildup(
      product,
      buildup.quantity,
      rowIdx,
      selectedIndicators,
      selectedLifeCycles,
      dynamicColumns
    );
    rowIdx++;
  }
}

  return [...baseColumns, ...dynamicColumns];
  }
    

  
  /**
   * Process indicators for a buildup by aggregating all product impacts
   */
  private static processBuildupIndicators(
    buildup: (IBuildup & IBuildupWithProcessedProducts),
    rowIndex: number,
    selectedIndicators: ColumnDefinition[],
    selectedLifeCycles: ColumnDefinition[],
    dynamicColumns: ColumnDefinition[]
  ): void {
    // Pre-check if Reuse is included in the lifecycle stages
    const hasReuse = selectedLifeCycles.some(lc => lc.key === 'Reuse');
    const nonReuseCycles = hasReuse 
      ? selectedLifeCycles.filter(lc => lc.key !== 'Reuse') 
      : selectedLifeCycles;
    
    selectedIndicators.forEach(indicator => {
      const indicatorKey = indicator.key as ImpactCategoryKey;
      
      // Calculate totals for each lifecycle stage by summing across all products
      // and normalizing by buildup quantity
      if (nonReuseCycles.length > 0) {
        // Process total across all non-reuse lifecycle stages
        const totalKey = `${indicatorKey}-Total`;
        let totalValue = 0;
        let hasValue = false;
        
        buildup.processedProducts.forEach(product => {
          const productTotalImpact = ProductDataService.calculateTotal(
            product, 
            indicatorKey, 
            nonReuseCycles.map(lc => lc.key)
          );
          
          if (productTotalImpact !== null) {
            // Normalize by product quantity relative to buildup quantity
            const normalizedImpact = (productTotalImpact) / buildup.quantity;
            totalValue += normalizedImpact;
            hasValue = true;
          }
        });
        
        // Find and update the corresponding column
        const totalColumnIndex = dynamicColumns.findIndex(col => col.key === totalKey);
        if (totalColumnIndex !== -1 && dynamicColumns[totalColumnIndex].columnValues) {
          dynamicColumns[totalColumnIndex].columnValues!.push({
            rowId: rowIndex, 
            value: hasValue ? totalValue : null
          });
        }
        
        // Process each individual lifecycle stage
        nonReuseCycles.forEach(cycle => {
          const cycleKey = `${indicatorKey}-${cycle.key}`;
          let cycleValue = 0;
          let hasCycleValue = false;
          
          buildup.processedProducts.forEach(product => {
            const productCycleImpact = ProductDataService.getImpactValue(
              product, 
              indicatorKey, 
              cycle.key
            );
            
            if (productCycleImpact !== null) {
              // Normalize by product quantity relative to buildup quantity
              const normalizedImpact = (productCycleImpact) / buildup.quantity;
              cycleValue += normalizedImpact;
              hasCycleValue = true;
            }
          });
          
          const cycleColumnIndex = dynamicColumns.findIndex(col => col.key === cycleKey);
          if (cycleColumnIndex !== -1 && dynamicColumns[cycleColumnIndex].columnValues) {
            dynamicColumns[cycleColumnIndex].columnValues!.push({
              rowId: rowIndex, 
              value: hasCycleValue ? cycleValue : null
            });
          }
        });
      }
      
      // Process Reuse lifecycle stage if selected
      if (hasReuse) {
        const reuseKey = `${indicatorKey}-Reuse`;
        let reuseValue = 0;
        let hasReuseValue = false;
        
        buildup.processedProducts.forEach(product => {
          const productReuseImpact = ProductDataService.getImpactValue(
            product, 
            indicatorKey, 
            'Reuse'
          );
          
          if (productReuseImpact !== null) {
            // Normalize by product quantity relative to buildup quantity
            const normalizedImpact = (productReuseImpact) / buildup.quantity;
            reuseValue += normalizedImpact;
            hasReuseValue = true;
          }
        });
        
        const reuseColumnIndex = dynamicColumns.findIndex(col => col.key === reuseKey);
        if (reuseColumnIndex !== -1 && dynamicColumns[reuseColumnIndex].columnValues) {
          dynamicColumns[reuseColumnIndex].columnValues!.push({
            rowId: rowIndex, 
            value: hasReuseValue ? reuseValue : null
          });
        }
      }
    });
  }
  
  /**
   * Process indicators for a single product within a buildup
   */
  private static processProductIndicatorsInBuildup(
    product: IProductWithCalculatedImpacts,
    buildupQuantity: number,
    rowIndex: number,
    selectedIndicators: ColumnDefinition[],
    selectedLifeCycles: ColumnDefinition[],
    dynamicColumns: ColumnDefinition[]
  ): void {
    // Pre-check if Reuse is included in the lifecycle stages
    const hasReuse = selectedLifeCycles.some(lc => lc.key === 'Reuse');
    const nonReuseCycles = hasReuse 
      ? selectedLifeCycles.filter(lc => lc.key !== 'Reuse') 
      : selectedLifeCycles;
    
    selectedIndicators.forEach(indicator => {
      const indicatorKey = indicator.key as ImpactCategoryKey;
      
      // Process non-reuse lifecycle stages
      if (nonReuseCycles.length > 0) {
        // Process total across all non-reuse lifecycle stages
        const totalKey = `${indicatorKey}-Total`;
        const productTotalImpact = ProductDataService.calculateTotal(
          product, 
          indicatorKey, 
          nonReuseCycles.map(lc => lc.key)
        );
        
        // Normalize by product quantity relative to buildup quantity
        let normalizedTotalImpact = null;
        if (productTotalImpact !== null) {
          normalizedTotalImpact = (productTotalImpact) / buildupQuantity;
        }
        
        // Find and update the corresponding column
        const totalColumnIndex = dynamicColumns.findIndex(col => col.key === totalKey);
        if (totalColumnIndex !== -1 && dynamicColumns[totalColumnIndex].columnValues) {
          dynamicColumns[totalColumnIndex].columnValues!.push({
            rowId: rowIndex, 
            value: normalizedTotalImpact
          });
        }
        
        // Process each individual lifecycle stage
        nonReuseCycles.forEach(cycle => {
          const cycleKey = `${indicatorKey}-${cycle.key}`;
          const productCycleImpact = ProductDataService.getImpactValue(
            product, 
            indicatorKey, 
            cycle.key
          );
          
          // Normalize by product quantity relative to buildup quantity
          let normalizedCycleImpact = null;
          if (productCycleImpact !== null) {
            normalizedCycleImpact = (productCycleImpact) / buildupQuantity;
          }
          
          const cycleColumnIndex = dynamicColumns.findIndex(col => col.key === cycleKey);
          if (cycleColumnIndex !== -1 && dynamicColumns[cycleColumnIndex].columnValues) {
            dynamicColumns[cycleColumnIndex].columnValues!.push({
              rowId: rowIndex, 
              value: normalizedCycleImpact
            });
          }
        });
      }
      
      // Process Reuse lifecycle stage if selected
      if (hasReuse) {
        const reuseKey = `${indicatorKey}-Reuse`;
        const productReuseImpact = ProductDataService.getImpactValue(
          product, 
          indicatorKey, 
          'Reuse'
        );
        
        // Normalize by product quantity relative to buildup quantity
        let normalizedReuseImpact = null;
        if (productReuseImpact !== null) {
          normalizedReuseImpact = (productReuseImpact) / buildupQuantity;
        }
        
        const reuseColumnIndex = dynamicColumns.findIndex(col => col.key === reuseKey);
        if (reuseColumnIndex !== -1 && dynamicColumns[reuseColumnIndex].columnValues) {
          dynamicColumns[reuseColumnIndex].columnValues!.push({
            rowId: rowIndex, 
            value: normalizedReuseImpact
          });
        }
      }
    });
  }
   /**
   * Helper method to get all available buildups columns
   */
   static getAllBuildupTableColumns(
    selectedBuildupColumns: ColumnDefinition[],
    selectedIndicators: ColumnDefinition[],
    selectedLifeCycles: ColumnDefinition[]
  ): ColumnDefinition[] {
    return [
      ...selectedBuildupColumns,
      ...SharedDataService.createDynamicColumns(selectedIndicators, selectedLifeCycles)
    ];
  }
}