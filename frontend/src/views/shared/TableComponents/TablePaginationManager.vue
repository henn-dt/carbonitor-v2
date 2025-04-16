<template>
    <div class="pagination-manager">
      <slot 
        :paginatedIndices="paginatedIndices" 
        :pagination="paginationInfo"
      ></slot>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, computed, watch, type PropType } from 'vue';
  
  export default defineComponent({
    name: 'TablePaginationManager',
    
    props: {
      // Row indices after filtering and sorting
      rowIndices: {
        type: Array as PropType<number[]>,
        required: true
      },
      
      // Page size
      pageSize: {
        type: Number,
        default: 10
      }
    },
    
    emits: ['page-changed'],
    
    setup(props, { emit }) {
      // Pagination state
      const currentPage = ref(1);
      
      // Reset to page 1 when data changes
      watch(() => props.rowIndices, () => {
        currentPage.value = 1;
      });
      
      // Calculate total pages
      const totalPages = computed(() => {
        return Math.max(1, Math.ceil(props.rowIndices.length / props.pageSize));
      });
      
      // Get paginated row indices
      const paginatedIndices = computed(() => {
        const start = (currentPage.value - 1) * props.pageSize;
        const end = start + props.pageSize;
        return props.rowIndices.slice(start, end);
      });
      
      // Go to a specific page
      function goToPage(page: number) {
        if (page < 1 || page > totalPages.value) return;
        currentPage.value = page;
        
        // Emit page change event
        emit('page-changed', {
          currentPage: currentPage.value,
          totalPages: totalPages.value,
          pageSize: props.pageSize,
          totalRows: props.rowIndices.length
        });
      }
      
      // Pagination info to expose via slot
      const paginationInfo = computed(() => ({
        currentPage: currentPage.value,
        totalPages: totalPages.value,
        pageSize: props.pageSize,
        totalRows: props.rowIndices.length,
        goToPage
      }));
      
      return {
        currentPage,
        totalPages,
        paginatedIndices,
        paginationInfo
      };
    }
  });
  </script>
  
  <style scoped>
  .pagination-manager {
    width: 100%;
  }
  </style>