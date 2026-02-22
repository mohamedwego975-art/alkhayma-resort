<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <div class="relative bg-gradient-to-br from-ocean-deep-900 via-ocean-deep-700 to-teal-glow-600 py-20 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <span class="inline-block px-4 py-2 mb-4 text-sm font-medium text-white bg-white/10 backdrop-blur-md rounded-full border border-white/20">
          📸 Memories
        </span>
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-4">
          Gallery
        </h1>
        <p class="text-xl text-white/90 max-w-2xl mx-auto">
          Capturing moments of paradise
        </p>
      </div>
    </div>

    <!-- Filter Tabs -->
    <section class="py-8 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-950 border-b border-gray-200 dark:border-gray-800">
      <div class="max-w-6xl mx-auto">
        <div class="flex flex-wrap justify-center gap-3">
          <button
            v-for="category in categories"
            :key="category.id"
            @click="activeCategory = category.id"
            class="px-6 py-3 rounded-full font-medium transition-all"
            :class="activeCategory === category.id
              ? 'bg-ocean-deep-500 text-white'
              : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'"
          >
            {{ category.name }}
          </button>
        </div>
      </div>
    </section>

    <!-- Gallery Grid -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-950">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <div
            v-for="(image, index) in filteredImages"
            :key="index"
            class="group relative aspect-square rounded-xl overflow-hidden cursor-pointer"
            @click="openLightbox(index)"
          >
            <div
              class="w-full h-full bg-gradient-to-br flex items-center justify-center text-6xl"
              :class="image.gradient"
            >
              {{ image.emoji }}
            </div>
            <div class="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all flex items-center justify-center">
              <div class="opacity-0 group-hover:opacity-100 transition-opacity text-white text-center">
                <span class="text-3xl">🔍</span>
                <p class="text-sm mt-2">{{ image.title }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Video Section -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-gray-900">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <span class="badge badge-primary mb-4">Videos</span>
          <h2 class="heading-display text-3xl md:text-4xl text-gray-900 dark:text-white mb-4">
            Experience الخيمة
          </h2>
        </div>

        <div class="grid md:grid-cols-2 gap-8">
          <div class="aspect-video rounded-2xl bg-gradient-to-br from-ocean-deep-500 to-teal-glow-500 flex items-center justify-center">
            <div class="text-center text-white">
              <span class="text-6xl mb-4">▶️</span>
              <p class="text-xl font-bold">Resort Tour</p>
              <p class="text-white/80">2:30 min</p>
            </div>
          </div>
          <div class="aspect-video rounded-2xl bg-gradient-to-br from-sand-gold-500 to-orange-500 flex items-center justify-center">
            <div class="text-center text-white">
              <span class="text-6xl mb-4">▶️</span>
              <p class="text-xl font-bold">Guest Experiences</p>
              <p class="text-white/80">1:45 min</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Instagram Feed -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-950">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <span class="badge badge-primary mb-4">@alkhayma.resort</span>
          <h2 class="heading-display text-3xl md:text-4xl text-gray-900 dark:text-white mb-4">
            Follow Us on Instagram
          </h2>
          <p class="text-gray-600 dark:text-gray-400">
            Tag us in your photos for a chance to be featured!
          </p>
        </div>

        <div class="grid grid-cols-3 md:grid-cols-6 gap-4">
          <div
            v-for="n in 6"
            :key="n"
            class="aspect-square rounded-xl bg-gradient-to-br from-gray-200 to-gray-300 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center"
          >
            <span class="text-3xl">📷</span>
          </div>
        </div>

        <div class="text-center mt-8">
          <a
            href="https://instagram.com/alkhayma.resort"
            target="_blank"
            class="btn-primary"
          >
            Follow @alkhayma.resort
          </a>
        </div>
      </div>
    </section>

    <!-- Lightbox Modal -->
    <div
      v-if="lightboxOpen"
      class="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4"
      @click="lightboxOpen = false"
    >
      <button
        class="absolute top-4 right-4 text-white text-4xl hover:text-gray-300"
        @click="lightboxOpen = false"
      >
        ×
      </button>
      <button
        v-if="currentImageIndex > 0"
        class="absolute left-4 top-1/2 -translate-y-1/2 text-white text-4xl hover:text-gray-300"
        @click.stop="prevImage"
      >
        ‹
      </button>
      <button
        v-if="currentImageIndex < filteredImages.length - 1"
        class="absolute right-4 top-1/2 -translate-y-1/2 text-white text-4xl hover:text-gray-300"
        @click.stop="nextImage"
      >
        ›
      </button>

      <div class="max-w-4xl max-h-[80vh]" @click.stop>
        <div
          class="w-full h-[60vh] rounded-xl bg-gradient-to-br flex items-center justify-center text-[12rem]"
          :class="filteredImages[currentImageIndex]?.gradient"
        >
          {{ filteredImages[currentImageIndex]?.emoji }}
        </div>
        <p class="text-white text-center mt-4 text-xl">
          {{ filteredImages[currentImageIndex]?.title }}
        </p>
        <p class="text-white/60 text-center">
          {{ currentImageIndex + 1 }} / {{ filteredImages.length }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useMeta } from '@/composables/useSEO'

// SEO
useMeta({
  title: 'Gallery - الخيمة Beach Resort',
  description: 'Explore our photo gallery showcasing the beauty of الخيمة Beach Resort, rooms, beach, dining, and guest experiences.',
  keywords: 'gallery, photos, beach resort, Red Sea, luxury resort, Egypt'
})

const categories = [
  { id: 'all', name: 'All Photos' },
  { id: 'rooms', name: 'Rooms' },
  { id: 'beach', name: 'Beach' },
  { id: 'dining', name: 'Dining' },
  { id: 'activities', name: 'Activities' }
]

const activeCategory = ref('all')
const lightboxOpen = ref(false)
const currentImageIndex = ref(0)

const images = [
  { category: 'rooms', emoji: '🏨', title: 'Deluxe Room', gradient: 'from-blue-400 to-blue-600' },
  { category: 'rooms', emoji: '🛏️', title: 'Suite Bedroom', gradient: 'from-purple-400 to-purple-600' },
  { category: 'rooms', emoji: '🌅', title: 'Sea View', gradient: 'from-orange-400 to-pink-500' },
  { category: 'beach', emoji: '🏖️', title: 'Private Beach', gradient: 'from-yellow-400 to-orange-500' },
  { category: 'beach', emoji: '🌴', title: 'Palm Trees', gradient: 'from-green-400 to-teal-500' },
  { category: 'beach', emoji: '🌊', title: 'Red Sea', gradient: 'from-blue-500 to-cyan-500' },
  { category: 'dining', emoji: '🍽️', title: 'Restaurant', gradient: 'from-amber-400 to-red-500' },
  { category: 'dining', emoji: '☕', title: 'Beach Cafe', gradient: 'from-brown-400 to-amber-500' },
  { category: 'dining', emoji: '🦞', title: 'Seafood', gradient: 'from-red-400 to-orange-500' },
  { category: 'activities', emoji: '🤿', title: 'Diving', gradient: 'from-cyan-400 to-blue-600' },
  { category: 'activities', emoji: '🏄', title: 'Surfing', gradient: 'from-blue-400 to-teal-500' },
  { category: 'activities', emoji: '🪂', title: 'Parasailing', gradient: 'from-purple-400 to-pink-500' },
  { category: 'activities', emoji: '🐪', title: 'Desert Safari', gradient: 'from-yellow-500 to-orange-500' },
  { category: 'activities', emoji: '🧘', title: 'Beach Yoga', gradient: 'from-green-300 to-teal-400' },
  { category: 'rooms', emoji: '🛁', title: 'Luxury Bathroom', gradient: 'from-blue-300 to-cyan-400' },
  { category: 'beach', emoji: '🌅', title: 'Sunset', gradient: 'from-orange-400 to-pink-600' }
]

const filteredImages = computed(() => {
  if (activeCategory.value === 'all') return images
  return images.filter(img => img.category === activeCategory.value)
})

function openLightbox(index: number) {
  currentImageIndex.value = index
  lightboxOpen.value = true
}

function nextImage() {
  if (currentImageIndex.value < filteredImages.value.length - 1) {
    currentImageIndex.value++
  }
}

function prevImage() {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--
  }
}
</script>
