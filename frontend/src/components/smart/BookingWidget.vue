<template>
  <div class="sticky top-20 bg-white rounded-xl shadow-xl p-6">
    <h3 class="text-xl font-bold mb-4">Book Your Stay</h3>
    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium mb-1">Check-in</label>
        <input type="date" class="w-full px-3 py-2 border rounded-lg">
      </div>
      <div>
        <label class="block text-sm font-medium mb-1">Check-out</label>
        <input type="date" class="w-full px-3 py-2 border rounded-lg">
      </div>
      <button class="btn-primary w-full">Book Now</button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ productId: number }>()
</script>
