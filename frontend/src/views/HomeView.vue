<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="text-2xl font-bold text-blue-600">
              🏖️ الخيمة Resort
            </router-link>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/rooms" class="text-gray-700 hover:text-blue-600">Rooms</router-link>
            <template v-if="authStore.isAuthenticated">
              <router-link to="/account" class="text-gray-700 hover:text-blue-600">Account</router-link>
              <button @click="handleLogout" class="text-gray-700 hover:text-blue-600">Logout</button>
            </template>
            <template v-else>
              <router-link to="/login" class="text-gray-700 hover:text-blue-600">Login</router-link>
              <router-link to="/register" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                Register
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-12 px-4">
      <div class="text-center mb-12">
        <h1 class="text-5xl font-bold text-gray-900 mb-4">Welcome to الخيمة Beach Resort</h1>
        <p class="text-xl text-gray-600">Experience luxury by the sea</p>
      </div>

      <div class="grid md:grid-cols-3 gap-8 mb-12">
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-xl font-bold mb-2">🏨 Luxury Rooms</h3>
          <p class="text-gray-600">Comfortable rooms with stunning sea views</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-xl font-bold mb-2">🌊 Beach Access</h3>
          <p class="text-gray-600">Private beach with water sports</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-xl font-bold mb-2">🍽️ Fine Dining</h3>
          <p class="text-gray-600">Restaurant and cafe with local cuisine</p>
        </div>
      </div>

      <div class="text-center">
        <router-link 
          to="/rooms" 
          class="inline-block px-8 py-3 bg-blue-600 text-white text-lg rounded-lg hover:bg-blue-700"
        >
          Browse Rooms
        </router-link>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

function handleLogout() {
  authStore.logout()
  router.push('/')
}
</script>
