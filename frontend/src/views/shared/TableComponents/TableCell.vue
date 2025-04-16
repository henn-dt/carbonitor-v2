<template>
  <td 
    :class="{ 
      'numeric': column.columnProperties?.type === 'numeric',
      'date': column.columnProperties?.type === 'date',
      'string': column.columnProperties?.type === 'string' || !column.columnProperties?.type,
      'command': column.columnProperties?.type === 'command'
    }"
    >
    <template v-if="column.columnProperties?.type === 'command'">
      <!-- If a command component is defined in metadata, use it -->
      <component 
        v-if="column.metadata?.commandComponent"
        :is="column.metadata.commandComponent"
        :rowIndex="rowIndex"
      />
      <!-- Fallback to slot if no component is defined -->
      <slot v-else name="command-cell" :row-index="rowIndex"></slot>
    </template>
    <template v-else>
      {{ formattedValue }}
    </template>
  </td>
</template>

<script lang="ts">
import { defineComponent, computed, type PropType } from 'vue';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';


export default defineComponent({
  name: 'TableCell',

  
  props: {
    column: {
      type: Object as PropType<ColumnDefinition>,
      required: true
    },
    rowIndex: {
      type: Number,
      required: true
    },
  },
  
  emits: ['command-executed'],
  
  setup(props, {emit}) {
    // Get cell value from column
    const cellValue = computed(() => {
      return props.column.columnValues?.[props.rowIndex]?.value;
    });
    
    // Format cell value based on column type
    const formattedValue = computed(() => {
      const value = cellValue.value;
      const type = props.column.columnProperties?.type;
      
      if (value === null || value === undefined) return '';
      
      switch (type) {
        case ColumnType.numeric:
          return typeof value === 'number' 
            ? value.toLocaleString(undefined, { maximumFractionDigits: 2 })
            : String(value);
          
        case ColumnType.date:
          try {
            const date = new Date(value);
            return date.toLocaleDateString();
          } catch (e) {
            return String(value);
          }
          
        default:
          return String(value);
      }
    });


 
    
    return {
      cellValue,
      formattedValue,
    };
  }
});
</script>

<style scoped>
td {
  padding: 0.75rem;
  border: 1px solid #ddd;
  text-align: left;
}

.numeric {
  text-align: right;
}

.date {
  text-align: center;
}

.string {
  text-align: left;
}
</style>