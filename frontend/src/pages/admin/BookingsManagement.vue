<template>
  <div class="admin-management">
    <!-- Header with Filters -->
    <div class="header-section">
      <div class="management-header">
        <h1>{{ $t("admin.bookings") }}</h1>
        <div class="header-meta">
          <span class="badge">{{ filteredBookings.length }} {{ $t("admin.total") }}</span>
        </div>
      </div>

      <!-- Filter Bar -->
      <div class="filter-bar">
        <input
          v-model="searchQuery"
          type="text"
          :placeholder="$t('common.search')"
          class="search-input"
          aria-label="Search bookings by ID, user, or room"
        />
        <select v-model="filterStatus" class="filter-select" aria-label="Filter by status">
          <option value="">{{ $t("common.allStatuses") }}</option>
          <option value="pending">Pending</option>
          <option value="confirmed">Confirmed</option>
          <option value="checked_in">Checked In</option>
          <option value="checked_out">Checked Out</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>
    </div>

    <!-- Error Banner -->
    <div v-if="error" class="error-banner" role="alert">
      <span>⚠️ {{ error }}</span>
      <button @click="error = null">✕</button>
    </div>

    <!-- Success Banner -->
    <div v-if="success" class="success-banner" role="status">
      <span>✓ {{ success }}</span>
      <button @click="success = null">✕</button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container" aria-busy="true">
      <div class="spinner"></div>
      <p>{{ $t("common.loading") }}</p>
    </div>

    <!-- Bookings Table -->
    <div v-else class="table-wrapper">
      <table class="data-table" aria-label="Bookings list">
        <thead>
          <tr>
            <th>{{ $t("admin.id") }}</th>
            <th>{{ $t("booking.user") }}</th>
            <th>{{ $t("booking.room") }}</th>
            <th>{{ $t("booking.checkIn") }}</th>
            <th>{{ $t("booking.checkOut") }}</th>
            <th>{{ $t("booking.guests") }}</th>
            <th>{{ $t("booking.total") }}</th>
            <th>{{ $t("booking.status") }}</th>
            <th>{{ $t("admin.actions") }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredBookings.length === 0">
            <td colspan="9" class="empty-row">{{ $t("admin.noBookings") }}</td>
          </tr>
          <tr
            v-for="booking in filteredBookings"
            :key="booking.id"
            :class="`status-${booking.status}`"
          >
            <td>#{{ booking.id }}</td>
            <td>{{ booking.user_id }}</td>
            <td>{{ booking.room_id }}</td>
            <td>{{ formatDate(booking.check_in) }}</td>
            <td>{{ formatDate(booking.check_out) }}</td>
            <td>{{ booking.guests }}</td>
            <td>EGP {{ booking.total_price.toFixed(2) }}</td>
            <td>
              <span :class="`status-badge status-${booking.status}`">
                {{ booking.status.toUpperCase() }}
              </span>
            </td>
            <td>
              <div class="action-group">
                <select
                  :id="`status-select-${booking.id}`"
                  :value="booking.status"
                  :disabled="updatingId === booking.id"
                  class="status-select"
                  aria-label="Change booking status"
                  @change="(e) => updateStatus(booking.id, (e.target as HTMLSelectElement).value)"
                >
                  <option value="pending">PENDING</option>
                  <option value="confirmed">CONFIRMED</option>
                  <option value="checked_in">CHECKED IN</option>
                  <option value="checked_out">CHECKED OUT</option>
                  <option value="cancelled">CANCELLED</option>
                </select>
                <span
                  v-if="updatingId === booking.id"
                  class="mini-spinner"
                  aria-label="Updating..."
                ></span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { bookingApi, type Booking } from "../../api/bookings";

const bookings = ref<Booking[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const success = ref<string | null>(null);
const updatingId = ref<number | null>(null);
const searchQuery = ref("");
const filterStatus = ref("");

const filteredBookings = computed(() => {
  return bookings.value.filter((booking) => {
    const matchesSearch =
      booking.id.toString().includes(searchQuery.value) ||
      booking.user_id.toString().includes(searchQuery.value) ||
      booking.room_id.toString().includes(searchQuery.value);
    const matchesStatus = !filterStatus.value || booking.status === filterStatus.value;
    return matchesSearch && matchesStatus;
  });
});

async function fetchBookings() {
  loading.value = true;
  error.value = null;
  try {
    const response = await bookingApi.adminGetAll();
    bookings.value = response.data;
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { error?: string } } };
    error.value = axiosErr.response?.data?.error ?? "Failed to load bookings";
  } finally {
    loading.value = false;
  }
}

async function updateStatus(bookingId: number, status: string) {
  updatingId.value = bookingId;
  error.value = null;
  try {
    const response = await bookingApi.adminUpdateStatus(bookingId, status);
    const index = bookings.value.findIndex((b) => b.id === bookingId);
    if (index !== -1 && bookings.value[index]) {
      bookings.value[index] = { ...bookings.value[index], status: response.data.status };
    }
    success.value = "Booking status updated successfully";
    setTimeout(() => (success.value = null), 3000);
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { error?: string } } };
    error.value = axiosErr.response?.data?.error ?? "Failed to update booking status";
  } finally {
    updatingId.value = null;
  }
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("ar-EG", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

onMounted(fetchBookings);
</script>

<style scoped>
.admin-management {
  padding: 1.5rem;
}
.header-section {
  margin-bottom: 1.5rem;
}
.management-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}
.management-header h1 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}
.header-meta {
  display: flex;
  gap: 1rem;
  align-items: center;
}
.badge {
  background: var(--color-primary, #4f46e5);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.85rem;
}
.error-banner,
.success-banner {
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.error-banner {
  background: #fee2e2;
  border: 1px solid #f87171;
  color: #991b1b;
}
.success-banner {
  background: #d1fae5;
  border: 1px solid #6ee7b7;
  color: #065f46;
}
.error-banner button,
.success-banner button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.filter-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.search-input,
.filter-select {
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.9rem;
}
.search-input {
  flex: 1;
}
.filter-select {
  min-width: 150px;
}
.search-input:focus,
.filter-select:focus {
  outline: none;
  border-color: var(--color-primary, #4f46e5);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

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
.mini-spinner {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid #e5e7eb;
  border-top-color: var(--color-primary, #4f46e5);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
.table-wrapper {
  overflow-x: auto;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}
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
.data-table tr:hover td {
  background: #f9fafb;
}
.empty-row {
  text-align: center;
  color: #9ca3af;
  padding: 2rem !important;
}
.status-badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}
.status-badge.status-pending {
  background: #fef3c7;
  color: #92400e;
}
.status-badge.status-confirmed {
  background: #d1fae5;
  color: #065f46;
}
.status-badge.status-checked_in {
  background: #dbeafe;
  color: #1e40af;
}
.status-badge.status-checked_out {
  background: #f3f4f6;
  color: #374151;
}
.status-badge.status-cancelled {
  background: #fee2e2;
  color: #991b1b;
}
.action-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.status-select {
  font-size: 0.85rem;
  padding: 0.35rem 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background: white;
  cursor: pointer;
}
.status-select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
