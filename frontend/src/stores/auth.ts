import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'
import type { User, AuthResponse } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(localStorage.getItem('access_token'))
  const refreshTokenValue = ref<string | null>(localStorage.getItem('refresh_token'))
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin = computed(() => user.value?.role === 'admin' || user.value?.role === 'superadmin')

  async function login(email: string, password: string) {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)

    const response = await api.post<AuthResponse>('/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    accessToken.value = response.data.access_token
    refreshTokenValue.value = response.data.refresh_token
    user.value = response.data.user

    localStorage.setItem('access_token', response.data.access_token)
    localStorage.setItem('refresh_token', response.data.refresh_token)

    return response.data
  }

  async function register(email: string, password: string, full_name: string, phone?: string) {
    const response = await api.post<AuthResponse>('/auth/register', {
      email, password, full_name, phone,
    })

    accessToken.value = response.data.access_token
    refreshTokenValue.value = response.data.refresh_token
    user.value = response.data.user

    localStorage.setItem('access_token', response.data.access_token)
    localStorage.setItem('refresh_token', response.data.refresh_token)

    return response.data
  }

  async function refreshToken() {
    if (!refreshTokenValue.value) throw new Error('No refresh token available')

    const response = await api.post<{ access_token: string }>('/auth/refresh', {
      refresh_token: refreshTokenValue.value,
    })

    accessToken.value = response.data.access_token
    localStorage.setItem('access_token', response.data.access_token)

    return response.data
  }

  async function fetchUser() {
    if (!accessToken.value) return
    const response = await api.get<User>('/auth/me')
    user.value = response.data
  }

  async function logout() {
    try {
      if (refreshTokenValue.value) {
        await api.post('/auth/logout', { refresh_token: refreshTokenValue.value })
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      accessToken.value = null
      refreshTokenValue.value = null
      user.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }

  if (accessToken.value) {
    fetchUser().catch(() => { logout() })
  }

  return {
    accessToken, refreshTokenValue, user, isAuthenticated, isAdmin,
    login, register, refreshToken, fetchUser, logout,
  }
})
