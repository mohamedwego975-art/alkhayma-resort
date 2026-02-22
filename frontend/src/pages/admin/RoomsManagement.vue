<template>
  <div class="admin-management">
    <!-- Header with Actions -->
    <div class="header-section">
      <div class="management-header">
        <h1>{{ $t("admin.rooms") }}</h1>
        <div class="header-meta">
          <span class="badge">{{ filteredRooms.length }} {{ $t("admin.total") }}</span>
          <button class="btn btn-primary" @click="showAddForm = true">
            + {{ $t("admin.addNew") }}
          </button>
        </div>
      </div>

      <!-- Filter Bar -->
      <div class="filter-bar">
        <input
          v-model="searchQuery"
          type="text"
          :placeholder="$t('common.search')"
          class="search-input"
          aria-label="Search rooms"
        />
        <select v-model="filterStatus" class="filter-select" aria-label="Filter by status">
          <option value="">{{ $t("common.allStatuses") }}</option>
          <option value="available">{{ $t("room.status.available") }}</option>
          <option value="occupied">{{ $t("room.status.occupied") }}</option>
          <option value="maintenance">{{ $t("room.status.maintenance") }}</option>
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

    <!-- Rooms Table -->
    <div v-else class="table-wrapper">
      <table class="data-table" aria-label="Rooms list">
        <thead>
          <tr>
            <th>{{ $t("admin.id") }}</th>
            <th>{{ $t("room.number") }}</th>
            <th>{{ $t("room.type") }}</th>
            <th>{{ $t("room.status") }}</th>
            <th>{{ $t("room.pricePerNight") }}</th>
            <th>{{ $t("room.capacity") }}</th>
            <th>{{ $t("room.rating") }}</th>
            <th>{{ $t("room.active") }}</th>
            <th>{{ $t("admin.actions") }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredRooms.length === 0">
            <td colspan="9" class="empty-row">{{ $t("admin.noRooms") }}</td>
          </tr>
          <tr v-for="room in filteredRooms" :key="room.id">
            <td>#{{ room.id }}</td>
            <td>
              <strong>{{ room.room_number }}</strong>
            </td>
            <td>
              <span :class="`type-badge type-${room.room_type?.toLowerCase()}`">
                {{ room.room_type?.toUpperCase() }}
              </span>
            </td>
            <td>
              <select
                :value="room.status"
                :disabled="updatingId === room.id"
                class="status-select"
                aria-label="Change room status"
                @change="(e) => updateRoomStatus(room.id, (e.target as HTMLSelectElement).value)"
              >
                <option value="available">AVAILABLE</option>
                <option value="occupied">OCCUPIED</option>
                <option value="maintenance">MAINTENANCE</option>
              </select>
            </td>
            <td>EGP {{ room.price_per_night?.toFixed(2) }}</td>
            <td>{{ room.capacity }} {{ $t("room.persons") }}</td>
            <td>⭐ {{ room.rating?.toFixed(1) ?? "—" }}</td>
            <td>
              <button
                v-if="room.is_active"
                @click="toggleRoomActive(room.id, false)"
                :disabled="updatingId === room.id"
                class="action-btn active"
              >
                Deactivate
              </button>
              <button
                v-else
                @click="toggleRoomActive(room.id, true)"
                :disabled="updatingId === room.id"
                class="action-btn inactive"
              >
                Activate
              </button>
            </td>
            <td>
              <div class="action-group">
                <button
                  @click="editRoom(room)"
                  :disabled="updatingId === room.id"
                  class="action-btn-icon"
                  title="Edit room"
                >
                  ✎
                </button>
                <button
                  @click="deleteRoom(room.id)"
                  :disabled="updatingId === room.id"
                  class="action-btn-icon danger"
                  title="Delete room"
                >
                  ✕
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddForm || editingRoom" class="modal-overlay" @click.self="closeForm">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ editingRoom ? $t("admin.editRoom") : $t("admin.addNewRoom") }}</h2>
          <button @click="closeForm" class="close-btn">✕</button>
        </div>
        <form @submit.prevent="saveRoom" class="form">
          <div class="form-group">
            <label for="room_number">{{ $t("room.number") }}</label>
            <input
              id="room_number"
              v-model="formData.room_number"
              type="text"
              required
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="room_type">{{ $t("room.type") }}</label>
            <select id="room_type" v-model="formData.room_type" required class="form-input">
              <option value="">Select Type</option>
              <option value="standard">Standard</option>
              <option value="deluxe">Deluxe</option>
              <option value="suite">Suite</option>
              <option value="beach">Beach</option>
            </select>
          </div>
          <div class="form-group">
            <label for="capacity">{{ $t("room.capacity") }}</label>
            <input
              id="capacity"
              v-model.number="formData.capacity"
              type="number"
              min="1"
              required
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="price">{{ $t("room.pricePerNight") }}</label>
            <input
              id="price"
              v-model.number="formData.price_per_night"
              type="number"
              min="0"
              step="0.01"
              required
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="description_en">{{ $t("room.description") }} (EN)</label>
            <textarea
              id="description_en"
              v-model="formData.description_en"
              class="form-input"
              rows="3"
            ></textarea>
          </div>
          <div class="form-group">
            <label>
              <input v-model="formData.is_active" type="checkbox" />
              {{ $t("common.active") }}
            </label>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="saving">
              {{ saving ? $t("common.saving") : $t("common.save") }}
            </button>
            <button type="button" @click="closeForm" class="btn btn-secondary">
              {{ $t("common.cancel") }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { roomApi, type Room, type RoomCreate } from "../../api/rooms";

const rooms = ref<Room[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const success = ref<string | null>(null);
const updatingId = ref<number | null>(null);
const saving = ref(false);
const showAddForm = ref(false);
const editingRoom = ref<Room | null>(null);
const searchQuery = ref("");
const filterStatus = ref("");

const formData = ref<RoomCreate>({
  room_number: "",
  room_type: "",
  price_per_night: 0,
  capacity: 1,
  description_en: "",
  is_active: true,
});

const filteredRooms = computed(() => {
  return rooms.value.filter((room) => {
    const matchesSearch =
      room.room_number.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      room.room_type.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesStatus = !filterStatus.value || room.status === filterStatus.value;
    return matchesSearch && matchesStatus;
  });
});

async function fetchRooms() {
  loading.value = true;
  error.value = null;
  try {
    const response = await roomApi.getAll();
    rooms.value = response.data;
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { error?: string } } };
    error.value = axiosErr.response?.data?.error ?? "Failed to load rooms";
  } finally {
    loading.value = false;
  }
}

async function updateRoomStatus(roomId: number, status: string) {
  updatingId.value = roomId;
  error.value = null;
  try {
    await roomApi.adminUpdateStatus(roomId, status);
    const idx = rooms.value.findIndex((r) => r.id === roomId);
    if (idx !== -1 && rooms.value[idx]) {
      rooms.value[idx]!.status = status;
    }
    success.value = "Status updated successfully";
    setTimeout(() => (success.value = null), 3000);
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { error?: string } } };
    error.value = axiosErr.response?.data?.error ?? "Failed to update status";
  } finally {
    updatingId.value = null;
  }
}

async function toggleRoomActive(roomId: number, isActive: boolean) {
  updatingId.value = roomId;
  error.value = null;
  try {
    await roomApi.adminToggleActive(roomId, isActive);
    const idx = rooms.value.findIndex((r) => r.id === roomId);
    if (idx !== -1 && rooms.value[idx]) {
      rooms.value[idx]!.is_active = isActive;
    }
    success.value = `Room ${isActive ? "activated" : "deactivated"}`;
    setTimeout(() => (success.value = null), 3000);
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { error?: string } } };
    error.value = axiosErr.response?.data?.error ?? "Failed to update room";
  } finally {
    updatingId.value = null;
  }
}

function editRoom(room: Room) {
  editingRoom.value = room;
  formData.value = {
    room_number: room.room_number,
    room_type: room.room_type,
    price_per_night: room.price_per_night,
    capacity: room.capacity,
    description_en: room.description_en,
    is_active: room.is_active,
  };
  showAddForm.value = false;
}

async function saveRoom() {
  saving.value = true;
  error.value = null;
  try {
    if (editingRoom.value) {
      await roomApi.adminUpdate(editingRoom.value.id, formData.value);
      const idx = rooms.value.findIndex((r) => r.id === editingRoom.value!.id);
      if (idx !== -1 && rooms.value[idx]) {
        rooms.value[idx] = { ...rooms.value[idx], ...formData.value };
      }
      success.value = "Room updated successfully";
    } else {
      const response = await roomApi.adminCreate(formData.value);
      rooms.value.push(response.data);
      success.value = "Room created successfully";
    }
    closeForm();
    setTimeout(() => (success.value = null), 3000);
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { error?: string } } };
    error.value = axiosErr.response?.data?.error ?? "Failed to save room";
  } finally {
    saving.value = false;
  }
}

async function deleteRoom(roomId: number) {
  if (!confirm("Are you sure you want to delete this room?")) return;
  updatingId.value = roomId;
  error.value = null;
  try {
    await roomApi.adminDelete(roomId);
    rooms.value = rooms.value.filter((r) => r.id !== roomId);
    success.value = "Room deleted successfully";
    setTimeout(() => (success.value = null), 3000);
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { error?: string } } };
    error.value = axiosErr.response?.data?.error ?? "Failed to delete room";
  } finally {
    updatingId.value = null;
  }
}

function closeForm() {
  showAddForm.value = false;
  editingRoom.value = null;
  formData.value = {
    room_number: "",
    room_type: "",
    price_per_night: 0,
    capacity: 1,
    description_en: "",
    is_active: true,
  };
}

onMounted(fetchRooms);
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
.type-badge,
.status-badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}
.type-badge {
  background: #ede9fe;
  color: #5b21b6;
}
.status-badge.status-available {
  background: #d1fae5;
  color: #065f46;
}
.status-badge.status-occupied {
  background: #dbeafe;
  color: #1e40af;
}
.status-badge.status-maintenance {
  background: #fee2e2;
  color: #991b1b;
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
}
.header-meta {
  display: flex;
  gap: 1rem;
  align-items: center;
}
.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-primary {
  background: var(--color-primary, #4f46e5);
  color: white;
}
.btn-primary:hover {
  background: #4338ca;
}
.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}
.btn-secondary:hover {
  background: #e5e7eb;
}
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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

.status-select {
  padding: 0.4rem 0.6rem;
  border: 1px solid #d1d5db;
  border-radius: 0.3rem;
  font-size: 0.85rem;
  cursor: pointer;
}
.status-select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}
.modal {
  background: white;
  border-radius: 0.5rem;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}
.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
}
.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
}
.close-btn:hover {
  color: #374151;
}

.form {
  padding: 1.5rem;
}
.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
  font-size: 0.9rem;
}
.form-group input[type="checkbox"] {
  margin-right: 0.5rem;
}
.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  font-family: inherit;
}
.form-input:focus {
  outline: none;
  border-color: var(--color-primary, #4f46e5);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}
</style>
