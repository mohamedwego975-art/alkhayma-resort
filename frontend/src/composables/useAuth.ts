import { useAuthStore } from '@/stores/auth'

export function useAuth() {
  const authStore = useAuthStore()

  return {
    user: authStore.user,
    isAuthenticated: authStore.isAuthenticated,
    isAdmin: authStore.isAdmin,
    login: authStore.login,
    register: authStore.register,
    logout: authStore.logout,
    refreshToken: authStore.refreshToken,
  }
}
