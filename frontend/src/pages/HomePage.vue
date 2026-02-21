<template>
  <div class="min-h-screen">
    <!-- 1. Hero Section -->
    <section class="relative h-screen flex items-center justify-center overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-blue-600 via-teal-500 to-blue-800"></div>
      <div class="relative z-10 text-center text-white px-4">
        <h1 class="text-6xl md:text-8xl font-bold mb-4 animate-fade-in">
          الخيمة Beach Resort
        </h1>
        <p class="text-2xl md:text-3xl mb-8 animate-slide-up">Your Escape Awaits</p>
        <div class="animate-bounce mt-12">
          <span class="text-4xl">↓</span>
        </div>
      </div>
      <BookingWidget :product-id="1" class="absolute bottom-8 left-1/2 -translate-x-1/2 z-20" />
    </section>

    <!-- 2. Services Grid -->
    <section class="py-20 px-4 max-w-7xl mx-auto">
      <h2 class="text-4xl font-bold text-center mb-12">Our Services</h2>
      <div ref="servicesGrid" class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="service in services" :key="service.name" 
             class="service-card bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition">
          <div class="text-5xl mb-4">{{ service.icon }}</div>
          <h3 class="text-2xl font-bold mb-2">{{ service.name }}</h3>
          <p class="text-gray-600 mb-4">{{ service.description }}</p>
          <router-link :to="service.link" class="text-blue-600 hover:text-blue-800">
            Explore →
          </router-link>
        </div>
      </div>
    </section>

    <!-- 3. Featured Packages -->
    <section class="py-20 px-4 bg-gray-50">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-4xl font-bold text-center mb-12">Featured Packages</h2>
        <div v-if="loading" class="grid md:grid-cols-3 gap-8">
          <div v-for="i in 3" :key="i" class="bg-white rounded-lg p-6 animate-pulse">
            <div class="h-48 bg-gray-200 rounded mb-4"></div>
            <div class="h-6 bg-gray-200 rounded mb-2"></div>
            <div class="h-4 bg-gray-200 rounded"></div>
          </div>
        </div>
        <div v-else class="grid md:grid-cols-3 gap-8">
          <div v-for="pkg in packages" :key="pkg.id" 
               class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition">
            <div class="h-48 bg-gradient-to-r from-blue-400 to-teal-400 flex items-center justify-center">
              <span class="text-white text-6xl">🏖️</span>
            </div>
            <div class="p-6">
              <div class="flex justify-between items-start mb-2">
                <h3 class="text-xl font-bold">{{ pkg.name }}</h3>
                <span class="px-2 py-1 bg-green-100 text-green-800 text-sm rounded">
                  Save ${{ pkg.savings }}
                </span>
              </div>
              <p class="text-gray-600 mb-4">{{ pkg.description }}</p>
              <div class="flex justify-between items-center">
                <span class="text-2xl font-bold text-blue-600">${{ pkg.price }}</span>
                <button class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                  Book Now
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 4. Chat Bubble -->
    <ChatBubble />

    <!-- 5. Testimonials -->
    <section class="py-20 px-4 max-w-7xl mx-auto">
      <h2 class="text-4xl font-bold text-center mb-12">What Our Guests Say</h2>
      <div class="grid md:grid-cols-3 gap-8">
        <div v-for="review in testimonials" :key="review.name" 
             class="bg-white rounded-lg shadow-lg p-6">
          <div class="flex items-center mb-4">
            <div class="text-3xl mr-2">{{ review.flag }}</div>
            <div>
              <h4 class="font-bold">{{ review.name }}</h4>
              <div class="text-yellow-500">{{ '★'.repeat(review.rating) }}</div>
            </div>
          </div>
          <p class="text-gray-600">{{ review.text }}</p>
        </div>
      </div>
    </section>

    <!-- 6. CTA Banner -->
    <section class="relative h-96 flex items-center justify-center overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-r from-blue-600 to-teal-600 opacity-90"></div>
      <div class="relative z-10 text-center text-white px-4">
        <h2 class="text-5xl font-bold mb-4">Book Your Escape Today</h2>
        <p class="text-xl mb-8">Limited time offers available</p>
        <router-link to="/rooms" 
                     class="inline-block px-8 py-4 bg-white text-blue-600 rounded-lg text-lg font-bold hover:bg-gray-100">
          Browse Rooms
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import BookingWidget from '@/components/smart/BookingWidget.vue'
import ChatBubble from '@/components/smart/ChatBubble.vue'
import { apiClient } from '@/api'

gsap.registerPlugin(ScrollTrigger)

const servicesGrid = ref<HTMLElement>()
const loading = ref(true)
const packages = ref<any[]>([])

const services = [
  { name: 'Luxury Rooms', icon: '🏨', description: 'Comfortable rooms with sea view', link: '/rooms' },
  { name: 'Private Beach', icon: '🏖️', description: 'VIP and standard beach access', link: '/beach' },
  { name: 'Restaurant', icon: '🍽️', description: 'Fine dining experience', link: '/restaurant' },
  { name: 'Cafe', icon: '☕', description: 'Coffee and light snacks', link: '/cafe' },
  { name: 'Activities', icon: '🏄', description: 'Water sports and more', link: '/activities' },
  { name: 'Events', icon: '🎉', description: 'Special occasions', link: '/events' }
]

const testimonials = [
  { name: 'John Smith', flag: '🇺🇸', rating: 5, text: 'Amazing experience! The beach is pristine and the service is exceptional.' },
  { name: 'Ahmed Hassan', flag: '🇪🇬', rating: 5, text: 'أفضل منتجع زرته! الخدمة ممتازة والموقع رائع.' },
  { name: 'Maria Garcia', flag: '🇪🇸', rating: 5, text: 'Perfect vacation spot. Will definitely come back!' }
]

async function fetchHomeData() {
  loading.value = true
  try {
    const response = await apiClient.get('/products/home')
    packages.value = response.data.packages || []
  } catch (e) {
    // Fallback data
    packages.value = [
      { id: 1, name: 'Weekend Getaway', description: '2 nights + breakfast', price: 299, savings: 50 },
      { id: 2, name: 'Family Package', description: '3 nights + all meals', price: 599, savings: 100 },
      { id: 3, name: 'Luxury Escape', description: '5 nights + VIP beach', price: 999, savings: 200 }
    ]
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchHomeData()
  
  if (servicesGrid.value) {
    gsap.from('.service-card', {
      scrollTrigger: {
        trigger: servicesGrid.value,
        start: 'top 80%'
      },
      y: 50,
      opacity: 0,
      duration: 0.6,
      stagger: 0.1
    })
  }
})
</script>

<style scoped>
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.animate-fade-in {
  animation: fade-in 1s ease-out;
}

.animate-slide-up {
  animation: slide-up 1s ease-out 0.3s both;
}
</style>
