<template>
  <div class="min-h-screen bg-white dark:bg-gray-950">
    <!-- Header Section -->
    <div class="relative bg-gradient-to-r from-ocean-deep-900 via-ocean-deep-700 to-teal-glow-600 py-20 px-4">
      <div class="max-w-7xl mx-auto text-center">
        <span class="inline-block px-4 py-2 mb-4 text-sm font-medium text-white bg-white/10 backdrop-blur-md rounded-full border border-white/20">
          🏖️ Exclusive Beach Access
        </span>
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-4">
          Beach Access Packages
        </h1>
        <p class="text-xl text-white/90 max-w-2xl mx-auto">
          Choose between our VIP Premium experience or Standard Beach Access
        </p>
      </div>
    </div>

    <!-- VIP vs Normal Cards -->
    <section class="py-16 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="grid md:grid-cols-2 gap-8 mb-12">
          <!-- VIP Card -->
          <div class="relative group bg-white dark:bg-gray-900 rounded-2xl shadow-xl overflow-hidden border-4 border-sand-gold-500 hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
            <!-- VIP Badge -->
            <div class="absolute top-4 right-4 z-10">
              <span class="px-4 py-2 bg-gradient-to-r from-sand-gold-500 to-sand-gold-600 text-white font-bold rounded-full shadow-lg">
                👑 VIP
              </span>
            </div>

            <div class="h-64 bg-gradient-to-r from-sand-gold-400 to-sand-gold-600 flex items-center justify-center relative overflow-hidden">
              <!-- Decorative pattern -->
              <div class="absolute inset-0 opacity-20">
                <div class="absolute inset-0" style="background-image: radial-gradient(circle, #fff 1px, transparent 1px); background-size: 20px 20px;"></div>
              </div>
              <span class="text-white text-9xl relative z-10">🍹</span>
            </div>

            <div class="p-8">
              <div class="mb-4">
                <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">VIP Beach Access</h2>
                <p class="text-gray-600 dark:text-gray-400">Exclusive beach experience with premium amenities</p>
              </div>

              <!-- Features -->
              <ul class="space-y-3 mb-8">
                <li class="flex items-center gap-3 text-gray-700 dark:text-gray-300">
                  <span class="w-6 h-6 rounded-full bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400 flex items-center justify-center text-sm font-bold">✓</span>
                  <span>Private Cabana with stunning sea views</span>
                </li>
                <li class="flex items-center gap-3 text-gray-700 dark:text-gray-300">
                  <span class="w-6 h-6 rounded-full bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400 flex items-center justify-center text-sm font-bold">✓</span>
                  <span>Dedicated Waiter Service all day</span>
                </li>
                <li class="flex items-center gap-3 text-gray-700 dark:text-gray-300">
                  <span class="w-6 h-6 rounded-full bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400 flex items-center justify-center text-sm font-bold">✓</span>
                  <span>Premium Sunbeds & Lounge chairs</span>
                </li>
                <li class="flex items-center gap-3 text-gray-700 dark:text-gray-300">
                  <span class="w-6 h-6 rounded-full bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400 flex items-center justify-center text-sm font-bold">✓</span>
                  <span>Complimentary Drinks & Snacks</span>
                </li>
                <li class="flex items-center gap-3 text-gray-700 dark:text-gray-300">
                  <span class="w-6 h-6 rounded-full bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400 flex items-center justify-center text-sm font-bold">✓</span>
                  <span>Priority Access & Private Entrance</span>
                </li>
                <li class="flex items-center gap-3 text-gray-700 dark:text-gray-300">
                  <span class="w-6 h-6 rounded-full bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400 flex items-center justify-center text-sm font-bold">✓</span>
                  <span>Beach Towels & Lockers included</span>
                </li>
              </ul>

              <!-- Price & CTA -->
              <div class="flex items-center justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
                <div>
                  <span class="text-4xl font-bold text-sand-gold-600">$150</span>
                  <span class="text-gray-500 dark:text-gray-400 ml-1">/day</span>
                </div>
                <button class="btn-primary px-8 py-3 text-lg bg-sand-gold-500 hover:bg-sand-gold-600 text-white font-bold rounded-full shadow-lg hover:shadow-xl transition-all">
                  Book VIP
                </button>
              </div>
            </div>
          </div>

          <!-- Standard Card -->
          <div class="relative group bg-white dark:bg-gray-900 rounded-2xl shadow-xl overflow-hidden border-4 border-ocean-deep-500 hover:shadow-2xl transition-all duration-300 hover:-translate-y-2">
            <!-- Popular Badge -->
            <div class="absolute top-4 right-4 z-10">
              <span class="px-4 py-2 bg-gradient-to-r from-ocean-deep-500 to-teal-glow-500 text-white font-bold rounded-full shadow-lg">
                🔥 Popular
              </span>
            </div>

            <div class="h-64 bg-gradient-to-r from-ocean-deep-400 to-ocean-deep-600 flex items-center justify-center relative overflow-hidden">
              <!-- Decorative pattern -->
              <div class="absolute inset-0 opacity-20">
                <div class="absolute inset-0" style="background-image: radial-gradient(circle, #fff 1px, transparent 1px); background-size: 20px 20px;"></div>
              </div>
              <span class="text-white text-9xl relative z-10">🏖️</span>
            </div>

            <div class="p-8">
              <div class="mb-4">
                <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">Standard Beach</h2>
                <p class="text-gray-600 dark:text-gray-400">Enjoy our beautiful beach with standard amenities</p>
              </div>

              <!-- Features -->
              <ul class="space-y-3 mb-8">
                <li class="flex items-center gap-3 text-gray-700 dark:text-gray-300">
                  <span class="w-6 h-6 rounded-full bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400 flex items-center justify-center text-sm font-bold">✓</span>
                  <span>Full Beach Access</span>
                </li>
                <li class="flex items-center gap-3 text-gray-700 dark:text-gray-300">
                  <span class="w-6 h-6 rounded-full bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400 flex items-center justify-center text-sm font-bold">✓</span>
                  <span>Standard Sunbeds & Umbrellas</span>
                </li>
                <li class="flex items-center gap-3 text-gray-700 dark:text-gray-300">
                  <span class="w-6 h-6 rounded-full bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400 flex items-center justify-center text-sm font-bold">✓</span>
                  <span>Shower & Changing Facilities</span>
                </li>
                <li class="flex items-center gap-3 text-gray-700 dark:text-gray-300">
                  <span class="w-6 h-6 rounded-full bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400 flex items-center justify-center text-sm font-bold">✓</span>
                  <span>Access to Beach Bar & Restaurant</span>
                </li>
                <li class="flex items-center gap-3 text-gray-700 dark:text-gray-300">
                  <span class="w-6 h-6 rounded-full bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400 flex items-center justify-center text-sm font-bold">✓</span>
                  <span>Safe Swimming Area</span>
                </li>
                <li class="flex items-center gap-3 text-gray-500 dark:text-gray-500">
                  <span class="w-6 h-6 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-500 flex items-center justify-center text-sm">×</span>
                  <span class="line-through">Private Cabana (upgrade available)</span>
                </li>
              </ul>

              <!-- Price & CTA -->
              <div class="flex items-center justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
                <div>
                  <span class="text-4xl font-bold text-ocean-deep-600">$50</span>
                  <span class="text-gray-500 dark:text-gray-400 ml-1">/day</span>
                </div>
                <button class="btn-primary px-8 py-3 text-lg font-bold rounded-full shadow-lg hover:shadow-xl transition-all">
                  Book Now
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Activities Add-ons -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-gray-900">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-12">
          <span class="badge badge-primary mb-4">Add-ons</span>
          <h2 class="heading-display text-4xl md:text-5xl text-gray-900 dark:text-white mb-4">
            Water Activities
          </h2>
          <p class="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Enhance your beach experience with exciting water activities
          </p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div v-for="activity in activities" :key="activity.name"
               class="bg-white dark:bg-gray-800 rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 group">
            <div class="h-48 bg-gradient-to-r from-teal-glow-400 to-ocean-deep-500 flex items-center justify-center relative overflow-hidden">
              <div class="absolute inset-0 bg-black/10 group-hover:bg-black/0 transition-colors"></div>
              <span class="text-white text-7xl relative z-10 group-hover:scale-110 transition-transform">{{ activity.icon }}</span>
            </div>
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">{{ activity.name }}</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">{{ activity.description }}</p>
              <div class="flex justify-between items-center">
                <div>
                  <span class="text-2xl font-bold gradient-text">${{ activity.price }}</span>
                  <span class="text-gray-500 dark:text-gray-400 text-sm ml-1">/person</span>
                </div>
                <button class="btn-primary text-sm px-6 py-2">
                  Add to Booking
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Info Banner -->
    <section class="py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto">
        <div class="bg-gradient-to-r from-ocean-deep-500 to-teal-glow-500 rounded-2xl p-8 text-white text-center">
          <h3 class="text-2xl font-bold mb-4">Need a Custom Package?</h3>
          <p class="text-white/90 mb-6">
            Planning a group event or special occasion? Contact us for customized beach packages tailored to your needs.
          </p>
          <button class="bg-white text-ocean-deep-600 px-8 py-3 rounded-full font-bold hover:bg-white/90 transition-all">
            Contact Our Team
          </button>
        </div>
      </div>
    </section>

    <SmartSuggestModal v-if="showSuggest" :product-id="1" trigger="idle" @close="showSuggest = false" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import SmartSuggestModal from '@/components/smart/SmartSuggestModal.vue'
import { useMeta } from '@/composables/useSEO'

// SEO
useMeta({
  title: 'Beach Access Packages - الخيمة Beach Resort',
  description: 'Choose between VIP Premium or Standard Beach Access at الخيمة Beach Resort. Enjoy water activities and exclusive amenities.',
  keywords: 'beach access, vip beach, water activities, red sea, parasailing, banana boat'
})

const showSuggest = ref(false)

const activities = [
  { name: 'Banana Boat', icon: '🍌', description: '15 minutes of pure fun and excitement with friends and family', price: 35 },
  { name: 'Tube Ride', icon: '🛟', description: 'Thrilling water ride across the waves - safe for all ages', price: 30 },
  { name: 'Parasailing', icon: '🪂', description: 'Soar high above the Red Sea and enjoy breathtaking aerial views', price: 85 }
]

onMounted(() => {
  // Trigger suggest modal on idle (5 seconds of inactivity)
  let idleTimer: number
  
  const resetTimer = () => {
    clearTimeout(idleTimer)
    idleTimer = window.setTimeout(() => {
      showSuggest.value = true
    }, 5000)
  }

  window.addEventListener('mousemove', resetTimer)
  window.addEventListener('keypress', resetTimer)
  window.addEventListener('scroll', resetTimer)
  resetTimer()
})
</script>
