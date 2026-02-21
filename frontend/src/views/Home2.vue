<template>
  <div class="min-h-screen">
    <div class="bg-gradient-to-r from-blue-600 to-teal-600 text-white py-20">
      <div class="max-w-7xl mx-auto px-4 text-center">
        <h1 class="text-5xl font-bold mb-4">Welcome to الخيمة Beach Resort</h1>
        <p class="text-xl mb-8">Experience luxury by the Red Sea</p>
        <router-link to="/rooms" class="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100">
          Book Now
        </router-link>
      </div>
    </div>
    
    <div class="max-w-7xl mx-auto px-4 py-16">
      <h2 class="text-3xl font-bold mb-8">Featured Rooms</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="i in 3" :key="i" class="bg-white rounded-xl shadow-lg overflow-hidden">
          <img src="https://via.placeholder.com/400x300" alt="Room" class="w-full h-48 object-cover">
          <div class="p-4">
            <h3 class="font-bold text-lg mb-2">Deluxe Room {{ i }}</h3>
            <p class="text-gray-600 mb-4">From $100/night</p>
            <router-link to="/rooms" class="block text-center bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
              View Details
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>
