import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type User } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function login(email: string, password: string) {
    loading.value = true
    error.value = null
    try {
      const response = await authApi.login({ email, password })
      token.value = response.data.access_token
      localStorage.setItem('token', response.data.access_token)
      await fetchUser()
      return true
    } catch (e: any) {
      error.value = e.response?.data?.error || 'Login failed'
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(email: string, password: string, full_name: string, phone?: string) {
    loading.value = true
    error.value = null
    try {
      const response = await authApi.register({ email, password, full_name, phone })
      user.value = response.data
      await login(email, password)
      return true
    } catch (e: any) {
      error.value = e.response?.data?.error || 'Registration failed'
      return false
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    if (!token.value) return
    try {
      const response = await authApi.getMe()
      user.value = response.data
    } catch (e) {
      logout()
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    login,
    register,
    fetchUser,
    logout,
  }
})
