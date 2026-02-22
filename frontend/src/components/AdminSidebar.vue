<template>
  <aside class="admin-sidebar" :class="{ 'collapsed': isCollapsed, 'mobile-open': isMobileOpen }">
    <!-- Logo -->
    <div class="sidebar-header">
      <div class="logo">
        <span class="logo-icon">🏖️</span>
        <span v-if="!isCollapsed" class="logo-text">{{ $t('admin.title') }}</span>
      </div>
      <button v-if="isMobile" class="mobile-close" @click="$emit('close')">
        ✕
      </button>
    </div>

    <!-- Navigation -->
    <nav class="sidebar-nav">
      <div class="nav-section">
        <span v-if="!isCollapsed" class="section-title">{{ $t('admin.main') }}</span>
        <router-link
          v-for="item in mainNavItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ 'active': $route.path === item.path }"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span v-if="!isCollapsed" class="nav-text">{{ item.name }}</span>
          <span v-if="!isCollapsed && item.badge" class="nav-badge">{{ item.badge }}</span>
        </router-link>
      </div>

      <div class="nav-section">
        <span v-if="!isCollapsed" class="section-title">{{ $t('admin.management') }}</span>
        <router-link
          v-for="item in managementNavItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ 'active': $route.path === item.path }"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span v-if="!isCollapsed" class="nav-text">{{ item.name }}</span>
          <span v-if="!isCollapsed && item.badge" class="nav-badge">{{ item.badge }}</span>
        </router-link>
      </div>

      <div class="nav-section">
        <span v-if="!isCollapsed" class="section-title">{{ $t('admin.system') }}</span>
        <router-link
          v-for="item in systemNavItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ 'active': $route.path === item.path }"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span v-if="!isCollapsed" class="nav-text">{{ item.name }}</span>
        </router-link>
      </div>
    </nav>

    <!-- User Profile -->
    <div class="sidebar-footer">
      <div class="user-profile" v-if="!isCollapsed">
        <div class="user-avatar">👤</div>
        <div class="user-info">
          <span class="user-name">{{ user?.full_name || 'Admin' }}</span>
          <span class="user-role">{{ user?.role || 'Administrator' }}</span>
        </div>
      </div>
      <button v-else class="user-avatar-small">👤</button>
      
      <button class="logout-btn" @click="logout" :title="$t('auth.logout')">
        <span class="nav-icon">🚪</span>
        <span v-if="!isCollapsed">{{ $t('auth.logout') }}</span>
      </button>
    </div>

    <!-- Toggle Button (Desktop) -->
    <button
      v-if="!isMobile"
      class="toggle-btn"
      @click="$emit('toggle')"
      :title="isCollapsed ? $t('admin.expand') : $t('admin.collapse')"
    >
      {{ isCollapsed ? '→' : '←' }}
    </button>
  </aside>

  <!-- Mobile Overlay -->
  <div
    v-if="isMobile && isMobileOpen"
    class="mobile-overlay"
    @click="$emit('close')"
  ></div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const router = useRouter()
const authStore = useAuthStore()

const props = defineProps<{
  isCollapsed: boolean
  isMobileOpen?: boolean
}>()

defineEmits<{
  toggle: []
  close: []
}>()

const isMobile = computed(() => window.innerWidth < 768)
const user = computed(() => authStore.user)

const mainNavItems = [
  { path: '/admin', icon: '📊', name: t('admin.dashboard'), badge: null },
  { path: '/admin/analytics', icon: '📈', name: t('admin.analytics'), badge: null },
]

const managementNavItems = [
  { path: '/admin/bookings', icon: '📅', name: t('admin.bookings'), badge: 12 },
  { path: '/admin/rooms', icon: '🏨', name: t('admin.rooms'), badge: null },
  { path: '/admin/products', icon: '🏖️', name: t('admin.products'), badge: null },
  { path: '/admin/users', icon: '👥', name: t('admin.users'), badge: null },
]

const systemNavItems = [
  { path: '/admin/settings', icon: '⚙️', name: t('admin.settings'), badge: null },
  { path: '/admin/logs', icon: '📝', name: t('admin.logs'), badge: null },
]

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.admin-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 260px;
  background: #1e293b;
  color: white;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  z-index: 1000;
}

.admin-sidebar.collapsed {
  width: 80px;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 28px;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  color: white;
}

.mobile-close {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
}

.sidebar-nav {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: 24px;
}

.section-title {
  display: block;
  padding: 0 20px;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.2s;
  position: relative;
}

.nav-item:hover,
.nav-item.active {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: #667eea;
}

.nav-icon {
  font-size: 20px;
  width: 24px;
  text-align: center;
}

.nav-text {
  font-size: 14px;
  flex: 1;
}

.nav-badge {
  background: #ef4444;
  color: white;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 600;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #667eea;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.user-avatar-small {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #667eea;
  border: none;
  cursor: pointer;
  font-size: 20px;
  margin-bottom: 12px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
}

.user-role {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 10px;
  background: rgba(239, 68, 68, 0.2);
  border: none;
  border-radius: 8px;
  color: #ef4444;
  cursor: pointer;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.3);
}

.toggle-btn {
  position: absolute;
  top: 50%;
  right: -12px;
  width: 24px;
  height: 24px;
  background: #667eea;
  border: none;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  transform: translateY(-50%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

@media (max-width: 768px) {
  .admin-sidebar {
    transform: translateX(-100%);
    width: 260px !important;
  }
  
  .admin-sidebar.mobile-open {
    transform: translateX(0);
  }
  
  .toggle-btn {
    display: none;
  }
}
</style>
