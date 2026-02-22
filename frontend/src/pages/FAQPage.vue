<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-5xl mx-auto">
      <h1 class="text-4xl font-bold text-center text-gray-900 mb-4">
        Project Pages Index
      </h1>
      <p class="text-center text-gray-600 mb-12">
        Complete list of all frontend and admin dashboard pages
      </p>

      <!-- Frontend Pages Section -->
      <div class="mb-12">
        <h2 class="text-2xl font-semibold text-gray-800 mb-6 pb-2 border-b-2 border-blue-500">
          Frontend Pages
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <router-link
            v-for="page in frontendPages"
            :key="page.path"
            :to="page.path"
            class="block p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-200 hover:border-blue-400"
          >
            <div class="flex items-center">
              <span class="text-2xl mr-3">{{ page.icon }}</span>
              <div>
                <h3 class="font-medium text-gray-900">{{ page.name }}</h3>
                <p class="text-sm text-gray-500">{{ page.path }}</p>
              </div>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Admin Dashboard Pages Section -->
      <div class="mb-12">
        <h2 class="text-2xl font-semibold text-gray-800 mb-6 pb-2 border-b-2 border-blue-500">
          Admin Dashboard Pages
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <router-link
            v-for="page in adminPages"
            :key="page.path"
            :to="page.path"
            class="block p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-200 hover:border-blue-400"
          >
            <div class="flex items-center">
              <span class="text-2xl mr-3">{{ page.icon }}</span>
              <div>
                <h3 class="font-medium text-gray-900">{{ page.name }}</h3>
                <p class="text-sm text-gray-500">{{ page.path }}</p>
              </div>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Auth Pages Section -->
      <div class="mb-12">
        <h2 class="text-2xl font-semibold text-gray-800 mb-6 pb-2 border-b-2 border-blue-500">
          Authentication Pages
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <router-link
            v-for="page in authPages"
            :key="page.path"
            :to="page.path"
            class="block p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-200 hover:border-blue-400"
          >
            <div class="flex items-center">
              <span class="text-2xl mr-3">{{ page.icon }}</span>
              <div>
                <h3 class="font-medium text-gray-900">{{ page.name }}</h3>
                <p class="text-sm text-gray-500">{{ page.path }}</p>
              </div>
            </div>
          </router-link>
        </div>
      </div>

      <!-- System Info -->
      <div class="bg-blue-50 rounded-lg p-6 mt-8">
        <h3 class="text-lg font-semibold text-blue-900 mb-4">
          System Information
        </h3>
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
import { computed } from 'vue'

interface PageInfo {
  name: string
  path: string
  icon: string
}

const frontendPages: PageInfo[] = [
  { name: 'Home', path: '/', icon: '🏠' },
  { name: 'Beach', path: '/beach', icon: '🏖️' },
  { name: 'Location', path: '/location', icon: '📍' },
  { name: 'Rooms', path: '/rooms', icon: '🛏️' },
  { name: 'Room Detail', path: '/rooms/:id', icon: '🚪' },
  { name: 'Dashboard', path: '/dashboard', icon: '📊' },
]

const adminPages: PageInfo[] = [
  { name: 'Admin Dashboard', path: '/admin', icon: '🎛️' },
  { name: 'Analytics', path: '/admin/analytics', icon: '📈' },
  { name: 'Bookings Management', path: '/admin/bookings', icon: '📅' },
  { name: 'Rooms Management', path: '/admin/rooms', icon: '🏨' },
  { name: 'Products Management', path: '/admin/products', icon: '🛍️' },
  { name: 'Users Management', path: '/admin/users', icon: '👥' },
  { name: 'Settings', path: '/admin/settings', icon: '⚙️' },
]

const authPages: PageInfo[] = [
  { name: 'Login', path: '/login', icon: '🔐' },
  { name: 'Register', path: '/register', icon: '📝' },
]

const totalPages = computed(() => {
  return frontendPages.length + adminPages.length + authPages.length
})
</script>
