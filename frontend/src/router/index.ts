import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/pages/HomePage.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue')
    },
    {
      path: '/rooms',
      name: 'rooms',
      component: () => import('@/pages/RoomsPage.vue')
    },
    {
      path: '/rooms/:slug',
      name: 'room-detail',
      component: () => import('@/pages/RoomDetailPage.vue')
    },
    {
      path: '/beach',
      name: 'beach',
      component: () => import('@/pages/BeachPage.vue')
    },
    {
      path: '/location',
      name: 'location',
      component: () => import('@/pages/LocationPage.vue')
    },
    {
      path: '/booking/:productId?',
      name: 'booking',
      component: () => import('@/views/BookingView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/booking/confirm',
      name: 'booking-confirm',
      component: () => import('@/views/BookingView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/account',
      name: 'account',
      component: () => import('@/views/AccountView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/pages/DashboardPage.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        {
          path: '',
          name: 'admin-dashboard',
          component: () => import('@/pages/admin/DashboardOverview.vue')
        },
        {
          path: 'analytics',
          name: 'admin-analytics',
          component: () => import('@/pages/admin/DashboardOverview.vue')
        },
        {
          path: 'bookings',
          name: 'admin-bookings',
          component: () => import('@/pages/admin/BookingsManagement.vue')
        },
        {
          path: 'rooms',
          name: 'admin-rooms',
          component: () => import('@/pages/admin/RoomsManagement.vue')
        },
        {
          path: 'products',
          name: 'admin-products',
          component: () => import('@/pages/admin/ProductsManagement.vue')
        },
        {
          path: 'users',
          name: 'admin-users',
          component: () => import('@/pages/admin/UsersManagement.vue')
        },
        {
          path: 'settings',
          name: 'admin-settings',
          component: () => import('@/pages/admin/SettingsPage.vue')
        }
      ]
    }
  ]
})

router.beforeEach(async (to, _from, next) => {
  const { useAuthStore } = await import('@/stores/auth')
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresAdmin && authStore.user?.role !== 'admin') {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
