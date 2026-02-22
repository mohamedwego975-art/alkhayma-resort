<template>
  <div class="stat-card">
    <div class="stat-header">
      <span class="stat-icon">{{ icon }}</span>
      <span class="stat-trend" :class="trend">
        {{ change }}
        {{ trend === 'up' ? '↑' : '↓' }}
      </span>
    </div>
    <div class="stat-value">{{ value }}</div>
    <div class="stat-title">{{ title }}</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  value: string
  change: string
  icon: string
  trend: 'up' | 'down'
}>()
</script>

<style scoped>
.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.stat-icon {
  font-size: 24px;
}

.stat-trend {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 12px;
}

.stat-trend.up {
  background: #d1fae5;
  color: #065f46;
}

.stat-trend.down {
  background: #fee2e2;
  color: #991b1b;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.stat-title {
  font-size: 14px;
  color: #6b7280;
}
</style>
