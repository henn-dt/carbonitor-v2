<!-- frontend/src/views/user/components/buildups/speckleViewer/BuildupViewerDisplayModeDropdown.vue -->
<template>
  <div style="position: relative;">
    <ControlButton
      :title="`Graphic mode`"
      @click="toggleDropdown"
    >
      <span class="icon display_style"></span>
    </ControlButton>
    <div
      v-if="dropdownOpen"
      class="dropdown-popup"
      @mousedown.prevent
    >
      <ul>
        <li
          v-for="opt in graphicsOptions"
          :key="opt.key"
          :class="{selected: displayMode === opt.key}"
          @click="onSelectMode(opt.key)"
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
  import { applyDisplayMode, type GraphicMode } from '@/views/user/components/buildups/speckleViewer/displayMode'
  import { useColorStore } from "@/stores/colorStore"
  
  const props = defineProps<{
    viewer: any
    initialMode?: GraphicMode
  }>()
  const emit = defineEmits(['update:mode'])

  const colorStore = useColorStore()

  const displayMode = ref<GraphicMode>(props.initialMode ?? 'modelGroups')

  watch(
  [displayMode, () => props.viewer],
  async ([mode, viewer]) => {
    if (viewer && colorStore)
      await applyDisplayMode(viewer, mode, colorStore)
  },
  { immediate: true }
)

  const graphicsOptions = [
  { key: 'modelGroups', label: 'Model Groups', icon: 'group' },
  { key: 'mappedElements', label: 'Mapped Elements', icon: 'mapped' },
  { key: 'nonMappedElements', label: 'Non-mapped', icon: 'cancel_node' },
  { key: 'noOverrides', label: 'No Overrides', icon: 'default' },
] as const

  const dropdownOpen = ref(false)
  function toggleDropdown(e: MouseEvent) {
  dropdownOpen.value = !dropdownOpen.value
  e.stopPropagation()
}
function onSelectMode(mode: GraphicMode) {
  displayMode.value = mode
  dropdownOpen.value = false
}

// Close dropdown when clicking outside
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
  min-width: 140px;
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