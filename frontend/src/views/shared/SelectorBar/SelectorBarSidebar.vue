<!-- frontend/src/views/shared/SelectorBar/SelectorBarSidebar.vue -->
<template>
    <div class="sidebar selectors-container-vertical" 
         @mouseenter="showSelectors" 
         @mouseleave="hideIfAutoHide"
         :class="{ 'collapsed': isCollapsed }">
      <div class="selector-item" @click="toggleCollapse"
        :class="{ 'collapsed': isCollapsed }" >
        <span v-if="isCollapsed" class="icon collapse-right"></span>
        <span v-if="!isCollapsed" class="icon collapse-left"></span>
      </div>
      
      <div class="selectors-content" >
        <!-- Default slot for page-specific selectors -->
        <slot></slot>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  export default defineComponent({
    name: 'SelectorBar',
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