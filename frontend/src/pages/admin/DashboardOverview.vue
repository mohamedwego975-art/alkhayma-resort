<template>
  <div class="dashboard-overview">
    <!-- Page Title -->
    <div class="page-header">
      <h1>{{ $t('admin.dashboard') }}</h1>
      <p class="subtitle">{{ $t('admin.welcome') }}</p>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <StatCard
        v-for="stat in stats"
        :key="stat.key"
        :title="stat.title"
        :value="stat.value"
        :change="stat.change"
        :icon="stat.icon"
        :trend="stat.trend"
      />
    </div>

    <!-- Charts Row -->
    <div class="charts-row">
      <!-- Revenue Chart -->
      <div class="chart-card">
        <h3>{{ $t('analytics.revenue') }}</h3>
        <div class="chart-placeholder">
          <div class="bar-chart">
            <div
              v-for="(bar, index) in revenueData"
              :key="index"
              class="bar"
              :style="{ height: `${bar.value}%` }"
            >
              <span class="bar-label">{{ bar.label }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Occupancy Chart -->
      <div class="chart-card">
        <h3>{{ $t('analytics.occupancy') }}</h3>
        <div class="occupancy-stats">
          <div class="occupancy-circle">
            <div class="circle-value">{{ occupancyRate }}%</div>
            <div class="circle-label">{{ $t('analytics.current') }}</div>
          </div>
          <div class="occupancy-details">
            <div class="detail-item">
              <span class="label">{{ $t('analytics.occupied') }}:</span>
              <span class="value">{{ occupiedRooms }}</span>
            </div>
            <div class="detail-item">
              <span class="label">{{ $t('analytics.available') }}:</span>
              <span class="value">{{ availableRooms }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Bookings & Activity -->
    <div class="split-row">
      <!-- Recent Bookings -->
      <div class="panel">
        <div class="panel-header">
          <h3>{{ $t('admin.recentBookings') }}</h3>
          <router-link to="/admin/bookings" class="view-all">
            {{ $t('admin.viewAll') }} →
          </router-link>
        </div>
        <div class="bookings-list">
          <div
            v-for="booking in recentBookings"
            :key="booking.id"
            class="booking-item"
          >
            <div class="booking-info">
              <span class="guest-name">{{ booking.guest_name }}</span>
              <span class="booking-details">
                {{ booking.room_type }} • {{ formatDate(booking.check_in) }}
              </span>
            </div>
            <div class="booking-status" :class="booking.status">
              {{ $t(`booking.status.${booking.status}`) }}
            </div>
          </div>
        </div>
      </div>

      <!-- Popular Products -->
      <div class="panel">
        <div class="panel-header">
          <h3>{{ $t('admin.popularProducts') }}</h3>
          <router-link to="/admin/products" class="view-all">
            {{ $t('admin.viewAll') }} →
          </router-link>
        </div>
        <div class="products-list">
          <div
            v-for="(product, index) in popularProducts"
            :key="product.id"
            class="product-item"
          >
            <span class="rank">#{{ index + 1 }}</span>
            <span class="product-name">{{ product.name }}</span>
            <span class="product-bookings">{{ product.bookings }} {{ $t('admin.bookings') }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Alerts & Notifications -->
    <div class="alerts-panel" v-if="alerts.length > 0">
      <h3>{{ $t('admin.alerts') }}</h3>
      <div class="alerts-list">
        <div
          v-for="alert in alerts"
          :key="alert.id"
          class="alert-item"
          :class="alert.type"
        >
          <span class="alert-icon">{{ alert.icon }}</span>
          <span class="alert-message">{{ alert.message }}</span>
          <button class="alert-action" @click="handleAlert(alert)">
            {{ alert.action }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import StatCard from '@/components/admin/StatCard.vue'

const { t } = useI18n()

// Stats data
const stats = ref([
  { key: 'revenue', title: t('analytics.todayRevenue'), value: '$1,240', change: '+12%', icon: '💰', trend: 'up' as const },
  { key: 'bookings', title: t('analytics.activeBookings'), value: '23', change: '+5%', icon: '📅', trend: 'up' as const },
  { key: 'guests', title: t('analytics.totalGuests'), value: '45', change: '-2%', icon: '👥', trend: 'down' as const },
  { key: 'occupancy', title: t('analytics.occupancyRate'), value: '78%', change: '+8%', icon: '🏨', trend: 'up' as const },
])

// Revenue chart data
const revenueData = ref([
  { label: 'Mon', value: 45 },
  { label: 'Tue', value: 60 },
  { label: 'Wed', value: 75 },
  { label: 'Thu', value: 55 },
  { label: 'Fri', value: 80 },
  { label: 'Sat', value: 95 },
  { label: 'Sun', value: 70 },
])

// Occupancy data
const occupancyRate = ref(78)
const occupiedRooms = ref(18)
const availableRooms = ref(5)

// Recent bookings
const recentBookings = ref([
  { id: 1, guest_name: 'John Smith', room_type: 'Deluxe Suite', check_in: '2024-02-25', status: 'confirmed' },
  { id: 2, guest_name: 'Sarah Johnson', room_type: 'Standard Room', check_in: '2024-02-26', status: 'pending' },
  { id: 3, guest_name: 'Michael Brown', room_type: 'VIP Beach', check_in: '2024-02-27', status: 'confirmed' },
  { id: 4, guest_name: 'Emily Davis', room_type: 'Family Room', check_in: '2024-02-28', status: 'confirmed' },
])

// Popular products
const popularProducts = ref([
  { id: 1, name: 'VIP Beach Access', bookings: 45 },
  { id: 2, name: 'Deluxe Room', bookings: 38 },
  { id: 3, name: 'Spa Package', bookings: 32 },
  { id: 4, name: 'Water Activities', bookings: 28 },
])

// Alerts
const alerts = ref([
  { id: 1, type: 'warning', icon: '⚠️', message: '3 bookings pending confirmation', action: 'Review', link: '/admin/bookings' },
  { id: 2, type: 'info', icon: 'ℹ️', message: 'Maintenance scheduled for Room 101', action: 'View', link: '/admin/rooms' },
])

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

const handleAlert = (alert: any) => {
  // Handle alert action
  console.log('Handling alert:', alert)
}

onMounted(async () => {
  // Fetch real analytics data
  try {
    const response = await fetch('http://localhost:8000/api/analytics/dashboard')
    if (response.ok) {
      const data = await response.json()
      // Update stats with real data
      if (stats.value[0]) stats.value[0].value = `$${data.today_revenue}`
      if (stats.value[1]) stats.value[1].value = String(data.active_bookings)
      if (stats.value[2]) stats.value[2].value = String(data.total_customers)
      if (stats.value[3]) stats.value[3].value = `${data.occupancy_rate}%`
      occupancyRate.value = data.occupancy_rate
      occupiedRooms.value = data.occupied_rooms
      availableRooms.value = data.available_rooms
    }
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
  }
})
</script>

<style scoped>
.dashboard-overview {
  padding: 24px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.subtitle {
  color: #6b7280;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-card h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: #1f2937;
}

.chart-placeholder {
  height: 200px;
  display: flex;
  align-items: flex-end;
  padding: 20px 0;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  width: 100%;
  height: 100%;
  gap: 12px;
}

.bar {
  flex: 1;
  background: linear-gradient(to top, #667eea, #764ba2);
  border-radius: 6px 6px 0 0;
  min-height: 20px;
  position: relative;
  transition: opacity 0.2s;
}

.bar:hover {
  opacity: 0.8;
}

.bar-label {
  position: absolute;
  bottom: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 12px;
  color: #6b7280;
}

.occupancy-stats {
  display: flex;
  align-items: center;
  gap: 40px;
  padding: 20px 0;
}

.occupancy-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: conic-gradient(#667eea v-bind('occupancyRate * 3.6')deg, #e5e7eb 0deg);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.circle-value {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
}

.circle-label {
  font-size: 12px;
  color: #6b7280;
}

.occupancy-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.detail-item .label {
  color: #6b7280;
}

.detail-item .value {
  font-weight: 600;
  color: #1f2937;
}

.split-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.panel {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.panel-header h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: #1f2937;
}

.view-all {
  color: #667eea;
  text-decoration: none;
  font-size: 14px;
}

.bookings-list,
.products-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.booking-item,
.product-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
}

.booking-info {
  display: flex;
  flex-direction: column;
}

.guest-name {
  font-weight: 600;
  color: #1f2937;
}

.booking-details {
  font-size: 13px;
  color: #6b7280;
}

.booking-status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.booking-status.confirmed {
  background: #d1fae5;
  color: #065f46;
}

.booking-status.pending {
  background: #fef3c7;
  color: #92400e;
}

.product-item {
  gap: 12px;
}

.rank {
  font-weight: 700;
  color: #667eea;
  width: 24px;
}

.product-name {
  flex: 1;
  color: #1f2937;
}

.product-bookings {
  font-size: 13px;
  color: #6b7280;
}

.alerts-panel {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.alerts-panel h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: #1f2937;
}

.alerts-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.alert-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
}

.alert-item.warning {
  background: #fef3c7;
}

.alert-item.info {
  background: #dbeafe;
}

.alert-icon {
  font-size: 20px;
}

.alert-message {
  flex: 1;
  color: #1f2937;
}

.alert-action {
  background: none;
  border: none;
  color: #667eea;
  font-weight: 600;
  cursor: pointer;
  padding: 4px 12px;
}
</style>
