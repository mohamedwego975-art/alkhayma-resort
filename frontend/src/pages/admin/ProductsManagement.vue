<template>
  <div class="admin-management">
    <!-- Header -->
    <div class="management-header">
      <h1>{{ $t('admin.products') }}</h1>
      <div class="header-meta">
        <span class="badge">{{ products.length }} {{ $t('admin.total') }}</span>
      </div>
    </div>

    <!-- Error Banner -->
    <div v-if="error" class="error-banner" role="alert">
      <span>⚠️ {{ error }}</span>
      <button @click="error = null">✕</button>
    </div>

    <!-- Filter Tabs -->
    <div class="filter-tabs" role="tablist" aria-label="Product type filter">
      <button
        v-for="tab in tabs"
        :key="tab.value"
        :class="['tab-btn', { active: activeTab === tab.value }]"
        role="tab"
        :aria-selected="activeTab === tab.value"
        @click="activeTab = tab.value"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container" aria-busy="true">
      <div class="spinner"></div>
      <p>{{ $t('common.loading') }}</p>
    </div>

    <!-- Products Table -->
    <div v-else class="table-wrapper">
      <table class="data-table" aria-label="Products list">
        <thead>
          <tr>
            <th>{{ $t('admin.id') }}</th>
            <th>{{ $t('product.name') }}</th>
            <th>{{ $t('product.type') }}</th>
            <th>{{ $t('product.price') }}</th>
            <th>{{ $t('product.capacity') }}</th>
            <th>{{ $t('product.active') }}</th>
            <th>{{ $t('admin.created') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredProducts.length === 0">
            <td colspan="7" class="empty-row">{{ $t('admin.noProducts') }}</td>
          </tr>
          <tr v-for="product in filteredProducts" :key="product.id">
            <td>#{{ product.id }}</td>
            <td>
              <div class="product-name">
                <strong>{{ product.name }}</strong>
                <small>{{ product.name_ar }}</small>
              </div>
            </td>
            <td>
              <span :class="`type-badge type-${product.type?.toLowerCase()}`">
                {{ product.type?.toUpperCase() }}
              </span>
            </td>
            <td>EGP {{ Number(product.base_price).toFixed(2) }}</td>
            <td>{{ product.capacity }}</td>
            <td>
              <span :class="product.is_active ? 'active-pill yes' : 'active-pill no'">
                {{ product.is_active ? $t('common.active') : $t('common.inactive') }}
              </span>
            </td>
            <td>{{ formatDate(product.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import apiClient from '../../api/client'

interface Product {
  id: number
  name: string
  name_ar: string
  type: string
  base_price: number
  capacity: number
  is_active: boolean
  created_at: string
}

const products = ref<Product[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const activeTab = ref('all')

const tabs = [
  { value: 'all', label: 'All' },
  { value: 'beach', label: 'Beach' },
  { value: 'water_activity', label: 'Water' },
  { value: 'restaurant', label: 'Restaurant' },
  { value: 'event', label: 'Events' },
]

const filteredProducts = computed(() => {
  if (activeTab.value === 'all') return products.value
  return products.value.filter((p) => p.type?.toLowerCase() === activeTab.value)
})

async function fetchProducts() {
  loading.value = true
  error.value = null
  try {
    const response = await apiClient.get<Product[]>('/products')
    products.value = response.data
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { error?: string } } }
    error.value = axiosErr.response?.data?.error ?? 'Failed to load products'
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('ar-EG', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

onMounted(fetchProducts)
</script>

<style scoped>
.admin-management { padding: 1.5rem; }
.management-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}
.management-header h1 { font-size: 1.5rem; font-weight: 700; margin: 0; }
.badge {
  background: var(--color-primary, #4f46e5);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.85rem;
}
.filter-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}
.tab-btn {
  padding: 0.4rem 1rem;
  border-radius: 999px;
  border: 1px solid #d1d5db;
  background: white;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.15s;
}
.tab-btn.active {
  background: var(--color-primary, #4f46e5);
  color: white;
  border-color: transparent;
}
.error-banner {
  background: #fee2e2;
  border: 1px solid #f87171;
  color: #991b1b;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.error-banner button { background: none; border: none; cursor: pointer; font-size: 1rem; }
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 3rem;
  gap: 1rem;
  color: #6b7280;
}
.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid #e5e7eb;
  border-top-color: var(--color-primary, #4f46e5);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.table-wrapper { overflow-x: auto; }
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}
.data-table th {
  background: #f9fafb;
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
}
.data-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #f3f4f6;
  vertical-align: middle;
}
.data-table tr:hover td { background: #f9fafb; }
.empty-row { text-align: center; color: #9ca3af; padding: 2rem !important; }
.product-name { display: flex; flex-direction: column; gap: 0.1rem; }
.product-name small { color: #9ca3af; font-size: 0.8rem; }
.type-badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  background: #ede9fe;
  color: #5b21b6;
}
.type-badge.type-beach { background: #dbeafe; color: #1e40af; }
.type-badge.type-water_activity { background: #d1fae5; color: #065f46; }
.type-badge.type-restaurant { background: #fef3c7; color: #92400e; }
.active-pill {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}
.active-pill.yes { background: #d1fae5; color: #065f46; }
.active-pill.no { background: #f3f4f6; color: #6b7280; }
</style>
