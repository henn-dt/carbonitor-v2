import { computed, type Ref } from 'vue';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';

export function useLifecycleAware(
  props: {
    precalculatedTable: ColumnDefinition[]
  },
  yAxisColumn: Ref<string>
) {
  // Determine if the current column is a lifecycle-total column that can be broken down
  const showLifecycleOption = computed(() => {
    return yAxisColumn.value.includes('-Total');
  });

  // Get all associated lifecycle stage columns for a Total column
  const getLifecycleColumns = (totalColumnKey: string) => {
    if (!totalColumnKey.includes('-Total')) return [];
    
    const indicatorKey = totalColumnKey.split('-')[0];
    
    return props.precalculatedTable.filter(col => 
      col.key.startsWith(indicatorKey + '-') && 
      !col.key.endsWith('-Total') && 
      !col.key.endsWith('-Reuse')
    );
  };

  return {
    showLifecycleOption,
    getLifecycleColumns
  };
}