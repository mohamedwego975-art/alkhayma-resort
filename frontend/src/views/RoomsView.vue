<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4">
      <h1 class="text-4xl font-bold mb-8">الغرف المتاحة</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition">
          <div class="h-64 bg-gradient-to-br from-blue-400 to-teal-400"></div>
          <div class="p-6">
            <h3 class="text-2xl font-bold mb-2">غرفة {{ i }}</h3>
            <p class="text-gray-600 mb-4">سعة: 2 ضيوف</p>
            <div class="flex items-center justify-between mb-4">
              <span class="text-2xl font-bold text-blue-600">$100</span>
              <span class="text-gray-500">/ ليلة</span>
            </div>
            <button class="w-full bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition font-semibold">
              احجز الآن
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>
