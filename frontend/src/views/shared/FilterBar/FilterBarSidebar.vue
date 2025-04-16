<!-- frontend/src/views/shared/FilterBar/SelectorBar.vue -->
<template>
    <div class="sidebar filter-element-container-vertical" 
         @mouseenter="showSelectors" 
         @mouseleave="hideIfAutoHide"
         :class="{ 'collapsed': isCollapsed }">
      <div class="filter-item" @click="toggleCollapse"
        :class="{ 'collapsed': isCollapsed }" >
        <slot name="title"></slot>
        <span v-if="isCollapsed" class="icon more"></span>
        <span v-if="!isCollapsed" class="icon close"></span>
      </div>
      
      <div class="filters-content" >
        <!-- Default slot for page-specific selectors -->
        <slot></slot>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  export default defineComponent({
    name: 'FilterBar',
    props: {
      autoHide: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        isCollapsed: false
      }
    },
    methods: {
      toggleCollapse() {
        this.isCollapsed = !this.isCollapsed;
      },
      showSelectors() {
        if (this.autoHide) {
          this.isCollapsed = false;
        }
      },
      hideIfAutoHide() {
        if (this.autoHide) {
          this.isCollapsed = true;
        }
      }
    }
  })
  </script>
  
  <style scoped>
  
  </style>