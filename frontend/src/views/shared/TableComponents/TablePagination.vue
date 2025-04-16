<template>
  <div v-if="pagination.totalPages > 1" class="pagination">
    <button 
      @click="$emit('page-change', pagination.currentPage - 1)"
      :disabled="pagination.currentPage === 1"
      class="pagination-button prev"
    >
      Previous
    </button>
    
    <div class="pagination-numbers">
      <!-- First page -->
      <button 
        v-if="showFirst"
        @click="$emit('page-change', 1)"
        class="pagination-button"
        :class="{ 'active': pagination.currentPage === 1 }"
      >
        1
      </button>
      
      <!-- Ellipsis if needed -->
      <span v-if="showLeftEllipsis" class="ellipsis">...</span>
      
      <!-- Page numbers around current page -->
      <button 
        v-for="page in visiblePages" 
        :key="page"
        @click="$emit('page-change', page)"
        class="pagination-button"
        :class="{ 'active': pagination.currentPage === page }"
      >
        {{ page }}
      </button>
      
      <!-- Ellipsis if needed -->
      <span v-if="showRightEllipsis" class="ellipsis">...</span>
      
      <!-- Last page -->
      <button 
        v-if="showLast"
        @click="$emit('page-change', pagination.totalPages)"
        class="pagination-button"
        :class="{ 'active': pagination.currentPage === pagination.totalPages }"
      >
        {{ pagination.totalPages }}
      </button>
    </div>
    
    <button 
      @click="$emit('page-change', pagination.currentPage + 1)"
      :disabled="pagination.currentPage === pagination.totalPages"
      class="pagination-button next"
    >
      Next
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, type PropType } from 'vue';

interface PaginationInfo {
  currentPage: number;
  totalPages: number;
  pageSize: number;
  totalRows: number;
  goToPage: (page: number) => void;
}

export default defineComponent({
  name: 'TablePagination',
  
  props: {
    pagination: {
      type: Object as PropType<PaginationInfo>,
      required: true
    },
    maxVisiblePages: {
      type: Number,
      default: 5
    }
  },
  
  emits: ['page-change'],
  
  setup(props) {
    // Calculate which page numbers to show
    const visiblePages = computed(() => {
      const { currentPage, totalPages } = props.pagination;
      
      if (totalPages <= props.maxVisiblePages) {
        // Show all pages if there are few
        return Array.from({ length: totalPages }, (_, i) => i + 1);
      }
      
      // Show pages around the current page
      const halfVisible = Math.floor(props.maxVisiblePages / 2);
      let start = Math.max(currentPage - halfVisible, 2);
      let end = Math.min(start + props.maxVisiblePages - 3, totalPages - 1);
      
      // Adjust start if end is at max
      if (end === totalPages - 1) {
        start = Math.max(totalPages - props.maxVisiblePages + 2, 2);
      }
      
      return Array.from({ length: end - start + 1 }, (_, i) => start + i);
    });
    
    // Determine if we need to show first page button separately
    const showFirst = computed(() => {
      if (props.pagination.totalPages <= props.maxVisiblePages) return false;
      return true;
    });
    
    // Determine if we need to show last page button separately
    const showLast = computed(() => {
      if (props.pagination.totalPages <= props.maxVisiblePages) return false;
      return true;
    });
    
    // Determine if we need ellipsis on left side
    const showLeftEllipsis = computed(() => {
      if (!visiblePages.value.length) return false;
      return visiblePages.value[0] > 2;
    });
    
    // Determine if we need ellipsis on right side
    const showRightEllipsis = computed(() => {
      if (!visiblePages.value.length) return false;
      return visiblePages.value[visiblePages.value.length - 1] < props.pagination.totalPages - 1;
    });
    
    return {
      visiblePages,
      showFirst,
      showLast,
      showLeftEllipsis,
      showRightEllipsis
    };
  }
});
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 1rem;
  gap: 0.5rem;
}

.pagination-button {
  padding: 0.4rem 0.8rem;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  min-width: 2.5rem;
  text-align: center;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-button.active {
  background-color: #2196f3;
  color: white;
  border-color: #2196f3;
}

.pagination-button:hover:not(:disabled):not(.active) {
  background-color: #e0e0e0;
}

.pagination-numbers {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  margin: 0 0.5rem;
}

.ellipsis {
  margin: 0 0.25rem;
}

.pagination-button.prev,
.pagination-button.next {
  min-width: 5rem;
}
</style>