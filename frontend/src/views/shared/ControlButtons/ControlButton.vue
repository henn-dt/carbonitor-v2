<template>
    <button
    type="button"
      class="control-button"
      :title="title"
      :class="iconClass"
      @click.stop="onClick"
    >
      <slot>
        <!-- fallback icon can go here if needed -->
      </slot>
    </button>
  </template>
  
  <script setup lang="ts">
  defineProps<{
    title?: string
    iconClass?: string
  }>()
  const emit = defineEmits(['click'])
function onClick(e: MouseEvent) {
  emit('click', e)
}
  </script>
  
  <style scoped>
  .control-button {
    background: none;
    border: none;
    width: 36px;
    height: 36px;
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background .17s;
  }
  .control-button:hover {
    background: rgba(25,120,212,0.11);
  }
  .icon {
    font-size: 1.45em;
  }
  </style>