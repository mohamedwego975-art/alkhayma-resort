<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-4xl font-bold mb-8">Our Rooms</h1>

      <div v-if="loading" class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="i in 6" :key="i" class="bg-white rounded-lg overflow-hidden animate-pulse">
          <div class="h-64 bg-gray-200"></div>
          <div class="p-6">
            <div class="h-6 bg-gray-200 rounded mb-4"></div>
            <div class="h-4 bg-gray-200 rounded mb-2"></div>
            <div class="h-4 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>

      <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="room in rooms" :key="room.id" 
             class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition cursor-pointer"
             @click="$router.push(`/rooms/${room.id}`)">
          
          <!-- Image Swiper -->
          <div class="relative h-64 bg-gradient-to-r from-blue-400 to-blue-600 flex items-center justify-center">
            <span class="text-white text-8xl">🏨</span>
            <LiveCounter :product-id="room.id" class="absolute top-4 right-4" />
          </div>

          <div class="p-6">
            <h3 class="text-2xl font-bold mb-2">Room {{ room.room_number }}</h3>
            
            <div class="flex items-center gap-2 mb-4">
              <span class="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded">
                {{ room.room_type }}
              </span>
              <span class="text-gray-600 text-sm">
                👥 {{ room.capacity }} guests
              </span>
            </div>

            <div class="flex flex-wrap gap-2 mb-4">
              <span v-if="room.amenities" class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                WiFi
              </span>
              <span class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                AC
              </span>
              <span class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                TV
              </span>
            </div>

            <div class="flex justify-between items-center">
              <div>
                <span class="text-sm text-gray-600">from</span>
                <span class="text-2xl font-bold text-blue-600 ml-1">
                  ${{ room.price_per_night }}
                </span>
                <span class="text-sm text-gray-600">/night</span>
              </div>
              <button class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                View
              </button>
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
import LiveCounter from '@/components/smart/LiveCounter.vue'

const rooms = ref<Room[]>([])
const loading = ref(true)

async function fetchRooms() {
  loading.value = true
  try {
    const response = await roomApi.getAll()
    rooms.value = response.data
  } catch (e) {
    console.error('Failed to fetch rooms:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRooms()
})
</script>
