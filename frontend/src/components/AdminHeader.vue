<template>
  <header class="admin-header">
    <!-- Left: Mobile Toggle & Breadcrumb -->
    <div class="header-left">
      <button v-if="isMobile" class="mobile-toggle" @click="$emit('toggle-sidebar')">
        ☰
      </button>
      <Breadcrumb :breadcrumbs="breadcrumbItems" />
    </div>

    <!-- Right: Search, Notifications, User -->
    <div class="header-right">
      <!-- Search -->
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          :placeholder="$t('admin.search')"
          @keyup.enter="handleSearch"
        />
        <button @click="handleSearch">🔍</button>
      </div>

      <!-- Notifications -->
      <button class="notification-btn" @click="showNotifications = !showNotifications">
        <span class="icon">🔔</span>
        <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
      </button>

      <!-- Language Switcher -->
      <div class="language-switcher">
        <button @click="toggleLocale" class="locale-btn">
          {{ currentLocale === 'ar' ? '🇪🇬' : '🇬🇧' }}
        </button>
      </div>
    </div>

    <!-- Notifications Dropdown -->
    <div v-if="showNotifications" class="notifications-dropdown">
      <div class="notifications-header">
        <h4>{{ $t('admin.notifications') }}</h4>
        <button @click="markAllRead">{{ $t('admin.markAllRead') }}</button>
      </div>
      <div class="notifications-list">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="notification-item"
          :class="{ unread: !notification.read }"
          @click="markRead(notification.id)"
        >
          <span class="notification-icon">{{ notification.icon }}</span>
          <div class="notification-content">
            <p class="notification-title">{{ notification.title }}</p>
            <p class="notification-time">{{ notification.time }}</p>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import Breadcrumb from './Breadcrumb.vue'

const { t, locale } = useI18n()
const route = useRoute()

const props = defineProps<{
  isMobile?: boolean
}>()

defineEmits<{
  'toggle-sidebar': []
}>()

const searchQuery = ref('')
const showNotifications = ref(false)
const currentLocale = computed(() => locale.value)

const breadcrumbItems = computed(() => {
  const paths = route.path.split('/').filter(Boolean)
  return paths.map((path, index) => ({
    label: t(`admin.${path}`) || path,
    path: '/' + paths.slice(0, index + 1).join('/')
  }))
})

const unreadCount = ref(3)
const notifications = ref([
  { id: 1, title: t('admin.newBooking'), icon: '📅', time: '2 min ago', read: false },
  { id: 2, title: t('admin.newReview'), icon: '⭐', time: '1 hour ago', read: false },
  { id: 3, title: t('admin.systemUpdate'), icon: '⚙️', time: '3 hours ago', read: true },
])

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    // Implement search functionality
    console.log('Searching for:', searchQuery.value)
  }
}

const toggleLocale = () => {
  locale.value = locale.value === 'ar' ? 'en' : 'ar'
  localStorage.setItem('locale', locale.value)
}

const markRead = (id: number) => {
  const notification = notifications.value.find(n => n.id === id)
  if (notification) {
    notification.read = true
    unreadCount.value = notifications.value.filter(n => !n.read).length
  }
}

const markAllRead = () => {
  notifications.value.forEach(n => n.read = true)
  unreadCount.value = 0
}

// Close notifications when clicking outside
watch(showNotifications, (value) => {
  if (value) {
    setTimeout(() => {
      document.addEventListener('click', closeNotifications, { once: true })
    }, 100)
  }
})

const closeNotifications = () => {
  showNotifications.value = false
}
</script>

<style scoped>
.admin-header {
  height: 64px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.mobile-toggle {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 8px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.search-box {
  display: flex;
  align-items: center;
  background: #f3f4f6;
  border-radius: 8px;
  padding: 4px 12px;
}

.search-box input {
  border: none;
  background: none;
  outline: none;
  padding: 4px 8px;
  width: 200px;
}

.search-box button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
}

.notification-btn {
  position: relative;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 8px;
}

.badge {
  position: absolute;
  top: 0;
  right: 0;
  background: #ef4444;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.locale-btn {
  background: none;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 6px 10px;
  cursor: pointer;
  font-size: 18px;
}

.notifications-dropdown {
  position: absolute;
  top: 64px;
  right: 24px;
  width: 320px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  z-index: 200;
}

.notifications-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.notifications-header h4 {
  margin: 0;
  font-size: 16px;
}

.notifications-header button {
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  font-size: 12px;
}

.notifications-list {
  max-height: 300px;
  overflow-y: auto;
}

.notification-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: background 0.2s;
}

.notification-item:hover {
  background: #f9fafb;
}

.notification-item.unread {
  background: #eff6ff;
}

.notification-icon {
  font-size: 20px;
}

.notification-content {
  flex: 1;
}

.notification-title {
  margin: 0;
  font-size: 14px;
  color: #1f2937;
}

.notification-time {
  margin: 4px 0 0 0;
  font-size: 12px;
  color: #6b7280;
}
</style>
