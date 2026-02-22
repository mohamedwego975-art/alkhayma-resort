<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 py-8 px-4">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-2">
          My Account
        </h1>
        <p class="text-gray-600 dark:text-gray-400">
          Manage your bookings, loyalty points, and profile
        </p>
      </div>

      <!-- Tabs -->
      <div class="bg-white dark:bg-gray-900 rounded-2xl shadow-lg overflow-hidden">
        <!-- Tab Navigation -->
        <div class="border-b border-gray-200 dark:border-gray-700">
          <nav class="flex overflow-x-auto">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              class="px-6 py-4 text-sm font-medium whitespace-nowrap transition-colors relative"
              :class="activeTab === tab.id 
                ? 'text-ocean-deep-600 dark:text-ocean-deep-400' 
                : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'"
            >
              <span class="flex items-center gap-2">
                <span>{{ tab.icon }}</span>
                {{ tab.name }}
              </span>
              <div
                v-if="activeTab === tab.id"
                class="absolute bottom-0 left-0 right-0 h-0.5 bg-ocean-deep-500"
              ></div>
            </button>
          </nav>
        </div>

        <!-- Tab Content -->
        <div class="p-6 md:p-8">
          <!-- My Bookings Tab -->
          <div v-if="activeTab === 'bookings'">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-bold text-gray-900 dark:text-white">My Bookings</h2>
              <router-link to="/rooms" class="btn-primary text-sm">
                Book New Stay
              </router-link>
            </div>

            <!-- Loading State -->
            <div v-if="loadingBookings" class="space-y-4">
              <div v-for="i in 3" :key="i" class="animate-pulse bg-gray-100 dark:bg-gray-800 rounded-xl h-32"></div>
            </div>

            <!-- Empty State -->
            <div v-else-if="bookings.length === 0" class="text-center py-12">
              <div class="w-20 h-20 rounded-full bg-gray-100 dark:bg-gray-800 mx-auto mb-4 flex items-center justify-center text-4xl">
                📅
              </div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">No Bookings Yet</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">Start your vacation journey today!</p>
              <router-link to="/rooms" class="btn-primary">
                Explore Rooms
              </router-link>
            </div>

            <!-- Bookings List -->
            <div v-else class="space-y-4">
              <div
                v-for="booking in bookings"
                :key="booking.id"
                class="bg-gray-50 dark:bg-gray-800 rounded-xl p-6 hover:shadow-md transition-shadow"
              >
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div class="flex-1">
                    <div class="flex items-center gap-3 mb-2">
                      <span class="text-2xl">{{ getProductIcon(booking.product_type) }}</span>
                      <h3 class="font-bold text-gray-900 dark:text-white">Booking #{{ booking.id }}</h3>
                      <span
                        class="px-3 py-1 rounded-full text-xs font-bold"
                        :class="getStatusBadgeClass(booking.status)"
                      >
                        {{ booking.status }}
                      </span>
                    </div>
                    <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
                      {{ formatDate(booking.check_in) }} - {{ formatDate(booking.check_out) }}
                    </p>
                    <p class="text-sm text-gray-600 dark:text-gray-400">
                      {{ booking.guests }} {{ booking.guests === 1 ? 'guest' : 'guests' }} • ${{ booking.total_price }}
                    </p>
                  </div>
                  <div class="flex gap-2">
                    <router-link
                      :to="`/booking-confirmation/${booking.id}`"
                      class="btn-secondary text-sm"
                    >
                      View Details
                    </router-link>
                    <button
                      v-if="canCancel(booking)"
                      @click="cancelBooking(booking.id)"
                      :disabled="cancellingId === booking.id"
                      class="px-4 py-2 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                    >
                      {{ cancellingId === booking.id ? 'Cancelling...' : 'Cancel' }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Loyalty Points Tab -->
          <div v-if="activeTab === 'loyalty'">
            <!-- Points Summary -->
            <div class="grid md:grid-cols-3 gap-6 mb-8">
              <div class="bg-gradient-to-br from-sand-gold-100 to-sand-gold-50 dark:from-sand-gold-900/30 dark:to-sand-gold-800/20 rounded-xl p-6 text-center">
                <div class="text-4xl mb-2">⭐</div>
                <div class="text-3xl font-bold text-sand-gold-600">{{ loyaltyBalance }}</div>
                <div class="text-sm text-gray-600 dark:text-gray-400">Available Points</div>
              </div>
              <div class="bg-gradient-to-br from-ocean-deep-100 to-ocean-deep-50 dark:from-ocean-deep-900/30 dark:to-ocean-deep-800/20 rounded-xl p-6 text-center">
                <div class="text-4xl mb-2">🏆</div>
                <div class="text-2xl font-bold text-ocean-deep-600">{{ loyaltyTier }}</div>
                <div class="text-sm text-gray-600 dark:text-gray-400">Current Tier</div>
              </div>
              <div class="bg-gradient-to-br from-teal-glow-100 to-teal-glow-50 dark:from-teal-glow-900/30 dark:to-teal-glow-800/20 rounded-xl p-6 text-center">
                <div class="text-4xl mb-2">🎯</div>
                <div class="text-2xl font-bold text-teal-600">{{ pointsToNextTier }}</div>
                <div class="text-sm text-gray-600 dark:text-gray-400">Points to Next Tier</div>
              </div>
            </div>

            <!-- Tier Progress -->
            <div class="mb-8">
              <h3 class="font-bold text-gray-900 dark:text-white mb-4">Tier Progress</h3>
              <div class="bg-gray-100 dark:bg-gray-800 rounded-full h-4 mb-2">
                <div
                  class="h-full bg-gradient-to-r from-sand-gold-400 to-sand-gold-600 rounded-full transition-all"
                  :style="{ width: `${tierProgress}%` }"
                ></div>
              </div>
              <div class="flex justify-between text-sm text-gray-600 dark:text-gray-400">
                <span>{{ loyaltyTier }}</span>
                <span>{{ nextTier }}</span>
              </div>
            </div>

            <!-- Transaction History -->
            <div>
              <h3 class="font-bold text-gray-900 dark:text-white mb-4">Transaction History</h3>
              <div v-if="loadingLoyalty" class="animate-pulse space-y-3">
                <div v-for="i in 3" :key="i" class="h-16 bg-gray-100 dark:bg-gray-800 rounded-lg"></div>
              </div>
              <div v-else-if="loyaltyTransactions.length === 0" class="text-center py-8 text-gray-500">
                No transactions yet. Start earning points with your first booking!
              </div>
              <div v-else class="space-y-3">
                <div
                  v-for="transaction in loyaltyTransactions"
                  :key="transaction.id"
                  class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800 rounded-lg"
                >
                  <div class="flex items-center gap-3">
                    <div
                      class="w-10 h-10 rounded-full flex items-center justify-center text-lg"
                      :class="transaction.type === 'earn' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'"
                    >
                      {{ transaction.type === 'earn' ? '+' : '-' }}
                    </div>
                    <div>
                      <p class="font-medium text-gray-900 dark:text-white">{{ transaction.description }}</p>
                      <p class="text-sm text-gray-500">{{ formatDate(transaction.created_at) }}</p>
                    </div>
                  </div>
                  <span
                    class="font-bold"
                    :class="transaction.type === 'earn' ? 'text-green-600' : 'text-red-600'"
                  >
                    {{ transaction.type === 'earn' ? '+' : '-' }}{{ transaction.points }} pts
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Profile Tab -->
          <div v-if="activeTab === 'profile'">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">Profile Settings</h2>
            
            <form @submit.prevent="updateProfile" class="space-y-6 max-w-lg">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Full Name
                </label>
                <input
                  v-model="profileForm.full_name"
                  type="text"
                  class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 focus:border-ocean-deep-500 focus:ring-2 focus:ring-ocean-deep-200 dark:bg-gray-800 dark:text-white transition-all"
                >
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Email Address
                </label>
                <input
                  v-model="profileForm.email"
                  type="email"
                  disabled
                  class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700 text-gray-500 cursor-not-allowed"
                >
                <p class="text-xs text-gray-500 mt-1">Email cannot be changed</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Phone Number
                </label>
                <input
                  v-model="profileForm.phone"
                  type="tel"
                  class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 focus:border-ocean-deep-500 focus:ring-2 focus:ring-ocean-deep-200 dark:bg-gray-800 dark:text-white transition-all"
                >
              </div>

              <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
                <button
                  type="submit"
                  :disabled="updatingProfile"
                  class="btn-primary w-full"
                >
                  {{ updatingProfile ? 'Saving...' : 'Save Changes' }}
                </button>
              </div>
            </form>

            <!-- Change Password -->
            <div class="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
              <h3 class="font-bold text-gray-900 dark:text-white mb-4">Change Password</h3>
              <form @submit.prevent="changePassword" class="space-y-4 max-w-lg">
                <input
                  v-model="passwordForm.current"
                  type="password"
                  placeholder="Current Password"
                  class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 focus:border-ocean-deep-500 dark:bg-gray-800 dark:text-white"
                >
                <input
                  v-model="passwordForm.new"
                  type="password"
                  placeholder="New Password"
                  class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 focus:border-ocean-deep-500 dark:bg-gray-800 dark:text-white"
                >
                <input
                  v-model="passwordForm.confirm"
                  type="password"
                  placeholder="Confirm New Password"
                  class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 focus:border-ocean-deep-500 dark:bg-gray-800 dark:text-white"
                >
                <button
                  type="submit"
                  :disabled="changingPassword"
                  class="btn-secondary w-full"
                >
                  {{ changingPassword ? 'Changing...' : 'Change Password' }}
                </button>
              </form>
            </div>
          </div>

          <!-- Reviews Tab -->
          <div v-if="activeTab === 'reviews'">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">My Reviews</h2>
            
            <div v-if="loadingReviews" class="space-y-4">
              <div v-for="i in 2" :key="i" class="animate-pulse bg-gray-100 dark:bg-gray-800 rounded-xl h-40"></div>
            </div>

            <div v-else-if="reviews.length === 0" class="text-center py-12">
              <div class="text-6xl mb-4">⭐</div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">No Reviews Yet</h3>
              <p class="text-gray-600 dark:text-gray-400">Complete a stay and share your experience!</p>
            </div>

            <div v-else class="space-y-4">
              <div
                v-for="review in reviews"
                :key="review.id"
                class="bg-gray-50 dark:bg-gray-800 rounded-xl p-6"
              >
                <div class="flex items-start justify-between mb-4">
                  <div>
                    <h3 class="font-bold text-gray-900 dark:text-white">{{ review.product_name }}</h3>
                    <p class="text-sm text-gray-500">{{ formatDate(review.created_at) }}</p>
                  </div>
                  <div class="flex text-yellow-400">
                    <span v-for="n in 5" :key="n">
                      {{ n <= review.rating ? '★' : '☆' }}
                    </span>
                  </div>
                </div>
                <p class="text-gray-700 dark:text-gray-300">{{ review.comment }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { bookingApi, apiClient } from '@/api'
import type { Booking } from '@/api/bookings'
import type { Review } from '@/api/reviews'
import { useMeta } from '@/composables/useSEO'

// SEO
useMeta({
  title: 'My Account - الخيمة Beach Resort',
  description: 'Manage your bookings, loyalty points, profile, and reviews at الخيمة Beach Resort.',
  keywords: 'account, bookings, loyalty, profile, reviews'
})

const router = useRouter()
const authStore = useAuthStore()

// Tabs
const tabs = [
  { id: 'bookings', name: 'My Bookings', icon: '📅' },
  { id: 'loyalty', name: 'Loyalty Points', icon: '⭐' },
  { id: 'profile', name: 'Profile', icon: '👤' },
  { id: 'reviews', name: 'My Reviews', icon: '💬' }
]
const activeTab = ref('bookings')

// Bookings
const bookings = ref<Booking[]>([])
const loadingBookings = ref(true)
const cancellingId = ref<number | null>(null)

// Loyalty
const loyaltyBalance = ref(0)
const loyaltyTier = ref('Silver')
const nextTier = ref('Gold')
const pointsToNextTier = ref(500)
const loyaltyTransactions = ref<any[]>([])
const loadingLoyalty = ref(true)

// Profile
const profileForm = ref({
  full_name: authStore.user?.full_name || '',
  email: authStore.user?.email || '',
  phone: authStore.user?.phone || ''
})
const updatingProfile = ref(false)

// Password
const passwordForm = ref({
  current: '',
  new: '',
  confirm: ''
})
const changingPassword = ref(false)

// Reviews
const reviews = ref<Review[]>([])
const loadingReviews = ref(true)

const tierProgress = computed(() => {
  const current = loyaltyBalance.value
  const needed = pointsToNextTier.value + current
  return Math.min(100, (current / needed) * 100)
})

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push({ name: 'login', query: { redirect: '/account' } })
    return
  }

  await Promise.all([
    fetchBookings(),
    fetchLoyalty(),
    fetchReviews()
  ])
})

async function fetchBookings() {
  try {
    loadingBookings.value = true
    const response = await bookingApi.getMyBookings()
    bookings.value = response.data
  } catch (error) {
    console.error('Failed to fetch bookings:', error)
  } finally {
    loadingBookings.value = false
  }
}

async function fetchLoyalty() {
  try {
    loadingLoyalty.value = true
    const response = await apiClient.get('/loyalty/balance')
    loyaltyBalance.value = response.data.balance || 0
    loyaltyTier.value = response.data.tier || 'Silver'
    nextTier.value = response.data.next_tier || 'Gold'
    pointsToNextTier.value = response.data.points_to_next || 500
    
    const txResponse = await apiClient.get('/loyalty/transactions')
    loyaltyTransactions.value = txResponse.data || []
  } catch (error) {
    console.error('Failed to fetch loyalty:', error)
  } finally {
    loadingLoyalty.value = false
  }
}

async function fetchReviews() {
  try {
    loadingReviews.value = true
    // Assuming we can fetch user's reviews
    const response = await apiClient.get('/reviews/my-reviews')
    reviews.value = response.data || []
  } catch (error) {
    console.error('Failed to fetch reviews:', error)
  } finally {
    loadingReviews.value = false
  }
}

function getProductIcon(type?: string) {
  if (type === 'room') return '🏨'
  if (type === 'beach') return '🏖️'
  return '🎁'
}

function getStatusBadgeClass(status: string) {
  switch (status) {
    case 'confirmed':
    case 'completed':
      return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
    case 'pending':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
    case 'cancelled':
      return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-400'
  }
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

function canCancel(booking: Booking) {
  return booking.status === 'pending' || booking.status === 'confirmed'
}

async function cancelBooking(id: number) {
  if (!confirm('Are you sure you want to cancel this booking?')) return
  
  cancellingId.value = id
  try {
    await apiClient.post(`/bookings/${id}/cancel`)
    await fetchBookings()
    alert('Booking cancelled successfully')
  } catch (error) {
    console.error('Failed to cancel booking:', error)
    alert('Failed to cancel booking. Please try again.')
  } finally {
    cancellingId.value = null
  }
}

async function updateProfile() {
  updatingProfile.value = true
  try {
    await apiClient.patch('/auth/me', {
      full_name: profileForm.value.full_name,
      phone: profileForm.value.phone
    })
    await authStore.fetchUser()
    alert('Profile updated successfully')
  } catch (error) {
    console.error('Failed to update profile:', error)
    alert('Failed to update profile. Please try again.')
  } finally {
    updatingProfile.value = false
  }
}

async function changePassword() {
  if (passwordForm.value.new !== passwordForm.value.confirm) {
    alert('New passwords do not match')
    return
  }
  
  changingPassword.value = true
  try {
    await apiClient.post('/auth/change-password', {
      current_password: passwordForm.value.current,
      new_password: passwordForm.value.new
    })
    passwordForm.value = { current: '', new: '', confirm: '' }
    alert('Password changed successfully')
  } catch (error) {
    console.error('Failed to change password:', error)
    alert('Failed to change password. Please check your current password.')
  } finally {
    changingPassword.value = false
  }
}
</script>
