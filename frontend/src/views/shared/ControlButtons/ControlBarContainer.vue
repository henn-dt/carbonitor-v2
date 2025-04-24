<!-- frontend/src/views/shared/SpeckleViewer/ViewerControls/ControlBarContainer.vue -->

<template>
    <div class="control-bar-container">
      <slot></slot>
    </div>
  </template>
  
  <style scoped>
  .control-bar-container {
    position: absolute;
    top: 30px;
    left: 5px;
    z-index: 5;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    background: rgba(255,255,255,0.86);
    border-radius: 8px;
    padding: .5em .4em;
    box-shadow: 0 2px 14px 0 rgba(0,0,0,0.14);
    min-width: 45px;
    user-select: none;
    pointer-events: auto;
  }
  </style>