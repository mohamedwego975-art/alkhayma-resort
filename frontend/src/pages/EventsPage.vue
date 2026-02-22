<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <div class="relative bg-gradient-to-br from-purple-900 via-pink-800 to-rose-700 py-20 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <span class="inline-block px-4 py-2 mb-4 text-sm font-medium text-white bg-white/10 backdrop-blur-md rounded-full border border-white/20">
          🎉 Celebrate with Us
        </span>
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-4">
          Events & Celebrations
        </h1>
        <p class="text-xl text-white/90 max-w-2xl mx-auto">
          Create unforgettable memories at the Red Sea
        </p>
      </div>
    </div>

    <!-- Weddings Section -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-950">
      <div class="max-w-6xl mx-auto">
        <div class="grid md:grid-cols-2 gap-12 items-center">
          <div class="order-2 md:order-1">
            <div class="aspect-square rounded-2xl bg-gradient-to-br from-pink-400 to-rose-500 flex items-center justify-center">
              <span class="text-9xl">💒</span>
            </div>
          </div>
          <div class="order-1 md:order-2">
            <span class="badge bg-pink-100 text-pink-800 mb-4">Weddings</span>
            <h2 class="heading-display text-3xl md:text-4xl text-gray-900 dark:text-white mb-6">
              Your Dream Beach Wedding
            </h2>
            <p class="text-gray-600 dark:text-gray-400 mb-6">
              Say "I do" with the Red Sea as your backdrop. Our dedicated wedding planners will create your perfect day, from intimate ceremonies to grand celebrations.
            </p>
            <ul class="space-y-3 mb-8">
              <li class="flex items-center gap-3">
                <span class="text-2xl">🏖️</span>
                <span class="text-gray-700 dark:text-gray-300">Beachfront ceremony setups</span>
              </li>
              <li class="flex items-center gap-3">
                <span class="text-2xl">🍽️</span>
                <span class="text-gray-700 dark:text-gray-300">Customized catering menus</span>
              </li>
              <li class="flex items-center gap-3">
                <span class="text-2xl">🎵</span>
                <span class="text-gray-700 dark:text-gray-300">Live music and entertainment</span>
              </li>
              <li class="flex items-center gap-3">
                <span class="text-2xl">📸</span>
                <span class="text-gray-700 dark:text-gray-300">Professional photography</span>
              </li>
              <li class="flex items-center gap-3">
                <span class="text-2xl">🌺</span>
                <span class="text-gray-700 dark:text-gray-300">Floral arrangements & decor</span>
              </li>
            </ul>
            <div class="flex gap-4">
              <router-link to="/contact" class="btn-primary">
                Plan Your Wedding
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Event Types -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-gray-900">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <span class="badge badge-primary mb-4">Occasions</span>
          <h2 class="heading-display text-3xl md:text-4xl text-gray-900 dark:text-white mb-4">
            Perfect for Every Celebration
          </h2>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="bg-white dark:bg-gray-800 rounded-2xl p-8 text-center hover:shadow-xl transition-shadow">
            <div class="text-5xl mb-4">🎂</div>
            <h3 class="font-bold text-gray-900 dark:text-white mb-2">Birthdays</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">From intimate dinners to pool parties</p>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-2xl p-8 text-center hover:shadow-xl transition-shadow">
            <div class="text-5xl mb-4">💍</div>
            <h3 class="font-bold text-gray-900 dark:text-white mb-2">Engagements</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">Romantic proposals by the sea</p>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-2xl p-8 text-center hover:shadow-xl transition-shadow">
            <div class="text-5xl mb-4">🎓</div>
            <h3 class="font-bold text-gray-900 dark:text-white mb-2">Graduations</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">Celebrate achievements in style</p>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-2xl p-8 text-center hover:shadow-xl transition-shadow">
            <div class="text-5xl mb-4">👶</div>
            <h3 class="font-bold text-gray-900 dark:text-white mb-2">Baby Showers</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">Beautiful celebrations for new beginnings</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Corporate Events -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-950">
      <div class="max-w-6xl mx-auto">
        <div class="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <span class="badge bg-blue-100 text-blue-800 mb-4">Corporate</span>
            <h2 class="heading-display text-3xl md:text-4xl text-gray-900 dark:text-white mb-6">
              Business Meets Pleasure
            </h2>
            <p class="text-gray-600 dark:text-gray-400 mb-6">
              Host your corporate retreats, team building events, and conferences in an inspiring seaside setting.
            </p>
            <ul class="space-y-3 mb-8">
              <li class="flex items-center gap-3">
                <span class="text-2xl">🏢</span>
                <span class="text-gray-700 dark:text-gray-300">Conference rooms with AV equipment</span>
              </li>
              <li class="flex items-center gap-3">
                <span class="text-2xl">🤝</span>
                <span class="text-gray-700 dark:text-gray-300">Team building activities</span>
              </li>
              <li class="flex items-center gap-3">
                <span class="text-2xl">🍽️</span>
                <span class="text-gray-700 dark:text-gray-300">Business lunch & dinner catering</span>
              </li>
              <li class="flex items-center gap-3">
                <span class="text-2xl">🎉</span>
                <span class="text-gray-700 dark:text-gray-300">Gala dinners & award ceremonies</span>
              </li>
            </ul>
            <router-link to="/contact" class="btn-primary">
              Plan Corporate Event
            </router-link>
          </div>
          <div class="aspect-square rounded-2xl bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center">
            <span class="text-9xl">💼</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Event Spaces -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-gray-900">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <span class="badge badge-primary mb-4">Venues</span>
          <h2 class="heading-display text-3xl md:text-4xl text-gray-900 dark:text-white mb-4">
            Our Event Spaces
          </h2>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div class="bg-white dark:bg-gray-800 rounded-2xl overflow-hidden shadow-lg">
            <div class="h-48 bg-gradient-to-br from-blue-400 to-cyan-500 flex items-center justify-center">
              <span class="text-7xl">🏖️</span>
            </div>
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Beachfront Lawn</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">Capacity: 300 guests</p>
              <p class="text-sm text-gray-500">Perfect for weddings, concerts, and large celebrations</p>
            </div>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-2xl overflow-hidden shadow-lg">
            <div class="h-48 bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center">
              <span class="text-7xl">🌴</span>
            </div>
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Garden Terrace</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">Capacity: 150 guests</p>
              <p class="text-sm text-gray-500">Ideal for receptions, dinners, and cocktail parties</p>
            </div>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-2xl overflow-hidden shadow-lg">
            <div class="h-48 bg-gradient-to-br from-purple-400 to-pink-500 flex items-center justify-center">
              <span class="text-7xl">🏛️</span>
            </div>
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Grand Ballroom</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4">Capacity: 200 guests</p>
              <p class="text-sm text-gray-500">Elegant indoor space for conferences and galas</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Packages -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-950">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <span class="badge badge-primary mb-4">Packages</span>
          <h2 class="heading-display text-3xl md:text-4xl text-gray-900 dark:text-white mb-4">
            Event Packages
          </h2>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div class="border-2 border-gray-200 dark:border-gray-700 rounded-2xl p-8 hover:border-ocean-deep-500 transition-colors">
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Intimate</h3>
            <p class="text-gray-600 dark:text-gray-400 mb-4">For 20-50 guests</p>
            <div class="text-3xl font-bold text-ocean-deep-600 mb-6">From $2,500</div>
            <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400 mb-6">
              <li>• Venue rental (4 hours)</li>
              <li>• Basic catering package</li>
              <li>• Standard sound system</li>
              <li>• Tables & chairs setup</li>
            </ul>
            <router-link to="/contact" class="btn-secondary w-full text-center block">
              Inquire
            </router-link>
          </div>

          <div class="border-2 border-sand-gold-500 rounded-2xl p-8 relative">
            <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-sand-gold-500 text-white px-4 py-1 rounded-full text-sm font-bold">
              Popular
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Premium</h3>
            <p class="text-gray-600 dark:text-gray-400 mb-4">For 50-150 guests</p>
            <div class="text-3xl font-bold text-sand-gold-600 mb-6">From $7,500</div>
            <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400 mb-6">
              <li>• Venue rental (8 hours)</li>
              <li>• Premium catering & bar</li>
              <li>• Professional sound & lights</li>
              <li>• Decor package</li>
              <li>• Event coordinator</li>
            </ul>
            <router-link to="/contact" class="btn-primary w-full text-center block">
              Inquire
            </router-link>
          </div>

          <div class="border-2 border-gray-200 dark:border-gray-700 rounded-2xl p-8 hover:border-ocean-deep-500 transition-colors">
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Grand</h3>
            <p class="text-gray-600 dark:text-gray-400 mb-4">For 150-300 guests</p>
            <div class="text-3xl font-bold text-ocean-deep-600 mb-6">Custom Quote</div>
            <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400 mb-6">
              <li>• Full-day venue access</li>
              <li>• Luxury catering & open bar</li>
              <li>• Premium AV & lighting</li>
              <li>• Custom decor & floral</li>
              <li>• Dedicated event team</li>
              <li>• Photography package</li>
            </ul>
            <router-link to="/contact" class="btn-secondary w-full text-center block">
              Inquire
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-16 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto">
        <div class="bg-gradient-to-r from-purple-500 via-pink-500 to-rose-500 rounded-2xl p-8 md:p-12 text-center text-white">
          <h2 class="text-3xl font-bold mb-4">Let's Plan Your Event</h2>
          <p class="text-lg text-white/90 mb-8">
            Our event specialists are ready to bring your vision to life
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <router-link to="/contact" class="bg-white text-pink-600 px-8 py-4 rounded-full font-bold hover:bg-white/90 transition-all shadow-lg">
              Start Planning
            </router-link>
            <a href="tel:+201001234567" class="bg-white/20 text-white px-8 py-4 rounded-full font-bold hover:bg-white/30 transition-all border border-white/30">
              Call Events Team
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
  title: 'Events & Celebrations - الخيمة Beach Resort',
  description: 'Host weddings, corporate events, and celebrations at الخيمة Beach Resort. Beautiful venues on the Red Sea coast.',
  keywords: 'events, weddings, celebrations, corporate events, Red Sea venue, beach wedding'
})
</script>
