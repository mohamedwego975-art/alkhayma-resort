<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow mb-8">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <router-link to="/" class="text-blue-600 hover:text-blue-800">← Back to Home</router-link>
      </div>
    </nav>

    <div class="max-w-4xl mx-auto px-4">
      <h1 class="text-3xl font-bold mb-8">My Account</h1>

      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h2 class="text-xl font-bold mb-4">Profile Information</h2>
        <div v-if="authStore.user" class="space-y-2">
          <p><strong>Name:</strong> {{ authStore.user.full_name }}</p>
          <p><strong>Email:</strong> {{ authStore.user.email }}</p>
          <p><strong>Phone:</strong> {{ authStore.user.phone || 'Not provided' }}</p>
          <p><strong>Role:</strong> {{ authStore.user.role }}</p>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold mb-4">My Bookings</h2>

        <div v-if="loading" class="text-center py-8 text-gray-600">Loading bookings...</div>

        <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {{ error }}
        </div>

        <div v-else-if="bookings.length === 0" class="text-center py-8 text-gray-600">
          No bookings yet. <router-link to="/rooms" class="text-blue-600 hover:underline">Browse rooms</router-link>
        </div>

        <div v-else class="space-y-4">
          <div 
            v-for="booking in bookings" 
            :key="booking.id"
            class="border rounded-lg p-4 hover:shadow-md transition"
          >
            <div class="flex justify-between items-start">
              <div>
                <h3 class="font-bold text-lg">Booking #{{ booking.id }}</h3>
                <p class="text-gray-600">Room ID: {{ booking.room_id }}</p>
                <p class="text-gray-600">Check-in: {{ formatDate(booking.check_in) }}</p>
                <p class="text-gray-600">Check-out: {{ formatDate(booking.check_out) }}</p>
                <p class="text-gray-600">Guests: {{ booking.guests }}</p>
              </div>
              <div class="text-right">
                <span class="px-3 py-1 rounded text-sm" :class="getStatusClass(booking.status)">
                  {{ booking.status }}
                </span>
                <p class="text-xl font-bold text-blue-600 mt-2">${{ booking.total_price }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { bookingApi, type Booking } from '@/api'

const authStore = useAuthStore()
const bookings = ref<Booking[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

async function fetchBookings() {
  loading.value = true
  error.value = null
  try {
    const response = await bookingApi.getMyBookings()
    bookings.value = response.data
  } catch (e: any) {
    error.value = e.response?.data?.error || 'Failed to load bookings'
  } finally {
    loading.value = false
  }
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString()
}

function getStatusClass(status: string) {
  const classes: Record<string, string> = {
    pending: 'bg-yellow-100 text-yellow-800',
    confirmed: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800',
    completed: 'bg-blue-100 text-blue-800'
  }
  return classes[status.toLowerCase()] || 'bg-gray-100 text-gray-800'
}

onMounted(() => {
  if (authStore.user) {
    fetchBookings()
  }
})
</script>
