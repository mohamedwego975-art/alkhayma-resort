<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <div class="relative bg-gradient-to-br from-teal-700 via-ocean-deep-700 to-blue-800 py-20 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <span class="inline-block px-4 py-2 mb-4 text-sm font-medium text-white bg-white/10 backdrop-blur-md rounded-full border border-white/20">
          🎯 Adventure Awaits
        </span>
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-4">
          Activities & Experiences
        </h1>
        <p class="text-xl text-white/90 max-w-2xl mx-auto">
          Discover endless adventures at the Red Sea
        </p>
      </div>
    </div>

    <!-- Water Sports -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-950">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <span class="badge badge-primary mb-4">Water Sports</span>
          <h2 class="heading-display text-3xl md:text-4xl text-gray-900 dark:text-white mb-4">
            Thrills on the Water
          </h2>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div class="bg-gray-50 dark:bg-gray-800 rounded-2xl overflow-hidden hover:shadow-xl transition-all group">
            <div class="h-48 bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center">
              <span class="text-7xl group-hover:scale-110 transition-transform">🏄</span>
            </div>
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Surfing & Windsurfing</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">Ride the Red Sea waves with professional instructors.</p>
              <div class="flex justify-between items-center">
                <span class="text-2xl font-bold text-ocean-deep-600">$45</span>
                <span class="text-sm text-gray-500">/hour</span>
              </div>
            </div>
          </div>

          <div class="bg-gray-50 dark:bg-gray-800 rounded-2xl overflow-hidden hover:shadow-xl transition-all group">
            <div class="h-48 bg-gradient-to-br from-teal-400 to-teal-600 flex items-center justify-center">
              <span class="text-7xl group-hover:scale-110 transition-transform">🤿</span>
            </div>
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Scuba Diving</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">Explore vibrant coral reefs and marine life.</p>
              <div class="flex justify-between items-center">
                <span class="text-2xl font-bold text-ocean-deep-600">$85</span>
                <span class="text-sm text-gray-500">/dive</span>
              </div>
            </div>
          </div>

          <div class="bg-gray-50 dark:bg-gray-800 rounded-2xl overflow-hidden hover:shadow-xl transition-all group">
            <div class="h-48 bg-gradient-to-br from-cyan-400 to-cyan-600 flex items-center justify-center">
              <span class="text-7xl group-hover:scale-110 transition-transform">🐠</span>
            </div>
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Snorkeling</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">Discover underwater wonders near the shore.</p>
              <div class="flex justify-between items-center">
                <span class="text-2xl font-bold text-ocean-deep-600">$25</span>
                <span class="text-sm text-gray-500">/session</span>
              </div>
            </div>
          </div>

          <div class="bg-gray-50 dark:bg-gray-800 rounded-2xl overflow-hidden hover:shadow-xl transition-all group">
            <div class="h-48 bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center">
              <span class="text-7xl group-hover:scale-110 transition-transform">🪂</span>
            </div>
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Parasailing</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">Soar above the sea for breathtaking views.</p>
              <div class="flex justify-between items-center">
                <span class="text-2xl font-bold text-ocean-deep-600">$85</span>
                <span class="text-sm text-gray-500">/flight</span>
              </div>
            </div>
          </div>

          <div class="bg-gray-50 dark:bg-gray-800 rounded-2xl overflow-hidden hover:shadow-xl transition-all group">
            <div class="h-48 bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center">
              <span class="text-7xl group-hover:scale-110 transition-transform">🍌</span>
            </div>
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Banana Boat</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">Fun group ride for all ages.</p>
              <div class="flex justify-between items-center">
                <span class="text-2xl font-bold text-ocean-deep-600">$35</span>
                <span class="text-sm text-gray-500">/15 min</span>
              </div>
            </div>
          </div>

          <div class="bg-gray-50 dark:bg-gray-800 rounded-2xl overflow-hidden hover:shadow-xl transition-all group">
            <div class="h-48 bg-gradient-to-br from-red-400 to-red-600 flex items-center justify-center">
              <span class="text-7xl group-hover:scale-110 transition-transform">🛥️</span>
            </div>
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Jet Ski</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">High-speed water adventure.</p>
              <div class="flex justify-between items-center">
                <span class="text-2xl font-bold text-ocean-deep-600">$60</span>
                <span class="text-sm text-gray-500">/30 min</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Land Activities -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-gray-900">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <span class="badge badge-primary mb-4">Land Adventures</span>
          <h2 class="heading-display text-3xl md:text-4xl text-gray-900 dark:text-white mb-4">
            Explore the Desert
          </h2>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="bg-white dark:bg-gray-800 rounded-xl p-6 text-center hover:shadow-lg transition-shadow">
            <div class="text-5xl mb-4">🏜️</div>
            <h3 class="font-bold text-gray-900 dark:text-white mb-2">Desert Safari</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">4x4 adventure into the Sinai desert</p>
            <span class="font-bold text-ocean-deep-600">$75</span>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-xl p-6 text-center hover:shadow-lg transition-shadow">
            <div class="text-5xl mb-4">🐪</div>
            <h3 class="font-bold text-gray-900 dark:text-white mb-2">Camel Riding</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Traditional Bedouin experience</p>
            <span class="font-bold text-ocean-deep-600">$40</span>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-xl p-6 text-center hover:shadow-lg transition-shadow">
            <div class="text-5xl mb-4">🏎️</div>
            <h3 class="font-bold text-gray-900 dark:text-white mb-2">ATV Quad Biking</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Thrilling desert ride</p>
            <span class="font-bold text-ocean-deep-600">$55</span>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-xl p-6 text-center hover:shadow-lg transition-shadow">
            <div class="text-5xl mb-4">⛰️</div>
            <h3 class="font-bold text-gray-900 dark:text-white mb-2">Mountain Hiking</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Guided Sinai mountain trails</p>
            <span class="font-bold text-ocean-deep-600">$35</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Resort Activities -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-950">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <span class="badge badge-primary mb-4">At the Resort</span>
          <h2 class="heading-display text-3xl md:text-4xl text-gray-900 dark:text-white mb-4">
            On-Site Activities
          </h2>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div class="text-center">
            <div class="w-20 h-20 rounded-full bg-ocean-deep-100 dark:bg-ocean-deep-900 mx-auto mb-4 flex items-center justify-center text-4xl">
              🧘
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Beach Yoga</h3>
            <p class="text-gray-600 dark:text-gray-400">Sunrise and sunset sessions</p>
            <span class="inline-block mt-2 text-ocean-deep-600 font-bold">$15/session</span>
          </div>

          <div class="text-center">
            <div class="w-20 h-20 rounded-full bg-ocean-deep-100 dark:bg-ocean-deep-900 mx-auto mb-4 flex items-center justify-center text-4xl">
              🏐
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Beach Volleyball</h3>
            <p class="text-gray-600 dark:text-gray-400">Daily tournaments</p>
            <span class="inline-block mt-2 text-ocean-deep-600 font-bold">Free</span>
          </div>

          <div class="text-center">
            <div class="w-20 h-20 rounded-full bg-ocean-deep-100 dark:bg-ocean-deep-900 mx-auto mb-4 flex items-center justify-center text-4xl">
              🎨
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Art Workshops</h3>
            <p class="text-gray-600 dark:text-gray-400">Painting and crafts</p>
            <span class="inline-block mt-2 text-ocean-deep-600 font-bold">$20</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Kids Club -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-yellow-50 to-orange-50 dark:from-gray-800 dark:to-gray-900">
      <div class="max-w-6xl mx-auto">
        <div class="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <span class="badge bg-yellow-100 text-yellow-800 mb-4">Kids Club</span>
            <h2 class="heading-display text-3xl md:text-4xl text-gray-900 dark:text-white mb-6">
              Fun for Little Ones
            </h2>
            <p class="text-gray-600 dark:text-gray-400 mb-6">
              Our supervised Kids Club offers endless entertainment for children aged 4-12, giving parents time to relax.
            </p>
            <ul class="space-y-3">
              <li class="flex items-center gap-3">
                <span class="text-2xl">🏰</span>
                <span class="text-gray-700 dark:text-gray-300">Beach games and sandcastle building</span>
              </li>
              <li class="flex items-center gap-3">
                <span class="text-2xl">🎨</span>
                <span class="text-gray-700 dark:text-gray-300">Arts and crafts workshops</span>
              </li>
              <li class="flex items-center gap-3">
                <span class="text-2xl">🏊</span>
                <span class="text-gray-700 dark:text-gray-300">Swimming lessons</span>
              </li>
              <li class="flex items-center gap-3">
                <span class="text-2xl">🎬</span>
                <span class="text-gray-700 dark:text-gray-300">Movie nights</span>
              </li>
            </ul>
            <div class="mt-6 p-4 bg-white dark:bg-gray-800 rounded-xl">
              <p class="font-bold text-gray-900 dark:text-white">Hours: 9:00 AM - 6:00 PM</p>
              <p class="text-ocean-deep-600 font-bold">Ages 4-12 • Free for guests</p>
            </div>
          </div>
          <div class="aspect-square rounded-2xl bg-gradient-to-br from-yellow-300 to-orange-400 flex items-center justify-center">
            <span class="text-9xl">👶</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Booking CTA -->
    <section class="py-16 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto">
        <div class="bg-gradient-to-r from-ocean-deep-500 to-teal-glow-500 rounded-2xl p-8 md:p-12 text-center text-white">
          <h2 class="text-3xl font-bold mb-4">Ready for Adventure?</h2>
          <p class="text-lg text-white/90 mb-8">
            Book your activities in advance to secure your spot!
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <router-link to="/booking" class="bg-white text-ocean-deep-600 px-8 py-4 rounded-full font-bold hover:bg-white/90 transition-all shadow-lg">
              Book Activities
            </router-link>
            <a href="tel:+201001234567" class="bg-white/20 text-white px-8 py-4 rounded-full font-bold hover:bg-white/30 transition-all border border-white/30">
              Call to Inquire
            </a>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useMeta } from '@/composables/useSEO'

// SEO
useMeta({
  title: 'Activities - الخيمة Beach Resort',
  description: 'Discover water sports, desert adventures, and resort activities at الخيمة Beach Resort. Diving, snorkeling, camel riding, and more!',
  keywords: 'activities, water sports, diving, snorkeling, desert safari, Red Sea, things to do'
})
</script>
