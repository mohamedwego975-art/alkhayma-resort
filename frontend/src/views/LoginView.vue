<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="text-center text-3xl font-bold text-gray-900">
          {{ $t('auth.login') }}
        </h2>
      </div>
      
      <form @submit.prevent="handleLogin" class="mt-8 space-y-6">
        <div v-if="authStore.error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {{ authStore.error }}
        </div>

        <div class="space-y-4">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              {{ $t('auth.email') }}
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-ocean-deep-500 focus:border-ocean-deep-500"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              {{ $t('auth.password') }}
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-ocean-deep-500 focus:border-ocean-deep-500"
            />
          </div>
        </div>

        <button
          type="submit"
          :disabled="authStore.loading"
          class="btn-primary w-full disabled:opacity-50"
        >
          {{ authStore.loading ? $t('common.loading') : $t('auth.loginButton') }}
        </button>

        <div class="text-center">
          <router-link to="/register" class="text-sm text-ocean-deep-600 hover:text-ocean-deep-500">
            {{ $t('auth.noAccount') }}
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')

async function handleLogin() {
  const success = await authStore.login(email.value, password.value)
  if (success) {
    router.push('/')
  }
}
</script>
