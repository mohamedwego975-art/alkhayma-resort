import { useAuthStore } from '@/stores/auth'

export function useAuth() {
  const authStore = useAuthStore()

  return {
    user: authStore.user,
    isAuthenticated: authStore.isAuthenticated,
    isAdmin: authStore.isAdmin,
    login: authStore.login,
    logout: authStore.logout,
  }
}
