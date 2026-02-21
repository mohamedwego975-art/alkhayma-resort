<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="text-center text-3xl font-bold text-gray-900">
          {{ $t('auth.register') }}
        </h2>
      </div>
      
      <form @submit.prevent="handleRegister" class="mt-8 space-y-6">
        <div v-if="authStore.error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {{ authStore.error }}
        </div>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">{{ $t('auth.fullName') }}</label>
            <input
              v-model="fullName"
              type="text"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-ocean-deep-500 focus:border-ocean-deep-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">{{ $t('auth.email') }}</label>
            <input
              v-model="email"
              type="email"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-ocean-deep-500 focus:border-ocean-deep-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">{{ $t('auth.phone') }}</label>
            <input
              v-model="phone"
              type="tel"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-ocean-deep-500 focus:border-ocean-deep-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">{{ $t('auth.password') }}</label>
            <input
              v-model="password"
              type="password"
              required
              minlength="8"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-ocean-deep-500 focus:border-ocean-deep-500"
            />
          </div>
        </div>

        <button
          type="submit"
          :disabled="authStore.loading"
          class="btn-primary w-full disabled:opacity-50"
        >
          {{ authStore.loading ? $t('common.loading') : $t('auth.registerButton') }}
        </button>

        <div class="text-center">
          <router-link to="/login" class="text-sm text-ocean-deep-600 hover:text-ocean-deep-500">
            {{ $t('auth.haveAccount') }}
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
const fullName = ref('')
const phone = ref('')

async function handleRegister() {
  const success = await authStore.register(
    email.value,
    password.value,
    fullName.value,
    phone.value || undefined
  )
  if (success) {
    router.push('/')
  }
}
</script>
