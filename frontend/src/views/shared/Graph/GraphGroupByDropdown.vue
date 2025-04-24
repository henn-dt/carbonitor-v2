<!-- frontend/src/views/shared/Graph/GraphGroupByDropdown.vue -->

<template>
    <div style="position: relative;">
      <ControlButton
        :title="`Group by: ${currentGroupByLabel}`"
        :class="toggleIcon"
        @click="toggleDropdown">
        <span :class="toggleIcon">
        </span>
      </ControlButton>
      <div
        v-if="dropdownOpen"
        class="dropdown-popup"
        @mousedown.prevent
      >
        <ul>
          <li
            v-for="opt in groupOptions"
            :key="opt.key"
            :class="{selected: sliceBy === opt.key}"
            @click="selectGroupBy(opt.key)"
          >
            <span :class="['icon', opt.icon]"></span> {{ opt.label }}
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
  import ControlButton from '@/views/shared/ControlButtons/ControlButton.vue'
  const props = defineProps<{sliceBy: string}>()
  const emit = defineEmits(['update:sliceBy'])
  
  const groupOptions = [
    { key: 'productName', label: 'Product', icon: 'product' },
    { key: 'mappingElement', label: 'Group', icon: 'group' }
  ]
  const currentGroupByLabel = computed(() => {
    const found = groupOptions.find(o => o.key === props.sliceBy)
    return found ? found.label : props.sliceBy
  })

  const toggleIcon = computed(() => {
    const found = groupOptions.find(o => o.key === props.sliceBy)
    return `icon ${found ? found.icon : 'unknown'}`
  })
  
  const dropdownOpen = ref(false)
  function toggleDropdown(e: MouseEvent) {
    dropdownOpen.value = !dropdownOpen.value
    e.stopPropagation()
  }
  function selectGroupBy(key: string) {
    emit('update:sliceBy', key)
    dropdownOpen.value = false
  }
  
  function handleClickOutside(e: MouseEvent) {
    if (!(e.target as Element)?.closest('.dropdown-popup')) {
      dropdownOpen.value = false
    }
  }
  onMounted(() => window.addEventListener('mousedown', handleClickOutside))
  onBeforeUnmount(() => window.removeEventListener('mousedown', handleClickOutside))
  </script>
  
  <style scoped>
  .dropdown-popup {
    position: absolute;
    left: 46px;
    top: 0;
    background: white;
    border-radius: 6px;
    box-shadow: 0 2px 14px 0 rgba(0,0,0,0.18);
    z-index: 99;
    min-width: 90px;
    padding: .5em 0;
  }
  .dropdown-popup ul {
    margin: 0; padding: 0; list-style: none;
  }
  .dropdown-popup li {
    padding: 0.5em 1em;
    cursor: pointer;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 0.7em;
  }
  .dropdown-popup li.selected, .dropdown-popup li:hover {
    background: #e6f0ff;
  }
  </style>