<template>
  <div>
    <!-- Hero Section -->
    <section class="relative h-screen flex items-center justify-center overflow-hidden">
      <div class="absolute inset-0 gradient-animated"></div>
      
      <!-- Floating Elements -->
      <div class="absolute inset-0 overflow-hidden pointer-events-none">
        <div class="absolute top-20 left-10 w-72 h-72 bg-white/10 rounded-full blur-3xl float"></div>
        <div class="absolute bottom-20 right-10 w-96 h-96 bg-teal-glow-500/10 rounded-full blur-3xl float" style="animation-delay: -3s"></div>
      </div>

      <div class="relative z-10 text-center text-white px-4 max-w-5xl mx-auto">
        <div class="mb-6 inline-block">
          <span class="badge glass-dark text-white text-sm px-4 py-2">✨ Luxury Beach Resort</span>
        </div>
        
        <h1 class="heading-display text-5xl sm:text-6xl md:text-7xl lg:text-8xl mb-6 animate-fade-in">
          الخيمة Beach Resort
        </h1>
        
        <p class="text-xl sm:text-2xl md:text-3xl mb-8 animate-slide-up font-light">
          Your Escape Awaits
        </p>
        
        <div class="flex gap-4 justify-center mb-12 animate-slide-up" style="animation-delay: 0.2s">
          <router-link to="/rooms" class="btn-primary">
            Explore Rooms
          </router-link>
          <router-link to="/beach" class="glass-dark px-6 py-3 rounded-xl font-semibold hover:bg-white/20 transition-all">
            View Beach
          </router-link>
        </div>

        <div class="animate-bounce mt-8">
          <span class="text-3xl md:text-4xl">↓</span>
        </div>
      </div>

      <BookingWidget :product-id="1" class="absolute bottom-4 md:bottom-8 left-1/2 -translate-x-1/2 z-20 w-11/12 md:w-auto glass shadow-2xl" />
    </section>

    <!-- Services Grid -->
    <section class="section-padding bg-gradient-to-b from-white to-gray-50">
      <div class="container-responsive">
        <div class="text-center mb-12">
          <span class="badge badge-primary mb-4">Our Services</span>
          <h2 class="heading-display text-4xl md:text-5xl lg:text-6xl mb-4 gradient-text">
            Experience Luxury
          </h2>
          <p class="text-gray-600 text-lg max-w-2xl mx-auto">
            Discover our world-class amenities and services designed for your perfect getaway
          </p>
        </div>

        <div ref="servicesGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
          <router-link 
            v-for="(service, index) in services" 
            :key="service.name"
            :to="service.link"
            class="service-card card group cursor-pointer"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <div class="p-8 text-center">
              <div class="text-5xl md:text-6xl mb-6 transform group-hover:scale-110 transition-transform duration-300">
                {{ service.icon }}
              </div>
              <h3 class="text-xl md:text-2xl font-bold mb-3 text-gray-800 group-hover:text-ocean-deep-600 transition-colors">
                {{ service.name }}
              </h3>
              <p class="text-gray-600 mb-4 text-sm md:text-base">
                {{ service.description }}
              </p>
              <span class="inline-flex items-center gap-2 text-ocean-deep-600 font-semibold group-hover:gap-4 transition-all">
                Explore <span>→</span>
              </span>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Featured Packages -->
    <section class="section-padding relative overflow-hidden">
      <!-- Background Pattern -->
      <div class="absolute inset-0 opacity-5">
        <div class="absolute inset-0" style="background-image: radial-gradient(circle, #0284c7 1px, transparent 1px); background-size: 30px 30px;"></div>
      </div>

      <div class="container-responsive relative z-10">
        <div class="text-center mb-12">
          <span class="badge badge-gold mb-4">Special Offers</span>
          <h2 class="heading-display text-4xl md:text-5xl lg:text-6xl mb-4 text-gray-800">
            Featured Packages
          </h2>
          <p class="text-gray-600 text-lg max-w-2xl mx-auto">
            Exclusive deals crafted for an unforgettable experience
          </p>
        </div>
        
        <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
          <div v-for="i in 3" :key="i" class="card p-6 animate-pulse">
            <div class="h-48 bg-gray-200 rounded-xl mb-4"></div>
            <div class="h-6 bg-gray-200 rounded mb-2"></div>
            <div class="h-4 bg-gray-200 rounded"></div>
          </div>
        </div>
        
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
          <div v-for="pkg in packages" :key="pkg.id" class="card-premium group cursor-pointer">
            <div class="relative h-56 bg-gradient-to-br from-ocean-deep-400 via-teal-glow-400 to-ocean-deep-500 flex items-center justify-center overflow-hidden">
              <div class="absolute inset-0 bg-black/10 group-hover:bg-black/0 transition-colors"></div>
              <span class="text-white text-6xl md:text-7xl relative z-10 transform group-hover:scale-110 transition-transform">🏖️</span>
            </div>
            
            <div class="p-6 bg-white">
              <div class="flex justify-between items-start mb-3">
                <h3 class="text-xl md:text-2xl font-bold text-gray-800">{{ pkg.name }}</h3>
                <span class="badge badge-success shimmer">
                  Save ${{ pkg.savings }}
                </span>
              </div>
              
              <p class="text-gray-600 mb-6 text-sm md:text-base">{{ pkg.description }}</p>
              
              <div class="flex justify-between items-center">
                <div>
                  <span class="text-3xl md:text-4xl font-bold gradient-text">${{ pkg.price }}</span>
                </div>
                <button class="btn-gold">Book Now</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Chat Bubble -->
    <ChatBubble />

    <!-- Testimonials -->
    <section class="section-padding bg-gradient-to-b from-white to-ocean-deep-50">
      <div class="container-responsive">
        <div class="text-center mb-12">
          <span class="badge badge-primary mb-4">Testimonials</span>
          <h2 class="heading-display text-4xl md:text-5xl lg:text-6xl mb-4 text-gray-800">
            What Our Guests Say
          </h2>
          <p class="text-gray-600 text-lg max-w-2xl mx-auto">
            Real experiences from real travelers
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
          <div v-for="review in testimonials" :key="review.name" class="glass p-8 rounded-2xl hover:shadow-2xl transition-all duration-300">
            <div class="flex items-center mb-6">
              <div class="w-12 h-12 rounded-full bg-gradient-to-br from-ocean-deep-400 to-teal-glow-400 flex items-center justify-center text-2xl mr-4">
                {{ review.flag }}
              </div>
              <div>
                <h4 class="font-bold text-gray-800 text-base md:text-lg">{{ review.name }}</h4>
                <div class="text-sand-gold-500 text-lg">{{ '★'.repeat(review.rating) }}</div>
              </div>
            </div>
            <p class="text-gray-600 text-sm md:text-base leading-relaxed italic">
              "{{ review.text }}"
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Banner -->
    <section class="relative h-96 md:h-[500px] flex items-center justify-center overflow-hidden">
      <div class="absolute inset-0 gradient-animated"></div>
      
      <!-- Overlay Pattern -->
      <div class="absolute inset-0 opacity-10">
        <div class="absolute inset-0" style="background-image: url('data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'1\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>
      </div>

      <div class="relative z-10 text-center text-white px-4 max-w-4xl mx-auto">
        <h2 class="heading-display text-4xl md:text-5xl lg:text-6xl mb-6">
          Book Your Escape Today
        </h2>
        <p class="text-xl md:text-2xl mb-8 font-light">
          Limited time offers available • Best price guaranteed
        </p>
        <div class="flex gap-4 justify-center flex-wrap">
          <router-link to="/rooms" class="glass-dark px-8 py-4 rounded-xl text-lg font-bold hover:bg-white/30 transition-all shadow-xl">
            Browse Rooms
          </router-link>
          <router-link to="/beach" class="btn-gold px-8 py-4 text-lg">
            View Beach Access
          </router-link>
        </div>
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
  { name: 'Restaurant', icon: '🍽️', description: 'Fine dining experience', link: '#' },
  { name: 'Cafe', icon: '☕', description: 'Coffee and light snacks', link: '#' },
  { name: 'Activities', icon: '🏄', description: 'Water sports and more', link: '#' },
  { name: 'Events', icon: '🎉', description: 'Special occasions', link: '#' }
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
