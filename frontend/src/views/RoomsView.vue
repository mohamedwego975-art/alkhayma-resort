<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow mb-8">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <router-link to="/" class="text-blue-600 hover:text-blue-800">← Back to Home</router-link>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4">
      <h1 class="text-4xl font-bold mb-8">Available Rooms</h1>

      <div v-if="loading" class="text-center py-12">
        <div class="text-gray-600">Loading rooms...</div>
      </div>

      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
        {{ error }}
      </div>

      <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="room in rooms" 
          :key="room.id"
          class="bg-white rounded-lg shadow overflow-hidden hover:shadow-lg transition"
        >
          <div class="h-48 bg-gradient-to-r from-blue-400 to-blue-600 flex items-center justify-center">
            <span class="text-white text-6xl">🏨</span>
          </div>
          <div class="p-6">
            <div class="flex justify-between items-start mb-2">
              <h3 class="text-xl font-bold">Room {{ room.room_number }}</h3>
              <span class="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded">
                {{ room.room_type }}
              </span>
            </div>
            <p class="text-gray-600 mb-4">{{ room.description_en || 'Comfortable room with amenities' }}</p>
            <div class="flex justify-between items-center">
              <div>
                <span class="text-2xl font-bold text-blue-600">${{ room.price_per_night }}</span>
                <span class="text-gray-600">/night</span>
              </div>
              <router-link 
                :to="`/rooms/${room.id}`"
                class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Book Now
              </router-link>
            </div>
            <div class="mt-4 text-sm text-gray-600">
              Capacity: {{ room.capacity }} guests
            </div>
          </div>
        </div>
      </div>

      <div v-if="!loading && rooms.length === 0" class="text-center py-12 text-gray-600">
        No rooms available at the moment.
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { roomApi, type Room } from '@/api'

const rooms = ref<Room[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

async function fetchRooms() {
  loading.value = true
  error.value = null
  try {
    const response = await roomApi.getAll()
    rooms.value = response.data
  } catch (e: any) {
    error.value = e.response?.data?.error || 'Failed to load rooms'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRooms()
})
</script>
