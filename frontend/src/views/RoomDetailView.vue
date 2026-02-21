<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow mb-8">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <router-link to="/rooms" class="text-blue-600 hover:text-blue-800">← Back to Rooms</router-link>
      </div>
    </nav>

    <div class="max-w-4xl mx-auto px-4">
      <div v-if="loading" class="text-center py-12">Loading...</div>

      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        {{ error }}
      </div>

      <div v-else-if="room" class="bg-white rounded-lg shadow overflow-hidden">
        <div class="h-96 bg-gradient-to-r from-blue-400 to-blue-600 flex items-center justify-center">
          <span class="text-white text-9xl">🏨</span>
        </div>

        <div class="p-8">
          <div class="flex justify-between items-start mb-6">
            <div>
              <h1 class="text-3xl font-bold mb-2">Room {{ room.room_number }}</h1>
              <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded">{{ room.room_type }}</span>
            </div>
            <div class="text-right">
              <div class="text-3xl font-bold text-blue-600">${{ room.price_per_night }}</div>
              <div class="text-gray-600">per night</div>
            </div>
          </div>

          <div class="mb-6">
            <h2 class="text-xl font-bold mb-2">Description</h2>
            <p class="text-gray-600">{{ room.description_en || 'Comfortable room with all amenities' }}</p>
          </div>

          <div class="mb-6">
            <h2 class="text-xl font-bold mb-2">Details</h2>
            <ul class="space-y-2 text-gray-600">
              <li>✓ Capacity: {{ room.capacity }} guests</li>
              <li>✓ Status: {{ room.status }}</li>
              <li v-if="room.amenities">✓ Amenities included</li>
            </ul>
          </div>

          <div class="border-t pt-6">
            <h2 class="text-xl font-bold mb-4">Book This Room</h2>
            <form @submit.prevent="handleBooking" class="space-y-4">
              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Check-in</label>
                  <input 
                    v-model="checkIn" 
                    type="date" 
                    required
                    :min="today"
                    class="w-full px-3 py-2 border border-gray-300 rounded"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Check-out</label>
                  <input 
                    v-model="checkOut" 
                    type="date" 
                    required
                    :min="checkIn || today"
                    class="w-full px-3 py-2 border border-gray-300 rounded"
                  />
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Number of Guests</label>
                <input 
                  v-model.number="guests" 
                  type="number" 
                  :max="room.capacity"
                  min="1"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded"
                />
              </div>

              <div v-if="bookingError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {{ bookingError }}
              </div>

              <button 
                type="submit"
                :disabled="bookingLoading"
                class="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {{ bookingLoading ? 'Processing...' : 'Confirm Booking' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { roomApi, bookingApi, type Room } from '@/api'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const room = ref<Room | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

const checkIn = ref('')
const checkOut = ref('')
const guests = ref(1)
const bookingLoading = ref(false)
const bookingError = ref<string | null>(null)

const today = computed(() => new Date().toISOString().split('T')[0])

async function fetchRoom() {
  loading.value = true
  error.value = null
  try {
    const response = await roomApi.getById(Number(route.params.id))
    room.value = response.data
    guests.value = 1
  } catch (e: any) {
    error.value = e.response?.data?.error || 'Failed to load room'
  } finally {
    loading.value = false
  }
}

async function handleBooking() {
  if (!authStore.isAuthenticated) {
    router.push({ name: 'login', query: { redirect: route.fullPath } })
    return
  }

  if (!room.value) return

  bookingLoading.value = true
  bookingError.value = null

  try {
    const nights = Math.ceil((new Date(checkOut.value).getTime() - new Date(checkIn.value).getTime()) / (1000 * 60 * 60 * 24))
    const totalPrice = nights * room.value.price_per_night

    await bookingApi.create({
      room_id: room.value.id,
      check_in: checkIn.value,
      check_out: checkOut.value,
      guests: guests.value,
      total_price: totalPrice
    })

    alert('Booking successful!')
    router.push('/account')
  } catch (e: any) {
    bookingError.value = e.response?.data?.error || 'Booking failed'
  } finally {
    bookingLoading.value = false
  }
}

onMounted(() => {
  fetchRoom()
})
</script>
