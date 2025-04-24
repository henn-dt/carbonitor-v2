<!-- frontend/src/views/user/components/buildups/speckleViewer/BuildupControlBar.vue -->
<template>
    <ControlBarContainer>
      <ControlGroup>
        <ButtonZoomExtents :viewer="viewer"  />
        <ButtonToggleProjection :viewer="viewer" />
      </ControlGroup>
      <ControlGroup>
        <DisplayModeDropdown :viewer="viewer" />
      </ControlGroup>
    </ControlBarContainer>
  </template>
  
  <script setup lang="ts">
  import ControlBarContainer from '@/views/shared/ControlButtons/ControlBarContainer.vue';
  import ControlGroup from '@/views/shared/ControlButtons/ControlGroup.vue';
  import ButtonToggleProjection from '@/views/shared/SpeckleViewer/ViewerControls/ButtonToggleProjection.vue';
  import ButtonZoomExtents from '@/views/shared/SpeckleViewer/ViewerControls/ButtonZoomExtents.vue';
  import DisplayModeDropdown from '@/views/user/components/buildups/speckleViewer/DisplayModeDropdown.vue';
  
  const props = defineProps<{ viewer: any }>()

  console.log('BuildupControlBar INIT', props.viewer)
  </script>