<template>
    <div class="control-group">
      <slot></slot>
    </div>
  </template>
  
  <style scoped>
  .control-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: .6em;
  }
  </style>