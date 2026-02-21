<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-4xl font-bold mb-8 text-center">Beach Access</h1>

      <!-- VIP vs Normal Cards -->
      <div class="grid md:grid-cols-2 gap-8 mb-12">
        <!-- VIP Card -->
        <div class="bg-white rounded-lg shadow-xl overflow-hidden border-4 border-sand-gold-500">
          <div class="h-64 bg-gradient-to-r from-sand-gold-400 to-sand-gold-600 flex items-center justify-center">
            <span class="text-white text-8xl">👑</span>
          </div>
          <div class="p-8">
            <div class="flex items-center gap-2 mb-4">
              <h2 class="text-3xl font-bold">VIP Beach</h2>
              <span class="px-3 py-1 bg-sand-gold-100 text-sand-gold-800 rounded">Premium</span>
            </div>
            <p class="text-gray-600 mb-6">Exclusive beach experience with premium amenities</p>
            
            <ul class="space-y-3 mb-8">
              <li class="flex items-center gap-2">
                <span class="text-green-500">✓</span>
                <span>Private Cabana</span>
              </li>
              <li class="flex items-center gap-2">
                <span class="text-green-500">✓</span>
                <span>Dedicated Waiter Service</span>
              </li>
              <li class="flex items-center gap-2">
                <span class="text-green-500">✓</span>
                <span>Premium Sunbeds</span>
              </li>
              <li class="flex items-center gap-2">
                <span class="text-green-500">✓</span>
                <span>Complimentary Drinks</span>
              </li>
              <li class="flex items-center gap-2">
                <span class="text-green-500">✓</span>
                <span>Priority Access</span>
              </li>
            </ul>

            <div class="mb-6">
              <span class="text-4xl font-bold text-sand-gold-600">$150</span>
              <span class="text-gray-600">/day</span>
            </div>

            <button class="w-full py-3 bg-sand-gold-500 text-white rounded-lg hover:bg-sand-gold-600 font-bold">
              Book VIP Access
            </button>
          </div>
        </div>

        <!-- Normal Card -->
        <div class="bg-white rounded-lg shadow-xl overflow-hidden border-4 border-ocean-deep-500">
          <div class="h-64 bg-gradient-to-r from-ocean-deep-400 to-ocean-deep-600 flex items-center justify-center">
            <span class="text-white text-8xl">🏖️</span>
          </div>
          <div class="p-8">
            <div class="flex items-center gap-2 mb-4">
              <h2 class="text-3xl font-bold">Standard Beach</h2>
              <span class="px-3 py-1 bg-ocean-deep-100 text-ocean-deep-800 rounded">Popular</span>
            </div>
            <p class="text-gray-600 mb-6">Enjoy our beautiful beach with standard amenities</p>
            
            <ul class="space-y-3 mb-8">
              <li class="flex items-center gap-2">
                <span class="text-green-500">✓</span>
                <span>Beach Access</span>
              </li>
              <li class="flex items-center gap-2">
                <span class="text-green-500">✓</span>
                <span>Standard Sunbeds</span>
              </li>
              <li class="flex items-center gap-2">
                <span class="text-green-500">✓</span>
                <span>Umbrella</span>
              </li>
              <li class="flex items-center gap-2">
                <span class="text-green-500">✓</span>
                <span>Shower Facilities</span>
              </li>
              <li class="flex items-center gap-2">
                <span class="text-green-500">✓</span>
                <span>Changing Rooms</span>
              </li>
            </ul>

            <div class="mb-6">
              <span class="text-4xl font-bold text-ocean-deep-600">$50</span>
              <span class="text-gray-600">/day</span>
            </div>

            <button class="btn-primary w-full">
              Book Standard Access
            </button>
          </div>
        </div>
      </div>

      <!-- Activities Add-ons -->
      <section class="mb-12">
        <h2 class="text-3xl font-bold mb-8 text-center">Water Activities</h2>
        <div class="grid md:grid-cols-3 gap-8">
          <div v-for="activity in activities" :key="activity.name"
               class="card hover:scale-105 transition-transform duration-200">
            <div class="h-48 bg-gradient-to-r from-teal-glow-400 to-ocean-deep-500 flex items-center justify-center">
              <span class="text-white text-6xl">{{ activity.icon }}</span>
            </div>
            <div class="p-6">
              <h3 class="text-xl font-bold mb-2">{{ activity.name }}</h3>
              <p class="text-gray-600 mb-4">{{ activity.description }}</p>
              <div class="flex justify-between items-center">
                <span class="text-2xl font-bold text-ocean-deep-600">${{ activity.price }}</span>
                <button class="btn-primary text-sm">Add</button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <SmartSuggestModal v-if="showSuggest" :product-id="1" trigger="idle" @close="showSuggest = false" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import SmartSuggestModal from '@/components/smart/SmartSuggestModal.vue'

const showSuggest = ref(false)

const activities = [
  { name: 'Banana Boat', icon: '🍌', description: '15 minutes of fun', price: 35 },
  { name: 'Tube Ride', icon: '🛟', description: 'Exciting water ride', price: 30 },
  { name: 'Parasailing', icon: '🪂', description: 'Fly above the sea', price: 85 }
]

onMounted(() => {
  // Trigger suggest modal on idle
  let idleTimer: number
  
  const resetTimer = () => {
    clearTimeout(idleTimer)
    idleTimer = setTimeout(() => {
      showSuggest.value = true
    }, 5000)
  }

  window.addEventListener('mousemove', resetTimer)
  window.addEventListener('keypress', resetTimer)
  resetTimer()
})
</script>
