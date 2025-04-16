<template>
    <div class="selection-manager">
      <slot 
        :selectedIndices="selectedIndices" 
        :selectionManager="selectionManager"
      ></slot>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, computed, watchEffect, type PropType } from 'vue';
  
  export default defineComponent({
    name: 'TableSelectionManager',
    
    props: {
      // Row indices after filtering, sorting, and pagination
      rowIndices: {
        type: Array as PropType<number[]>,
        required: true
      }
    },
    
    emits: ['selection-changed'],
    
    setup(props, { emit }) {
      // Selection state
      const selectedIndices = ref<number[]>([]);
      
      // Check if all visible rows are selected
      const isAllSelected = computed(() => {
        if (props.rowIndices.length === 0) return false;
        return props.rowIndices.every(index => selectedIndices.value.includes(index));
      });
      
      // Toggle selection for a specific row
      function toggleRowSelection(rowIndex: number) {
        if (selectedIndices.value.includes(rowIndex)) {
          selectedIndices.value = selectedIndices.value.filter(index => index !== rowIndex);
          emit('selection-changed', selectedIndices.value);
        } else {
          selectedIndices.value.push(rowIndex);
          emit('selection-changed', selectedIndices.value);
        }
      }
      
      // Toggle selection for all visible rows
      function toggleSelectAll() {
        if (isAllSelected.value) {
          // Deselect all visible rows
          selectedIndices.value = selectedIndices.value.filter(
            index => !props.rowIndices.includes(index)
          );
          emit('selection-changed', selectedIndices.value);
        } else {
          // Select all visible rows
          const newSelection = new Set([...selectedIndices.value, ...props.rowIndices]);
          selectedIndices.value = Array.from(newSelection);
          emit('selection-changed', selectedIndices.value);
        }
      }

            // Method to update selection from outside
      function setSelection(newSelection: number[]) {
        // Update only if different to prevent loops
        if (!arraysEqual(selectedIndices.value, newSelection)) {
          selectedIndices.value = [...newSelection];
        }
      }

      // Helper to compare arrays
      const arraysEqual = (a: number[], b: number[]) => {
        if (a.length !== b.length) return false;
        const sortedA = [...a].sort();
        const sortedB = [...b].sort();
        return sortedA.every((val, idx) => val === sortedB[idx]);
      };

      // Selection manager to expose via slot
      const selectionManager = computed(() => ({
        isAllSelected: isAllSelected.value,
        toggleRowSelection,
        toggleSelectAll,
        setSelection
      }));
      
      return {
        selectedIndices,
        selectionManager
      };
    }
  });
  </script>
  
  <style scoped>
  .selection-manager {
    width: 100%;
  }
  </style>