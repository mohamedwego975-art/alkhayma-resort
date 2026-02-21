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
            <label class="block text-sm font-medium text-gray-700">Full Name</label>
            <input
              v-model="fullName"
              type="text"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Email</label>
            <input
              v-model="email"
              type="email"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Phone (optional)</label>
            <input
              v-model="phone"
              type="tel"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Password</label>
            <input
              v-model="password"
              type="password"
              required
              minlength="8"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
        </div>

        <button
          type="submit"
          :disabled="authStore.loading"
          class="w-full py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
        >
          {{ authStore.loading ? 'Loading...' : 'Register' }}
        </button>

        <div class="text-center">
          <router-link to="/login" class="text-sm text-blue-600 hover:text-blue-500">
            Already have an account?
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
