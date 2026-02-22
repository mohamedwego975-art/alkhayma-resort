<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-5xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-12">
        <span class="badge badge-primary mb-4">Help Center</span>
        <h1 class="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
          Frequently Asked Questions
        </h1>
        <p class="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          Find answers to common questions about your stay at الخيمة Beach Resort
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="space-y-4">
        <div v-for="i in 5" :key="i" class="animate-pulse bg-white dark:bg-gray-900 rounded-xl h-20"></div>
      </div>

      <!-- FAQ List -->
      <div v-else class="space-y-4">
        <div
          v-for="(faq, index) in faqs"
          :key="index"
          class="bg-white dark:bg-gray-900 rounded-xl shadow-sm overflow-hidden"
        >
          <button
            @click="toggleFaq(index)"
            class="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
          >
            <span class="font-medium text-gray-900 dark:text-white pr-4">{{ faq.question }}</span>
            <span
              class="text-2xl text-ocean-deep-500 transition-transform flex-shrink-0"
              :class="{ 'rotate-45': openFaq === index }"
            >
              +
            </span>
          </button>
          <div
            v-show="openFaq === index"
            class="px-6 pb-4 text-gray-600 dark:text-gray-400 border-t border-gray-100 dark:border-gray-800 pt-4"
          >
            {{ faq.answer }}
          </div>
        </div>
      </div>

      <!-- Contact CTA -->
      <div class="mt-12 bg-gradient-to-r from-ocean-deep-500 to-teal-glow-500 rounded-2xl p-8 text-center text-white">
        <h2 class="text-2xl font-bold mb-2">Still have questions?</h2>
        <p class="text-white/90 mb-6">Our team is here to help you 24/7</p>
        <router-link to="/contact" class="bg-white text-ocean-deep-600 px-8 py-3 rounded-full font-bold hover:bg-white/90 transition-all shadow-lg inline-block">
          Contact Us
        </router-link>
      </div>

      <!-- Page Index -->
      <div class="mt-16 pt-16 border-t border-gray-200 dark:border-gray-800">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-8 text-center">
          Project Pages Index
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <strong>Frontend URL:</strong>
            <a href="http://localhost:5174" target="_blank" class="text-blue-600 hover:underline">
              http://localhost:5174
            </a>
          </div>
          <div>
            <strong>Backend API:</strong>
            <a href="http://localhost:8000/api" target="_blank" class="text-blue-600 hover:underline">
              http://localhost:8000/api
            </a>
          </div>
          <div>
            <strong>Total Pages:</strong> {{ totalPages }}
          </div>
          <div>
            <strong>Admin Pages:</strong> {{ adminPages.length }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { apiClient } from '@/api'
import { useMeta } from '@/composables/useSEO'

// SEO
useMeta({
  title: 'FAQ - الخيمة Beach Resort',
  description: 'Find answers to frequently asked questions about booking, amenities, policies, and more at الخيمة Beach Resort.',
  keywords: 'FAQ, questions, help, support, resort policies, booking help'
})

interface FAQ {
  question: string
  answer: string
}

interface PageInfo {
  name: string
  path: string
  icon: string
}

const faqs = ref<FAQ[]>([])
const loading = ref(true)
const openFaq = ref<number | null>(null)

const frontendPages: PageInfo[] = [
  { name: 'Home', path: '/', icon: '🏠' },
  { name: 'About', path: '/about', icon: 'ℹ️' },
  { name: 'Beach', path: '/beach', icon: '🏖️' },
  { name: 'Location', path: '/location', icon: '📍' },
  { name: 'Rooms', path: '/rooms', icon: '🛏️' },
  { name: 'Restaurant', path: '/restaurant', icon: '🍽️' },
  { name: 'Cafe', path: '/cafe', icon: '☕' },
  { name: 'Activities', path: '/activities', icon: '🎯' },
  { name: 'Events', path: '/events', icon: '🎉' },
  { name: 'Gallery', path: '/gallery', icon: '�' },
  { name: 'Team', path: '/team', icon: '👥' },
  { name: 'Contact', path: '/contact', icon: '📞' },
  { name: 'FAQ', path: '/faq', icon: '❓' },
]

const adminPages: PageInfo[] = [
  { name: 'Admin Dashboard', path: '/admin', icon: '🎛️' },
  { name: 'Analytics', path: '/admin/analytics', icon: '📈' },
  { name: 'Bookings', path: '/admin/bookings', icon: '📅' },
  { name: 'Rooms', path: '/admin/rooms', icon: '🏨' },
  { name: 'Products', path: '/admin/products', icon: '🛍️' },
  { name: 'Users', path: '/admin/users', icon: '�' },
  { name: 'Settings', path: '/admin/settings', icon: '⚙️' },
]

const totalPages = computed(() => frontendPages.length + adminPages.length)

function toggleFaq(index: number) {
  openFaq.value = openFaq.value === index ? null : index
}

onMounted(async () => {
  try {
    const response = await apiClient.get('/content/faq')
    faqs.value = response.data
  } catch (error) {
    console.error('Failed to fetch FAQs:', error)
    // Fallback FAQs
    faqs.value = [
      {
        question: "What are the check-in and check-out times?",
        answer: "Check-in is from 3:00 PM and check-out is until 12:00 PM. Early check-in and late check-out are available upon request and subject to availability."
      },
      {
        question: "Is airport transfer available?",
        answer: "Yes, we offer complimentary airport transfers from Sharm El Sheikh Airport. Please provide your flight details at least 24 hours before arrival."
      },
      {
        question: "Do you have WiFi?",
        answer: "Yes, complimentary high-speed WiFi is available throughout the resort including rooms, restaurants, and beach areas."
      },
      {
        question: "Are pets allowed?",
        answer: "We regret that pets are not allowed at the resort, with the exception of certified service animals."
      },
      {
        question: "What payment methods do you accept?",
        answer: "We accept all major credit cards (Visa, MasterCard, American Express), Paymob, Stripe, and cash payments in USD and EGP."
      }
    ]
  } finally {
    loading.value = false
  }
})
</script>
