import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(localStorage.getItem('access_token'))
  const refreshTokenValue = ref<string | null>(localStorage.getItem('refresh_token'))
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin = computed(() => user.value?.role === 'admin' || user.value?.role === 'superadmin')

  async function login(email: string, _password: string) {
    // Mock implementation for now
    const mockUser: User = {
      id: 1,
      email,
      full_name: 'Test User',
      role: 'guest'
    }
    
    accessToken.value = 'mock-token'
    refreshTokenValue.value = 'mock-refresh-token'
    user.value = mockUser

    localStorage.setItem('access_token', 'mock-token')
    localStorage.setItem('refresh_token', 'mock-refresh-token')

    return { access_token: 'mock-token', refresh_token: 'mock-refresh-token', user: mockUser }
  }

  async function logout() {
    accessToken.value = null
    refreshTokenValue.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return {
    accessToken, refreshTokenValue, user, isAuthenticated, isAdmin,
    login, logout,
  }
})
