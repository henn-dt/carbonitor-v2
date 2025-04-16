<!-- frontend/src/App.vue -->
<script setup lang="ts">
import { RouterView } from 'vue-router'
import Modals from "@/views/shared/Modals/Modals.vue"
</script>

<template>
  <RouterView />
  <Modals />
</template>