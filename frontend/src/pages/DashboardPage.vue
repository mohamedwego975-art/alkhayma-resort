<template>
  <div class="min-h-screen bg-gradient-to-br from-ocean-deep-50 to-teal-glow-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-ocean-deep-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-ocean-deep-900">{{ $t("dashboard.title") }}</h1>
            <p class="text-sm text-ocean-deep-600">
              {{ $t("dashboard.welcome") }}, {{ user?.full_name }}
            </p>
          </div>
          <button @click="logout" class="btn-secondary">
            {{ $t("auth.logout") }}
          </button>
        </div>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div v-for="stat in stats" :key="stat.label" class="card">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-ocean-deep-600">{{ stat.label }}</p>
              <p class="text-3xl font-bold text-ocean-deep-900 mt-1">{{ stat.value }}</p>
              <p class="text-xs text-teal-glow-600 mt-1">{{ stat.change }}</p>
            </div>
            <div :class="`w-12 h-12 rounded-full flex items-center justify-center ${stat.bgColor}`">
              <span class="text-2xl">{{ stat.icon }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="bg-white rounded-lg shadow-sm border border-ocean-deep-100 mb-6">
        <div class="border-b border-ocean-deep-100">
          <nav class="flex space-x-8 px-6" aria-label="Tabs">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
                activeTab === tab.id
                  ? 'border-ocean-deep-600 text-ocean-deep-900'
                  : 'border-transparent text-ocean-deep-600 hover:text-ocean-deep-900 hover:border-ocean-deep-300',
              ]"
            >
              {{ tab.label }}
            </button>
          </nav>
        </div>

        <!-- Tab Content -->
        <div class="p-6">
          <!-- Bookings Tab -->
          <div v-if="activeTab === 'bookings'">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg font-semibold text-ocean-deep-900">
                {{ $t("dashboard.recentBookings") }}
              </h3>
              <button class="btn-primary text-sm">{{ $t("dashboard.viewAll") }}</button>
            </div>
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-ocean-deep-200">
                <thead>
                  <tr>
                    <th
                      class="px-4 py-3 text-left text-xs font-medium text-ocean-deep-600 uppercase"
                    >
                      ID
                    </th>
                    <th
                      class="px-4 py-3 text-left text-xs font-medium text-ocean-deep-600 uppercase"
                    >
                      {{ $t("dashboard.guest") }}
                    </th>
                    <th
                      class="px-4 py-3 text-left text-xs font-medium text-ocean-deep-600 uppercase"
                    >
                      {{ $t("dashboard.room") }}
                    </th>
                    <th
                      class="px-4 py-3 text-left text-xs font-medium text-ocean-deep-600 uppercase"
                    >
                      {{ $t("dashboard.dates") }}
                    </th>
                    <th
                      class="px-4 py-3 text-left text-xs font-medium text-ocean-deep-600 uppercase"
                    >
                      {{ $t("dashboard.status") }}
                    </th>
                    <th
                      class="px-4 py-3 text-left text-xs font-medium text-ocean-deep-600 uppercase"
                    >
                      {{ $t("dashboard.total") }}
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-ocean-deep-100">
                  <tr v-if="loading" v-for="i in 5" :key="i">
                    <td colspan="6" class="px-4 py-4">
                      <div class="h-4 bg-ocean-deep-100 rounded animate-pulse"></div>
                    </td>
                  </tr>
                  <tr v-else-if="bookings.length === 0">
                    <td colspan="6" class="px-4 py-8 text-center text-ocean-deep-600">
                      {{ $t("dashboard.noBookings") }}
                    </td>
                  </tr>
                  <tr
                    v-else
                    v-for="booking in bookings"
                    :key="booking.id"
                    class="hover:bg-ocean-deep-50"
                  >
                    <td class="px-4 py-4 text-sm text-ocean-deep-900">#{{ booking.id }}</td>
                    <td class="px-4 py-4 text-sm text-ocean-deep-900">{{ booking.guest_name }}</td>
                    <td class="px-4 py-4 text-sm text-ocean-deep-900">{{ booking.room_number }}</td>
                    <td class="px-4 py-4 text-sm text-ocean-deep-600">
                      {{ formatDate(booking.check_in) }} - {{ formatDate(booking.check_out) }}
                    </td>
                    <td class="px-4 py-4">
                      <span :class="getStatusClass(booking.status)">
                        {{ $t(`dashboard.status_${booking.status}`) }}
                      </span>
                    </td>
                    <td class="px-4 py-4 text-sm font-medium text-ocean-deep-900">
                      ${{ booking.total_amount }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Rooms Tab -->
          <div v-if="activeTab === 'rooms'">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg font-semibold text-ocean-deep-900">
                {{ $t("dashboard.roomManagement") }}
              </h3>
              <button class="btn-primary text-sm">{{ $t("dashboard.addRoom") }}</button>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div
                v-for="room in rooms"
                :key="room.id"
                class="card hover:shadow-lg transition-shadow"
              >
                <div class="flex justify-between items-start mb-3">
                  <div>
                    <h4 class="font-semibold text-ocean-deep-900">
                      {{ $t("rooms.room") }} {{ room.room_number }}
                    </h4>
                    <p class="text-sm text-ocean-deep-600">{{ $t(`rooms.${room.room_type}`) }}</p>
                  </div>
                  <span
                    :class="
                      room.status === 'available'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    "
                    class="px-2 py-1 rounded-full text-xs font-medium"
                  >
                    {{ $t(`dashboard.${room.status}`) }}
                  </span>
                </div>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-ocean-deep-600">{{ $t("dashboard.price") }}:</span>
                    <span class="font-medium text-ocean-deep-900"
                      >${{ room.price_per_night }}/{{ $t("dashboard.night") }}</span
                    >
                  </div>
                  <div class="flex justify-between">
                    <span class="text-ocean-deep-600">{{ $t("dashboard.capacity") }}:</span>
                    <span class="font-medium text-ocean-deep-900"
                      >{{ room.capacity }} {{ $t("dashboard.guests") }}</span
                    >
                  </div>
                  <div class="flex justify-between">
                    <span class="text-ocean-deep-600">{{ $t("dashboard.rating") }}:</span>
                    <span class="font-medium text-ocean-deep-900"
                      >{{ room.rating || "N/A" }} ⭐</span
                    >
                  </div>
                </div>
                <div class="mt-4 flex gap-2">
                  <button class="flex-1 btn-secondary text-sm">{{ $t("dashboard.edit") }}</button>
                  <button class="flex-1 btn-primary text-sm">{{ $t("dashboard.view") }}</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Users Tab -->
          <div v-if="activeTab === 'users'">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg font-semibold text-ocean-deep-900">
                {{ $t("dashboard.userManagement") }}
              </h3>
              <button class="btn-primary text-sm">{{ $t("dashboard.addUser") }}</button>
            </div>
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-ocean-deep-200">
                <thead>
                  <tr>
                    <th
                      class="px-4 py-3 text-left text-xs font-medium text-ocean-deep-600 uppercase"
                    >
                      {{ $t("dashboard.name") }}
                    </th>
                    <th
                      class="px-4 py-3 text-left text-xs font-medium text-ocean-deep-600 uppercase"
                    >
                      {{ $t("dashboard.email") }}
                    </th>
                    <th
                      class="px-4 py-3 text-left text-xs font-medium text-ocean-deep-600 uppercase"
                    >
                      {{ $t("dashboard.role") }}
                    </th>
                    <th
                      class="px-4 py-3 text-left text-xs font-medium text-ocean-deep-600 uppercase"
                    >
                      {{ $t("dashboard.status") }}
                    </th>
                    <th
                      class="px-4 py-3 text-left text-xs font-medium text-ocean-deep-600 uppercase"
                    >
                      {{ $t("dashboard.joined") }}
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-ocean-deep-100">
                  <tr v-for="user in users" :key="user.id" class="hover:bg-ocean-deep-50">
                    <td class="px-4 py-4 text-sm text-ocean-deep-900">{{ user.full_name }}</td>
                    <td class="px-4 py-4 text-sm text-ocean-deep-600">{{ user.email }}</td>
                    <td class="px-4 py-4">
                      <span
                        :class="getRoleClass(user.role)"
                        class="px-2 py-1 rounded-full text-xs font-medium"
                      >
                        {{ $t(`dashboard.role_${user.role}`) }}
                      </span>
                    </td>
                    <td class="px-4 py-4">
                      <span
                        :class="user.is_active ? 'text-green-600' : 'text-red-600'"
                        class="text-sm"
                      >
                        {{ user.is_active ? $t("dashboard.active") : $t("dashboard.inactive") }}
                      </span>
                    </td>
                    <td class="px-4 py-4 text-sm text-ocean-deep-600">
                      {{ formatDate(user.created_at) }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Analytics Tab -->
          <div v-if="activeTab === 'analytics'">
            <h3 class="text-lg font-semibold text-ocean-deep-900 mb-4">
              {{ $t("dashboard.analytics") }}
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="card">
                <h4 class="font-semibold text-ocean-deep-900 mb-4">
                  {{ $t("dashboard.revenueChart") }}
                </h4>
                <div class="h-64 flex items-center justify-center bg-ocean-deep-50 rounded-lg">
                  <p class="text-ocean-deep-600">{{ $t("dashboard.chartPlaceholder") }}</p>
                </div>
              </div>
              <div class="card">
                <h4 class="font-semibold text-ocean-deep-900 mb-4">
                  {{ $t("dashboard.occupancyChart") }}
                </h4>
                <div class="h-64 flex items-center justify-center bg-ocean-deep-50 rounded-lg">
                  <p class="text-ocean-deep-600">{{ $t("dashboard.chartPlaceholder") }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useI18n } from "vue-i18n";
import api from "@/api/client";

const { t } = useI18n();
const router = useRouter();
const authStore = useAuthStore();

interface Booking {
  id: number;
  guest_name: string;
  room_number: string;
  check_in: string;
  check_out: string;
  status: string;
  total_amount: number;
}

interface Room {
  id: number;
  room_number: string;
  room_type: string;
  status: string;
  price_per_night: number;
  capacity: number;
  rating?: number;
}

interface User {
  id: number;
  full_name: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

const user = computed(() => authStore.user);
const activeTab = ref("bookings");
const loading = ref(true);
const bookings = ref<Booking[]>([]);
const rooms = ref<Room[]>([]);
const users = ref<User[]>([]);

const tabs = [
  { id: "bookings", label: t("dashboard.bookings") },
  { id: "rooms", label: t("dashboard.rooms") },
  { id: "users", label: t("dashboard.users") },
  { id: "analytics", label: t("dashboard.analytics") },
];

const stats = ref([
  {
    label: t("dashboard.totalBookings"),
    value: "0",
    change: "+0%",
    icon: "📅",
    bgColor: "bg-blue-100",
  },
  {
    label: t("dashboard.totalRevenue"),
    value: "$0",
    change: "+0%",
    icon: "💰",
    bgColor: "bg-green-100",
  },
  {
    label: t("dashboard.occupancyRate"),
    value: "0%",
    change: "+0%",
    icon: "🏨",
    bgColor: "bg-purple-100",
  },
  {
    label: t("dashboard.totalGuests"),
    value: "0",
    change: "+0%",
    icon: "👥",
    bgColor: "bg-orange-100",
  },
]);

const logout = () => {
  authStore.logout();
  router.push("/login");
};

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
};

const getStatusClass = (status: string) => {
  const classes = {
    confirmed: "px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800",
    pending: "px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800",
    cancelled: "px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800",
    completed: "px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800",
  };
  return classes[status as keyof typeof classes] || classes.pending;
};

const getRoleClass = (role: string) => {
  const classes = {
    admin: "bg-purple-100 text-purple-800",
    staff: "bg-blue-100 text-blue-800",
    guest: "bg-gray-100 text-gray-800",
  };
  return classes[role as keyof typeof classes] || classes.guest;
};

const fetchData = async () => {
  loading.value = true;
  try {
    // Fetch rooms
    const roomsResponse = await api.get("/rooms");
    rooms.value = (roomsResponse.data || []).map((room: any) => ({
      id: room.id,
      room_number: room.room_number || room.name,
      room_type: room.room_type || "standard",
      status: room.status || (room.is_active ? "available" : "occupied"),
      price_per_night: room.price_per_night || room.base_price,
      capacity: room.capacity,
      rating: room.rating,
    }));

    // Update stats
    const occupiedRooms = rooms.value.filter((r: Room) => r.status === "occupied").length;
    if (stats.value[2]) {
      stats.value[2].value = `${rooms.value.length > 0 ? Math.round((occupiedRooms / rooms.value.length) * 100) : 0}%`;
    }
  } catch (error) {
    console.error("Failed to fetch dashboard data:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  if (user.value?.role !== "admin") {
    router.push("/");
    return;
  }
  fetchData();
});
</script>
