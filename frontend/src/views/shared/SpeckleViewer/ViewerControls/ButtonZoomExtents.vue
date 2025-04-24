<!-- frontend/src/views/shared/SpeckleViewer/ViewerControls/ButtonZoomExtents.vue -->
<template>
    <ControlButton 
      :disabled="!viewerReady"
      @click="zoomToExtents"
      title="Zoom to extents"
    >
      <span class="icon zoom-extents"></span>
    </ControlButton>
  </template>
  
  <script setup lang="ts">

  import { CameraController } from '@speckle/viewer';
  import ControlButton from '@/views/shared/ControlButtons/ControlButton.vue'
  import { computed } from 'vue';
  
  const props = defineProps<{ viewer: any }>()
  const viewerReady = computed(() => !!props.viewer)
  console.log('ZoomExtentsButton viewer:', props.viewer)
  function zoomToExtents() {
    console.log('trying to zoom')
    if (!props.viewer) {
        console.log('viewer not ready')
        return; 
        }// double guard
        const cam = props.viewer.getExtension(CameraController) as CameraController
                if (cam?.setCameraView) {
        cam.setCameraView(undefined, undefined)
      } else if (props.viewer.setCameraView) {
        props.viewer.setCameraView()
      } else {
        console.warn('No suitable camera controller!', cam, props.viewer)
      }
      }
  </script>