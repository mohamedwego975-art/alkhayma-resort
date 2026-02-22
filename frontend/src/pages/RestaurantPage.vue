<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <div class="relative bg-gradient-to-br from-amber-900 via-orange-800 to-red-700 py-20 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <span class="inline-block px-4 py-2 mb-4 text-sm font-medium text-white bg-white/10 backdrop-blur-md rounded-full border border-white/20">
          🍽️ Fine Dining
        </span>
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-4">
          Restaurant
        </h1>
        <p class="text-xl text-white/90 max-w-2xl mx-auto">
          Savor exquisite flavors with stunning Red Sea views
        </p>
      </div>
    </div>

    <!-- Restaurant Overview -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-950">
      <div class="max-w-6xl mx-auto">
        <div class="grid md:grid-cols-2 gap-12 items-center">
          <div class="order-2 md:order-1">
            <div class="aspect-square rounded-2xl bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center">
              <span class="text-9xl">🍽️</span>
            </div>
          </div>
          <div class="order-1 md:order-2">
            <span class="badge badge-primary mb-4">Main Restaurant</span>
            <h2 class="heading-display text-3xl md:text-4xl text-gray-900 dark:text-white mb-6">
              Al-Bahr Restaurant
            </h2>
            <p class="text-gray-600 dark:text-gray-400 mb-6">
              Experience culinary excellence at Al-Bahr (The Sea), our signature restaurant offering panoramic views of the Red Sea. Our executive chef combines international techniques with local Egyptian flavors.
            </p>
            <div class="space-y-4">
              <div class="flex items-center gap-3">
                <span class="text-2xl">🕐</span>
                <span class="text-gray-700 dark:text-gray-300">Breakfast: 7:00 AM - 10:30 AM</span>
              </div>
              <div class="flex items-center gap-3">
                <span class="text-2xl">🕐</span>
                <span class="text-gray-700 dark:text-gray-300">Lunch: 12:30 PM - 3:00 PM</span>
              </div>
              <div class="flex items-center gap-3">
                <span class="text-2xl">🕐</span>
                <span class="text-gray-700 dark:text-gray-300">Dinner: 7:00 PM - 11:00 PM</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Menu Highlights -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-gray-900">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <span class="badge badge-primary mb-4">Menu</span>
          <h2 class="heading-display text-3xl md:text-4xl text-gray-900 dark:text-white mb-4">
            Culinary Highlights
          </h2>
          <p class="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            A selection of our most beloved dishes crafted with passion
          </p>
        </div>

        <!-- Breakfast -->
        <div class="mb-12">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
            <span class="text-3xl">🌅</span>
            Breakfast Selection
          </h3>
          <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 hover:shadow-lg transition-shadow">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Egyptian Breakfast</h4>
                <span class="font-bold text-orange-600">$12</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Ful medames, falafel, eggs, pita bread, tahini</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 hover:shadow-lg transition-shadow">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Continental</h4>
                <span class="font-bold text-orange-600">$15</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Pastries, cold cuts, cheese, fresh fruit, coffee</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 hover:shadow-lg transition-shadow">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Sea View Pancakes</h4>
                <span class="font-bold text-orange-600">$14</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Fluffy pancakes with maple syrup and fresh berries</p>
            </div>
          </div>
        </div>

        <!-- Main Courses -->
        <div class="mb-12">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
            <span class="text-3xl">🍖</span>
            Main Courses
          </h3>
          <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 hover:shadow-lg transition-shadow">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Grilled Sea Bass</h4>
                <span class="font-bold text-orange-600">$28</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Fresh catch with lemon butter sauce, grilled vegetables</p>
              <span class="inline-block mt-2 px-2 py-1 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-400 text-xs rounded">Chef's Choice</span>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 hover:shadow-lg transition-shadow">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Lamb Tagine</h4>
                <span class="font-bold text-orange-600">$32</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Tender lamb with apricots, almonds, and Moroccan spices</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 hover:shadow-lg transition-shadow">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Ribeye Steak</h4>
                <span class="font-bold text-orange-600">$45</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Premium cut with truffle mashed potatoes</p>
              <span class="inline-block mt-2 px-2 py-1 bg-amber-100 dark:bg-amber-900 text-amber-700 dark:text-amber-400 text-xs rounded">Premium</span>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 hover:shadow-lg transition-shadow">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Seafood Platter</h4>
                <span class="font-bold text-orange-600">$55</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Lobster, prawns, calamari, and fish of the day</p>
              <span class="inline-block mt-2 px-2 py-1 bg-amber-100 dark:bg-amber-900 text-amber-700 dark:text-amber-400 text-xs rounded">For 2 People</span>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 hover:shadow-lg transition-shadow">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Vegetable Couscous</h4>
                <span class="font-bold text-orange-600">$18</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Traditional couscous with seasonal vegetables</p>
              <span class="inline-block mt-2 px-2 py-1 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-400 text-xs rounded">Vegetarian</span>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 hover:shadow-lg transition-shadow">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Pasta Primavera</h4>
                <span class="font-bold text-orange-600">$20</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Fresh pasta with garden vegetables and parmesan</p>
            </div>
          </div>
        </div>

        <!-- Desserts -->
        <div>
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
            <span class="text-3xl">🍰</span>
            Desserts
          </h3>
          <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 hover:shadow-lg transition-shadow">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Umm Ali</h4>
                <span class="font-bold text-orange-600">$10</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Traditional Egyptian bread pudding with nuts</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 hover:shadow-lg transition-shadow">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Chocolate Fondant</h4>
                <span class="font-bold text-orange-600">$14</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Warm chocolate cake with vanilla ice cream</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-xl p-6 hover:shadow-lg transition-shadow">
              <div class="flex justify-between items-start mb-3">
                <h4 class="font-bold text-gray-900 dark:text-white">Fresh Fruit Platter</h4>
                <span class="font-bold text-orange-600">$12</span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Seasonal tropical fruits</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Special Dining Experiences -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-950">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <span class="badge bg-amber-100 text-amber-800 mb-4">Special Experiences</span>
          <h2 class="heading-display text-3xl md:text-4xl text-gray-900 dark:text-white mb-4">
            Unforgettable Dining
          </h2>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div class="bg-gradient-to-br from-amber-50 to-orange-50 dark:from-gray-800 dark:to-gray-700 rounded-2xl p-8">
            <div class="text-4xl mb-4">🌅</div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">Sunset Dinner</h3>
            <p class="text-gray-600 dark:text-gray-400 mb-4">Romantic beachfront dining as the sun sets over the Red Sea.</p>
            <span class="text-amber-600 font-bold">$150 per couple</span>
          </div>

          <div class="bg-gradient-to-br from-amber-50 to-orange-50 dark:from-gray-800 dark:to-gray-700 rounded-2xl p-8">
            <div class="text-4xl mb-4">🎣</div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">Catch of the Day</h3>
            <p class="text-gray-600 dark:text-gray-400 mb-4">Choose your fresh fish from our display and have it prepared to your liking.</p>
            <span class="text-amber-600 font-bold">Market price</span>
          </div>

          <div class="bg-gradient-to-br from-amber-50 to-orange-50 dark:from-gray-800 dark:to-gray-700 rounded-2xl p-8">
            <div class="text-4xl mb-4">🍷</div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">Wine Pairing</h3>
            <p class="text-gray-600 dark:text-gray-400 mb-4">5-course tasting menu with carefully selected wine pairings.</p>
            <span class="text-amber-600 font-bold">$120 per person</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Reservation CTA -->
    <section class="py-16 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto">
        <div class="bg-gradient-to-r from-amber-600 to-orange-600 rounded-2xl p-8 md:p-12 text-center text-white">
          <h2 class="text-3xl font-bold mb-4">Reserve Your Table</h2>
          <p class="text-lg text-white/90 mb-8 max-w-2xl mx-auto">
            Secure the best spot with a view. We recommend booking in advance for dinner.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <router-link to="/booking" class="bg-white text-amber-600 px-8 py-4 rounded-full font-bold hover:bg-white/90 transition-all shadow-lg">
              Book a Table
            </router-link>
            <a href="tel:+201001234567" class="bg-white/20 text-white px-8 py-4 rounded-full font-bold hover:bg-white/30 transition-all border border-white/30">
              Call to Reserve
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
  title: 'Restaurant - الخيمة Beach Resort',
  description: 'Dine at Al-Bahr Restaurant with stunning Red Sea views. Enjoy international and Egyptian cuisine, fresh seafood, and special dining experiences.',
  keywords: 'restaurant, dining, Red Sea, seafood, Egyptian cuisine, fine dining'
})
</script>
