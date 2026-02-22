<template>
  <div class="admin-management">
    <!-- Header with Search -->
    <div class="header-section">
      <div class="management-header">
        <h1>{{ $t("admin.users") }}</h1>
        <div class="header-meta">
          <span class="badge">{{ filteredUsers.length }} {{ $t("admin.total") }}</span>
        </div>
      </div>

      <!-- Filter Bar -->
      <div class="filter-bar">
        <input
          v-model="searchQuery"
          type="text"
          :placeholder="$t('common.search')"
          class="search-input"
          aria-label="Search users by name or email"
        />
        <select v-model="filterRole" class="filter-select" aria-label="Filter by role">
          <option value="">{{ $t("common.allRoles") }}</option>
          <option value="admin">Admin</option>
          <option value="staff">Staff</option>
          <option value="guest">Guest</option>
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

    <!-- Users Table -->
    <div v-else class="table-wrapper">
      <table class="data-table" aria-label="Users list">
        <thead>
          <tr>
            <th>{{ $t("admin.id") }}</th>
            <th>{{ $t("user.name") }}</th>
            <th>{{ $t("user.email") }}</th>
            <th>{{ $t("user.phone") }}</th>
            <th>{{ $t("user.role") }}</th>
            <th>{{ $t("user.active") }}</th>
            <th>{{ $t("admin.created") }}</th>
            <th>{{ $t("admin.actions") }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredUsers.length === 0">
            <td colspan="8" class="empty-row">{{ $t("admin.noUsers") }}</td>
          </tr>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>#{{ user.id }}</td>
            <td>
              <strong>{{ user.full_name }}</strong>
            </td>
            <td>
              <a :href="`mailto:${user.email}`" class="email-link">{{ user.email }}</a>
            </td>
            <td>{{ user.phone ?? "—" }}</td>
            <td>
              <span :class="`role-badge role-${user.role?.toLowerCase()}`">
                {{ user.role?.toUpperCase() }}
              </span>
            </td>
            <td>
              <button
                v-if="user.is_active"
                @click="toggleUserActive(user.id, false)"
                :disabled="updatingId === user.id"
                class="action-btn active"
              >
                Deactivate
              </button>
              <button
                v-else
                @click="toggleUserActive(user.id, true)"
                :disabled="updatingId === user.id"
                class="action-btn inactive"
              >
                Activate
              </button>
            </td>
            <td>{{ formatDate(user.created_at) }}</td>
            <td>
              <div class="action-group">
                <button
                  @click="deleteUser(user.id)"
                  :disabled="updatingId === user.id"
                  class="action-btn-icon danger"
                  title="Delete user"
                >
                  ✕
                </button>
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
import { authApi, type User } from "../../api/auth";

const users = ref<User[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const success = ref<string | null>(null);
const updatingId = ref<number | null>(null);
const searchQuery = ref("");
const filterRole = ref("");

const filteredUsers = computed(() => {
  return users.value.filter((user) => {
    const matchesSearch =
      user.full_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      user.email.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesRole = !filterRole.value || user.role === filterRole.value;
    return matchesSearch && matchesRole;
  });
});

async function fetchUsers() {
  loading.value = true;
  error.value = null;
  try {
    const response = await authApi.adminGetAllUsers();
    users.value = response.data;
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { error?: string } } };
    error.value = axiosErr.response?.data?.error ?? "Failed to load users";
  } finally {
    loading.value = false;
  }
}

async function toggleUserActive(userId: number, isActive: boolean) {
  updatingId.value = userId;
  error.value = null;
  try {
    await authApi.adminToggleUserActive(userId, isActive);
    const idx = users.value.findIndex((u) => u.id === userId);
    if (idx !== -1 && users.value[idx]) {
      users.value[idx]!.is_active = isActive;
    }
    success.value = `User ${isActive ? "activated" : "deactivated"}`;
    setTimeout(() => (success.value = null), 3000);
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { error?: string } } };
    error.value = axiosErr.response?.data?.error ?? "Failed to update user";
  } finally {
    updatingId.value = null;
  }
}

async function deleteUser(userId: number) {
  if (!confirm("Are you sure you want to delete this user? This action cannot be undone.")) return;
  updatingId.value = userId;
  error.value = null;
  try {
    await authApi.adminDeleteUser(userId);
    users.value = users.value.filter((u) => u.id !== userId);
    success.value = "User deleted successfully";
    setTimeout(() => (success.value = null), 3000);
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { error?: string } } };
    error.value = axiosErr.response?.data?.error ?? "Failed to delete user";
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

onMounted(fetchUsers);
</script>

<style scoped>
.admin-management {
  padding: 1.5rem;
}
.management-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.management-header h1 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}
.badge {
  background: var(--color-primary, #4f46e5);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.85rem;
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
.error-banner button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
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
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
.table-wrapper {
  overflow-x: auto;
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
.email-link {
  color: var(--color-primary, #4f46e5);
  text-decoration: none;
}
.email-link:hover {
  text-decoration: underline;
}
.role-badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}
.role-badge.role-admin {
  background: #fef3c7;
  color: #92400e;
}
.role-badge.role-staff {
  background: #dbeafe;
  color: #1e40af;
}
.role-badge.role-guest {
  background: #f3f4f6;
  color: #374151;
}
.active-pill {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}
.active-pill.yes {
  background: #d1fae5;
  color: #065f46;
}
.active-pill.no {
  background: #f3f4f6;
  color: #6b7280;
}

/* New Styles */
.header-section {
  margin-bottom: 1.5rem;
}
.management-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}
.header-meta {
  display: flex;
  gap: 1rem;
  align-items: center;
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
.success-banner {
  background: #d1fae5;
  border: 1px solid #6ee7b7;
  color: #065f46;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.success-banner button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}
.action-btn {
  padding: 0.35rem 0.7rem;
  border: none;
  border-radius: 0.3rem;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
}
.action-btn.active {
  background: #fee2e2;
  color: #991b1b;
}
.action-btn.active:hover:not(:disabled) {
  background: #f87171;
  color: white;
}
.action-btn.inactive {
  background: #d1fae5;
  color: #065f46;
}
.action-btn.inactive:hover:not(:disabled) {
  background: #6ee7b7;
  color: white;
}
.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.action-group {
  display: flex;
  gap: 0.5rem;
}
.action-btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.75rem;
  height: 1.75rem;
  padding: 0;
  border: 1px solid #d1d5db;
  border-radius: 0.3rem;
  background: white;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}
.action-btn-icon:hover:not(:disabled) {
  background: #f3f4f6;
  border-color: #9ca3af;
}
.action-btn-icon.danger:hover:not(:disabled) {
  background: #fee2e2;
  border-color: #f87171;
  color: #991b1b;
}
.action-btn-icon:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
