import { computed } from 'vue';
import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';

export function useColumnUtils(props: {
  precalculatedTable: ColumnDefinition[]
}) {
  // Computed properties for column options
  const availableColumns = computed<ColumnDefinition[]>(() => {
    return props.precalculatedTable.filter(col => col.visible==true);
  });

  const availableStringColumns = computed<ColumnDefinition[]>(() => {
    return props.precalculatedTable.filter(col => 
      col.columnProperties?.type === ColumnType.string || 
      col.columnProperties?.type === ColumnType.date
    ).filter(col => col.visible==true);
  });
  
  const availableNumericColumns = computed<ColumnDefinition[]>(() => {
    return props.precalculatedTable.filter(col => 
      col.columnProperties?.type === ColumnType.numeric
    ).filter(col => col.visible==true);
  });
  
  // Get unique units for the unit filter dropdown
  const availableUnits = computed(() => {
    const unitColumn = props.precalculatedTable.find(col => col.key === 'epd_declaredUnit');
    if (!unitColumn || !unitColumn.columnValues) return [];
    
    const uniqueUnits = new Set<string>();
    unitColumn.columnValues.forEach(value => {
      if (value.value && typeof value.value === 'string') {
        uniqueUnits.add(value.value);
      }
    });
    
    return Array.from(uniqueUnits);
  });

  return {
    availableColumns,
    availableStringColumns,
    availableNumericColumns, 
    availableUnits
  };
}