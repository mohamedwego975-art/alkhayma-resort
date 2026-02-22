<template>
  <div
    class="min-h-screen bg-gradient-to-b from-white to-gray-50 dark:from-gray-950 dark:to-gray-900 transition-colors"
  >
    <!-- Header -->
    <div
      class="bg-gradient-to-r from-ocean-deep-600 to-teal-glow-600 dark:from-ocean-deep-800 dark:to-teal-glow-800 text-white py-16"
    >
      <div class="container-responsive text-center">
        <span class="badge glass-dark text-white mb-4">🏨 Accommodation</span>
        <h1 class="heading-display text-4xl md:text-5xl lg:text-6xl mb-4">Luxury Rooms</h1>
        <p class="text-lg md:text-xl text-white/90 max-w-2xl mx-auto">
          Discover comfort and elegance in every corner
        </p>
      </div>
    </div>

    <div class="container-responsive section-padding">
      <!-- Breadcrumb -->
      <div class="mb-8 flex items-center gap-2 text-sm">
        <router-link to="/" class="text-ocean-deep-600 hover:text-ocean-deep-700">Home</router-link>
        <span class="text-gray-400">/</span>
        <span class="text-gray-700 dark:text-gray-300">Rooms</span>
      </div>

      <!-- Filters and Search -->
      <div
        class="bg-white dark:bg-gray-900 rounded-2xl p-6 mb-8 shadow-md border border-gray-200 dark:border-gray-800"
      >
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <!-- Search -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
              >Search</label
            >
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search rooms..."
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-ocean-deep-500"
            />
          </div>

          <!-- Room Type Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
              >Type</label
            >
            <select
              v-model="selectedRoomType"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-ocean-deep-500"
            >
              <option value="">All Types</option>
              <option value="standard">Standard</option>
              <option value="deluxe">Deluxe</option>
              <option value="suite">Suite</option>
            </select>
          </div>

          <!-- Capacity Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
              >Capacity</label
            >
            <select
              v-model.number="selectedCapacity"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-ocean-deep-500"
            >
              <option value="0">Any Capacity</option>
              <option value="1">1 Guest</option>
              <option value="2">2+ Guests</option>
              <option value="3">3+ Guests</option>
              <option value="4">4+ Guests</option>
            </select>
          </div>

          <!-- Sort -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
              >Sort</label
            >
            <select
              v-model="sortBy"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-ocean-deep-500"
            >
              <option value="name_asc">Room Number (A-Z)</option>
              <option value="price_asc">Price: Low to High</option>
              <option value="price_desc">Price: High to Low</option>
              <option value="rating_desc">Highest Rated</option>
            </select>
          </div>
        </div>

        <!-- Results Info -->
        <div class="mt-4 flex justify-between items-center">
          <span class="text-sm text-gray-600 dark:text-gray-400">
            Showing {{ filteredRooms.length }} of {{ rooms.length }} rooms
          </span>
          <button
            @click="resetFilters"
            class="text-sm text-ocean-deep-600 hover:text-ocean-deep-700 dark:text-teal-400 dark:hover:text-teal-300 font-medium"
          >
            Reset Filters
          </button>
        </div>
      </div>

      <!-- Error State -->
      <div
        v-if="error"
        class="mb-8 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-400"
      >
        <p class="font-medium">{{ error }}</p>
        <button @click="fetchRooms" class="mt-2 text-sm underline hover:no-underline">Retry</button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        <div
          v-for="i in 6"
          :key="i"
          class="bg-white dark:bg-gray-900 rounded-2xl overflow-hidden shadow-lg animate-pulse"
        >
          <div class="h-48 bg-gray-300 dark:bg-gray-800"></div>
          <div class="p-4 space-y-3">
            <div class="h-6 bg-gray-300 dark:bg-gray-800 rounded"></div>
            <div class="h-4 bg-gray-300 dark:bg-gray-800 rounded"></div>
            <div class="h-4 bg-gray-300 dark:bg-gray-800 rounded w-2/3"></div>
          </div>
        </div>
      </div>

      <!-- Rooms Grid -->
      <div
        v-else-if="filteredRooms.length > 0"
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8"
      >
        <router-link
          v-for="room in filteredRooms"
          :key="room.id"
          :to="`/rooms/${room.id}`"
          class="group bg-white dark:bg-gray-900 rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1"
        >
          <!-- Image -->
          <div
            class="relative h-48 bg-gradient-to-br from-ocean-deep-200 to-teal-glow-200 dark:from-ocean-deep-800 dark:to-teal-glow-800 flex items-center justify-center overflow-hidden"
          >
            <span class="text-6xl">🏨</span>
            <div
              class="absolute top-3 right-3 bg-white dark:bg-gray-900 px-3 py-1 rounded-full text-xs font-bold"
              :class="
                room.status === 'available'
                  ? 'text-green-600 dark:text-green-400'
                  : 'text-red-600 dark:text-red-400'
              "
            >
              {{ room.status === "available" ? "✓ Available" : "✗ Booked" }}
            </div>
          </div>

          <!-- Content -->
          <div class="p-6">
            <!-- Room Type Badge -->
            <div class="mb-3 inline-block">
              <span class="badge badge-primary text-xs">{{ room.room_type.toUpperCase() }}</span>
            </div>

            <!-- Title -->
            <h3 class="text-xl font-bold text-gray-800 dark:text-white mb-2">
              Room #{{ room.room_number }}
            </h3>

            <!-- Description -->
            <p class="text-sm text-gray-600 dark:text-gray-400 line-clamp-2 mb-4">
              {{ room.description_en || "Comfortable and modern room" }}
            </p>

            <!-- Amenities -->
            <div v-if="room.amenities" class="mb-4 flex flex-wrap gap-2">
              <span
                v-if="room.amenities.wifi"
                class="text-xs bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 px-2 py-1 rounded"
              >
                📶 WiFi
              </span>
              <span
                v-if="room.amenities.ac"
                class="text-xs bg-cyan-100 dark:bg-cyan-900/50 text-cyan-700 dark:text-cyan-300 px-2 py-1 rounded"
              >
                ❄️ AC
              </span>
              <span
                v-if="room.amenities.tv"
                class="text-xs bg-purple-100 dark:bg-purple-900/50 text-purple-700 dark:text-purple-300 px-2 py-1 rounded"
              >
                📺 TV
              </span>
              <span
                v-if="room.amenities.balcony"
                class="text-xs bg-orange-100 dark:bg-orange-900/50 text-orange-700 dark:text-orange-300 px-2 py-1 rounded"
              >
                🌅 Balcony
              </span>
            </div>

            <!-- Rating -->
            <div v-if="room.review_count > 0" class="mb-4 flex items-center gap-2">
              <div class="flex text-yellow-400">
                <span v-for="i in 5" :key="i" class="text-lg">
                  {{ i <= Math.round(room.rating || 0) ? "★" : "☆" }}
                </span>
              </div>
              <span class="text-sm text-gray-600 dark:text-gray-400"
                >{{ room.rating || 0 }} ({{ room.review_count }})</span
              >
            </div>

            <!-- Capacity & Price -->
            <div
              class="flex justify-between items-center pt-4 border-t border-gray-200 dark:border-gray-800"
            >
              <span class="text-sm text-gray-600 dark:text-gray-400"
                >👥 Up to {{ room.capacity }} guests</span
              >
              <div class="text-right">
                <span class="block text-lg font-bold text-ocean-deep-600 dark:text-teal-400"
                  >${{ room.price_per_night }}</span
                >
                <span class="text-xs text-gray-500 dark:text-gray-400">per night</span>
              </div>
            </div>
          </div>
        </router-link>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-16">
        <div class="text-6xl mb-4">🔍</div>
        <h3 class="text-2xl font-bold text-gray-800 dark:text-white mb-2">No Rooms Found</h3>
        <p class="text-gray-600 dark:text-gray-400 mb-4">
          Try adjusting your filters or search terms
        </p>
        <button
          @click="resetFilters"
          class="inline-block px-6 py-2 bg-ocean-deep-600 hover:bg-ocean-deep-700 text-white rounded-lg font-medium transition-colors"
        >
          Clear Filters
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { roomApi } from "@/api";

const router = useRouter();

const rooms = ref<any[]>([]);
const loading = ref(true);
const error = ref("");
const searchQuery = ref("");
const selectedRoomType = ref("");
const selectedCapacity = ref(0);
const sortBy = ref("name_asc");

const filteredRooms = computed(() => {
  let result = rooms.value.filter((room) => {
    // Search
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase();
      const matchesNumber = room.room_number?.toLowerCase().includes(query);
      const matchesDesc = room.description_en?.toLowerCase().includes(query);
      if (!matchesNumber && !matchesDesc) return false;
    }

    // Type
    if (selectedRoomType.value && room.room_type !== selectedRoomType.value) return false;

    // Capacity
    if (selectedCapacity.value > 0 && room.capacity < selectedCapacity.value) return false;

    return true;
  });

  // Sort
  switch (sortBy.value) {
    case "price_asc":
      result.sort((a, b) => a.price_per_night - b.price_per_night);
      break;
    case "price_desc":
      result.sort((a, b) => b.price_per_night - a.price_per_night);
      break;
    case "rating_desc":
      result.sort((a, b) => (b.rating || 0) - (a.rating || 0));
      break;
    case "name_asc":
      result.sort((a, b) => (a.room_number || "").localeCompare(b.room_number || ""));
      break;
  }

  return result;
});

async function fetchRooms() {
  loading.value = true;
  error.value = "";
  try {
    const response = await roomApi.getAll();
    rooms.value = response.data || [];
  } catch (err) {
    console.error("Failed to fetch rooms:", err);
    error.value = "Failed to load rooms. Please try again.";
  } finally {
    loading.value = false;
  }
}

function resetFilters() {
  searchQuery.value = "";
  selectedRoomType.value = "";
  selectedCapacity.value = 0;
  sortBy.value = "name_asc";
}

onMounted(() => {
  fetchRooms();
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
