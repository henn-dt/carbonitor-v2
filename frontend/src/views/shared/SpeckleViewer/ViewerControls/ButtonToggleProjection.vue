
<template>
    <ControlButton
      :title="projLabel"
      :class="iconClass"
      :disabled="!viewerReady"
      @click="toggleCamera"
    >
      <span :class="iconClass">
      </span>
    </ControlButton>
  </template>
  
  <script setup lang="ts">
  import { CameraController } from '@speckle/viewer';
  import ControlButton from '@/views/shared/ControlButtons/ControlButton.vue'
  import { computed, ref, watch } from 'vue';
  
  const props = defineProps<{ viewer: any }>()
  const viewerReady = computed(() => !!props.viewer)
  console.log('ProjectionToggleButton viewer:', props.viewer)
  const perspective = ref(true)
  
  function getCameraController(): CameraController | null {
  if (!props.viewer) return null
  // Your (working) getExtension method:
  // If you have the CameraController import in THIS file, do this:
  try {
    // import { CameraController } from '@speckle/viewer'
    const cam = props.viewer.getExtension(CameraController)
    return cam || null
  } catch { return null }
}
function updatePerspectiveState() {
    console.log("updatePerspectiveState called");
  const cam = getCameraController()
  if (!cam) return
  const current = cam.renderingCamera
  if (current.isPerspectiveCamera) perspective.value = true
  else if (current.isOrthographicCamera) perspective.value = false
  console.log(perspective.value)
}
function toggleCamera() {
    console.log("toggleCamera called");
  const cam = getCameraController()
  if (!cam) return
  const current = cam.renderingCamera
  if (current.isPerspectiveCamera) {
    cam.setOrthoCameraOn()
  } else if (current.isOrthographicCamera) {
    cam.setPerspectiveCameraOn()
  }
  updatePerspectiveState()
}

watch(() => props.viewer, () => {
    console.log("viewer watcher fired")
  updatePerspectiveState()
}, { immediate: true })

const iconClass = computed(() =>
  perspective.value ? 'icon perspective' : 'icon isometric'
)

const projLabel = computed(() =>
  perspective.value ? 'Switch to Isometric' : 'Switch to Perspective'
)
  
  </script>