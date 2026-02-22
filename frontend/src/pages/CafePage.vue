<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <div class="relative bg-gradient-to-br from-amber-800 via-orange-700 to-yellow-600 py-20 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <span class="inline-block px-4 py-2 mb-4 text-sm font-medium text-white bg-white/10 backdrop-blur-md rounded-full border border-white/20">
          ☕ Beachfront Cafe
        </span>
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-4">
          The Shore Cafe
        </h1>
        <p class="text-xl text-white/90 max-w-2xl mx-auto">
          Where coffee meets the waves
        </p>
      </div>
    </div>

    <!-- Atmosphere Section -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-950">
      <div class="max-w-6xl mx-auto">
        <div class="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <span class="badge badge-primary mb-4">Atmosphere</span>
            <h2 class="heading-display text-3xl md:text-4xl text-gray-900 dark:text-white mb-6">
              Relax by the Sea
            </h2>
            <p class="text-gray-600 dark:text-gray-400 mb-6">
              The Shore Cafe offers a laid-back atmosphere just steps from the water. Sink into our comfortable seating, feel the sea breeze, and watch the waves while enjoying premium coffee and light bites.
            </p>
            <div class="grid grid-cols-2 gap-4">
              <div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-4 text-center">
                <span class="text-3xl mb-2">🌊</span>
                <p class="font-bold text-gray-900 dark:text-white">Beachfront</p>
                <p class="text-sm text-gray-500">Direct sea views</p>
              </div>
              <div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-4 text-center">
                <span class="text-3xl mb-2">🎵</span>
                <p class="font-bold text-gray-900 dark:text-white">Live Music</p>
                <p class="text-sm text-gray-500">Acoustic evenings</p>
              </div>
              <div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-4 text-center">
                <span class="text-3xl mb-2">📚</span>
                <p class="font-bold text-gray-900 dark:text-white">Library</p>
                <p class="text-sm text-gray-500">Book exchange</p>
              </div>
              <div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-4 text-center">
                <span class="text-3xl mb-2">🎲</span>
                <p class="font-bold text-gray-900 dark:text-white">Games</p>
                <p class="text-sm text-gray-500">Board games</p>
              </div>
            </div>
          </div>
          <div class="aspect-square rounded-2xl bg-gradient-to-br from-amber-300 to-orange-400 flex items-center justify-center">
            <span class="text-9xl">☕</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Menu Section -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-gray-900">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <span class="badge badge-primary mb-4">Menu</span>
          <h2 class="heading-display text-3xl md:text-4xl text-gray-900 dark:text-white mb-4">
            Coffee & More
          </h2>
        </div>

        <!-- Coffee -->
        <div class="mb-12">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
            <span class="text-3xl">☕</span>
            Specialty Coffee
          </h3>
          <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Arabic Coffee</h4>
                <span class="font-bold text-amber-600">$4</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Traditional cardamom coffee</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Turkish Coffee</h4>
                <span class="font-bold text-amber-600">$5</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Strong and unfiltered</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Espresso</h4>
                <span class="font-bold text-amber-600">$3.5</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Single or double shot</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Cappuccino</h4>
                <span class="font-bold text-amber-600">$5.5</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">With latte art</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Iced Latte</h4>
                <span class="font-bold text-amber-600">$6</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Perfect for hot days</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Cold Brew</h4>
                <span class="font-bold text-amber-600">$6.5</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">12-hour steeped</p>
            </div>
          </div>
        </div>

        <!-- Tea -->
        <div class="mb-12">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
            <span class="text-3xl">🍵</span>
            Tea Selection
          </h3>
          <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Egyptian Tea</h4>
                <span class="font-bold text-amber-600">$3</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Black tea with mint</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Chamomile</h4>
                <span class="font-bold text-amber-600">$4</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Soothing herbal tea</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Hibiscus (Karkade)</h4>
                <span class="font-bold text-amber-600">$4</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Refreshing cold or hot</p>
            </div>
          </div>
        </div>

        <!-- Light Bites -->
        <div>
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
            <span class="text-3xl">🥐</span>
            Light Bites
          </h3>
          <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Croissants</h4>
                <span class="font-bold text-amber-600">$4</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Butter or chocolate filled</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Fruit Tart</h4>
                <span class="font-bold text-amber-600">$6</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Fresh seasonal fruits</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Cheesecake</h4>
                <span class="font-bold text-amber-600">$7</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">New York style</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Ice Cream</h4>
                <span class="font-bold text-amber-600">$5</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Local and international flavors</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Sandwiches</h4>
                <span class="font-bold text-amber-600">$8</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Fresh and toasted</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Smoothies</h4>
                <span class="font-bold text-amber-600">$7</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Fresh fruit blends</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Opening Hours -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-950">
      <div class="max-w-4xl mx-auto">
        <div class="bg-gradient-to-r from-amber-100 to-orange-100 dark:from-gray-800 dark:to-gray-700 rounded-2xl p-8">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center">Opening Hours</h2>
          <div class="grid md:grid-cols-2 gap-6">
            <div class="text-center md:text-left">
              <h3 class="font-bold text-gray-900 dark:text-white mb-2">Daily</h3>
              <p class="text-gray-600 dark:text-gray-400">7:00 AM - 11:00 PM</p>
            </div>
            <div class="text-center md:text-left">
              <h3 class="font-bold text-gray-900 dark:text-white mb-2">Happy Hour</h3>
              <p class="text-gray-600 dark:text-gray-400">4:00 PM - 6:00 PM</p>
              <p class="text-sm text-amber-600">20% off all drinks!</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-16 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto text-center">
        <div class="bg-gradient-to-r from-amber-600 to-orange-600 rounded-2xl p-8 md:p-12 text-white">
          <h2 class="text-3xl font-bold mb-4">Join Us for Coffee</h2>
          <p class="text-lg text-white/90 mb-8">
            Start your morning right or unwind after a day in the sun
          </p>
          <router-link to="/location" class="bg-white text-amber-600 px-8 py-4 rounded-full font-bold hover:bg-white/90 transition-all shadow-lg">
            Find Us on the Beach
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useMeta } from '@/composables/useSEO'

// SEO
useMeta({
  title: 'Cafe - الخيمة Beach Resort',
  description: 'Visit The Shore Cafe for premium coffee, tea, and light bites with stunning Red Sea views. Open daily 7AM-11PM with happy hour specials.',
  keywords: 'cafe, coffee, beach cafe, Red Sea, pastries, smoothies'
})
</script>
