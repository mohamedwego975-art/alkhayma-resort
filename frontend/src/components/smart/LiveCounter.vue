<template>
  <div class="inline-flex items-center gap-2 px-4 py-2 bg-gray-50 rounded-full text-sm">
    <span class="relative flex h-2 w-2">
      <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75"></span>
      <span class="relative inline-flex rounded-full h-2 w-2 bg-teal-500"></span>
    </span>
    <span class="text-gray-700">5 guests viewing now</span>
  </div>
</template>

<script setup lang="ts">
defineProps<{ productId: number; showScarcity?: boolean }>()
</script>
