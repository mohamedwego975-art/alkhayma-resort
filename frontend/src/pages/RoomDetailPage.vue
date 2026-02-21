<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4">
    <div class="max-w-7xl mx-auto">
      <router-link to="/rooms" class="text-blue-600 hover:text-blue-800 mb-4 inline-block">
        ← Back to Rooms
      </router-link>

      <div v-if="loading" class="animate-pulse">
        <div class="h-96 bg-gray-200 rounded-lg mb-8"></div>
        <div class="h-8 bg-gray-200 rounded mb-4"></div>
        <div class="h-4 bg-gray-200 rounded"></div>
      </div>

      <div v-else-if="room" class="grid lg:grid-cols-3 gap-8">
        <!-- Left: Image Gallery & Details -->
        <div class="lg:col-span-2">
          <!-- Image Gallery -->
          <div class="relative h-96 bg-gradient-to-r from-blue-400 to-blue-600 rounded-lg mb-6 flex items-center justify-center">
            <span class="text-white text-9xl">🏨</span>
          </div>

          <!-- Amenities -->
          <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h2 class="text-2xl font-bold mb-4">Amenities</h2>
            <div class="grid grid-cols-2 gap-4">
              <div class="flex items-center gap-2">
                <span>✓</span>
                <span>WiFi</span>
              </div>
              <div class="flex items-center gap-2">
                <span>✓</span>
                <span>Air Conditioning</span>
              </div>
              <div class="flex items-center gap-2">
                <span>✓</span>
                <span>TV</span>
              </div>
              <div class="flex items-center gap-2">
                <span>✓</span>
                <span>Mini Bar</span>
              </div>
            </div>
          </div>

          <!-- Description -->
          <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h2 class="text-2xl font-bold mb-4">Description</h2>
            <p class="text-gray-600">
              {{ room.description_en || 'Comfortable room with all modern amenities and stunning views.' }}
            </p>
          </div>

          <!-- Reviews -->
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-2xl font-bold mb-4">Guest Reviews</h2>
            <div class="space-y-4">
              <div v-for="i in 3" :key="i" class="border-b pb-4">
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-yellow-500">★★★★★</span>
                  <span class="font-bold">Guest {{ i }}</span>
                </div>
                <p class="text-gray-600">Great room with excellent service!</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Sticky Booking Widget -->
        <div class="lg:col-span-1">
          <div class="sticky top-4">
            <LiveCounter :product-id="room.id" class="mb-4" />
            
            <div class="bg-white rounded-lg shadow-lg p-6">
              <div class="mb-6">
                <h3 class="text-3xl font-bold text-blue-600 mb-2">
                  ${{ room.price_per_night }}
                  <span class="text-lg text-gray-600">/night</span>
                </h3>
                <p class="text-sm text-gray-600">Room {{ room.room_number }} • {{ room.room_type }}</p>
              </div>

              <form @submit.prevent="handleBooking" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium mb-1">Check-in</label>
                  <input 
                    v-model="checkIn" 
                    type="date" 
                    required
                    :min="today"
                    class="w-full px-3 py-2 border rounded"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium mb-1">Check-out</label>
                  <input 
                    v-model="checkOut" 
                    type="date" 
                    required
                    :min="checkIn || today"
                    class="w-full px-3 py-2 border rounded"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium mb-1">Guests</label>
                  <input 
                    v-model.number="guests" 
                    type="number" 
                    :max="room.capacity"
                    min="1"
                    required
                    class="w-full px-3 py-2 border rounded"
                  />
                </div>

                <!-- Add-ons -->
                <div class="border-t pt-4">
                  <h4 class="font-bold mb-2">Add-ons</h4>
                  <label class="flex items-center gap-2 mb-2">
                    <input v-model="addons.vipBeach" type="checkbox" />
                    <span>VIP Beach Access (+$65)</span>
                  </label>
                  <label class="flex items-center gap-2">
                    <input v-model="addons.dinner" type="checkbox" />
                    <span>Dinner Package (+$50)</span>
                  </label>
                </div>

                <!-- Price Preview -->
                <div class="border-t pt-4">
                  <div class="flex justify-between mb-2">
                    <span>{{ nights }} nights</span>
                    <span>${{ basePrice }}</span>
                  </div>
                  <div v-if="addons.vipBeach" class="flex justify-between mb-2 text-sm">
                    <span>VIP Beach</span>
                    <span>$65</span>
                  </div>
                  <div v-if="addons.dinner" class="flex justify-between mb-2 text-sm">
                    <span>Dinner</span>
                    <span>$50</span>
                  </div>
                  <div class="flex justify-between font-bold text-lg border-t pt-2">
                    <span>Total</span>
                    <span>${{ totalPrice }}</span>
                  </div>
                </div>

                <button 
                  type="submit"
                  :disabled="bookingLoading"
                  class="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  {{ bookingLoading ? 'Processing...' : 'Book Now' }}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>

    <SmartSuggestModal v-if="showSuggest" :product-id="1" trigger="scroll" @close="showSuggest = false" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { roomApi, bookingApi, type Room } from '@/api'
import { useAuthStore } from '@/stores/auth'
import LiveCounter from '@/components/smart/LiveCounter.vue'
import SmartSuggestModal from '@/components/smart/SmartSuggestModal.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const room = ref<Room | null>(null)
const loading = ref(true)
const checkIn = ref('')
const checkOut = ref('')
const guests = ref(1)
const addons = ref({ vipBeach: false, dinner: false })
const bookingLoading = ref(false)
const showSuggest = ref(false)

const today = computed(() => new Date().toISOString().split('T')[0])

const nights = computed(() => {
  if (!checkIn.value || !checkOut.value) return 0
  const diff = new Date(checkOut.value).getTime() - new Date(checkIn.value).getTime()
  return Math.ceil(diff / (1000 * 60 * 60 * 24))
})

const basePrice = computed(() => {
  if (!room.value) return 0
  return nights.value * room.value.price_per_night
})

const totalPrice = computed(() => {
  let total = basePrice.value
  if (addons.value.vipBeach) total += 65
  if (addons.value.dinner) total += 50
  return total
})

async function fetchRoom() {
  loading.value = true
  try {
    const response = await roomApi.getById(Number(route.params.slug))
    room.value = response.data
    guests.value = 1
  } catch (e) {
    console.error('Failed to fetch room:', e)
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
  try {
    await bookingApi.create({
      room_id: room.value.id,
      check_in: checkIn.value,
      check_out: checkOut.value,
      guests: guests.value,
      total_price: totalPrice.value
    })
    alert('Booking successful!')
    router.push('/account')
  } catch (e: any) {
    alert(e.response?.data?.error || 'Booking failed')
  } finally {
    bookingLoading.value = false
  }
}

onMounted(() => {
  fetchRoom()
  
  // Show suggest modal on scroll
  let scrolled = false
  window.addEventListener('scroll', () => {
    if (!scrolled && window.scrollY > 500) {
      scrolled = true
      setTimeout(() => {
        showSuggest.value = true
      }, 2000)
    }
  })
})
</script>
