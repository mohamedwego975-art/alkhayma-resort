<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow mb-8">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <router-link to="/" class="text-blue-600 hover:text-blue-800">← Back to Home</router-link>
      </div>
    </nav>

    <div class="max-w-md mx-auto px-4">
      <h1 class="text-3xl font-bold mb-8 text-center">Book Your Stay</h1>
      <div class="bg-white rounded-lg shadow p-6">
        <p class="text-gray-600 text-center">Select a room to start booking</p>
        <router-link 
          to="/rooms" 
          class="block mt-4 text-center px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Browse Rooms
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Booking page - redirects to rooms
</script>
