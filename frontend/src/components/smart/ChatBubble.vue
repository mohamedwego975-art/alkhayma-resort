<template>
  <div class="fixed bottom-6 right-6 z-50">
    <button @click="isOpen = !isOpen" class="bg-ocean-deep-600 text-white w-16 h-16 rounded-full shadow-lg hover:bg-ocean-deep-700 flex items-center justify-center">
      <span class="text-2xl">💬</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const isOpen = ref(false)
</script>
