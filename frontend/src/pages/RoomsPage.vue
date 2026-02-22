<template>
  <div class="min-h-screen bg-white dark:bg-gray-950 transition-colors">
    <!-- Header -->
    <div
      class="bg-gradient-to-r from-ocean-deep-600 to-teal-glow-600 dark:from-ocean-deep-800 dark:to-teal-glow-800 text-white py-16"
    >
      <div class="container-responsive text-center">
        <span class="badge glass-dark text-white mb-4">Accommodation</span>
        <h1 class="heading-display text-4xl md:text-5xl lg:text-6xl mb-4">Our Luxury Rooms</h1>
        <p class="text-lg md:text-xl text-white/90 max-w-2xl mx-auto">
          Discover comfort and elegance in every corner
        </p>
      </div>
    </div>

    <div class="container-responsive section-padding">
      <!-- Breadcrumb -->
      <Breadcrumb :breadcrumbs="[{ label: 'Rooms', to: '/rooms' }]" class="mb-8" />

      <!-- Advanced Search -->
      <AdvancedSearch
        @search="handleSearch"
        @filter="handleFilter"
        @sort="handleSort"
        class="mb-8"
      />

      <!-- Loading State -->
      <SkeletonLoader v-if="loading" :count="6" :cols="3" height="400px" wrapper="div" />

      <!-- Rooms Grid -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
        <RoomCard v-for="room in filteredRooms" :key="room.id" :room="room" />
      </div>

      <!-- Empty State -->
      <EmptyState
        v-if="!loading && filteredRooms.length === 0"
        icon="🏨"
        title="No Rooms Found"
        message="Try adjusting your filters or check back later"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { roomApi, type Room } from "@/api";
import RoomCard from "@/components/RoomCard.vue";
import SkeletonLoader from "@/components/SkeletonLoader.vue";
import EmptyState from "@/components/EmptyState.vue";
import Breadcrumb from "@/components/Breadcrumb.vue";
import { useMeta } from "@/composables/useSEO";

const rooms = ref<Room[]>([]);
const loading = ref(true);
const sortBy = ref("price_asc");
const searchQuery = ref("");
const filters = ref({
  minPrice: null as number | null,
  maxPrice: null as number | null,
  roomType: "",
  capacity: 0,
  amenities: [] as string[],
});

// Debounce timers
let searchDebounceTimer: ReturnType<typeof setTimeout> | null = null;
let filterDebounceTimer: ReturnType<typeof setTimeout> | null = null;

const handleSearch = (query: string) => {
  // Clear existing timer
  if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
  // Set new timer for debounce
  searchDebounceTimer = setTimeout(() => {
    searchQuery.value = query;
  }, 300);
};

const handleFilter = (newFilters: typeof filters.value) => {
  // Clear existing timer
  if (filterDebounceTimer) clearTimeout(filterDebounceTimer);
  // Set new timer for debounce
  filterDebounceTimer = setTimeout(() => {
    filters.value = { ...newFilters };
  }, 300);
};

const handleSort = (sortOption: string) => {
  sortBy.value = sortOption;
};

useMeta({
  title: "Luxury Rooms - الخيمة Beach Resort",
  description: "Browse our collection of luxury rooms at الخيمة Beach Resort on the Red Sea",
  keywords: "luxury rooms, resort accommodation, red sea",
});

async function fetchRooms() {
  loading.value = true;
  try {
    const response = await roomApi.getAll();
    rooms.value = response.data;
  } catch (error) {
    console.error("Failed to fetch rooms:", error);
  } finally {
    loading.value = false;
  }
}

const filteredRooms = computed(() => {
  let result = rooms.value.filter((room) => {
    // Search query filter
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase();
      const matchesRoomNumber = room.room_number?.toLowerCase().includes(query);
      const matchesDescription =
        room.description_en?.toLowerCase().includes(query) ||
        room.description_ar?.toLowerCase().includes(query);
      if (!matchesRoomNumber && !matchesDescription) return false;
    }

    // Price filter
    const minP = filters.value.minPrice ?? 0;
    const maxP = filters.value.maxPrice ?? Number.MAX_SAFE_INTEGER;
    if (room.price_per_night < minP || room.price_per_night > maxP) return false;

    // Room type filter
    if (filters.value.roomType && room.room_type !== filters.value.roomType) return false;

    // Capacity filter
    if (filters.value.capacity > 0 && room.capacity < filters.value.capacity) return false;

    // Amenities filter - handle multiple formats (seaView, sea view, seaview)
    if (filters.value.amenities.length > 0) {
      const roomAmenities =
        room.amenities
          ?.toLowerCase()
          .split(",")
          .map((a) => a.trim()) || [];

      const hasAllAmenities = filters.value.amenities.every((filterAmenity) => {
        const normalizedFilter = filterAmenity.toLowerCase();
        // Handle both camelCase and space/underscore variants
        return roomAmenities.some((roomAmenity) => {
          const normalizedRoom = roomAmenity.replace(/[ _]/g, "");
          const normalizedFilterNoCase = normalizedFilter.replace(/[ _]/g, "");
          return (
            normalizedRoom === normalizedFilterNoCase ||
            roomAmenity.includes(normalizedFilter) ||
            normalizedFilter.includes(roomAmenity)
          );
        });
      });
      if (!hasAllAmenities) return false;
    }

    return true;
  });

  // Sort
  if (sortBy.value === "price_asc") {
    result.sort((a, b) => a.price_per_night - b.price_per_night);
  } else if (sortBy.value === "price_desc") {
    result.sort((a, b) => b.price_per_night - a.price_per_night);
  } else if (sortBy.value === "rating_desc") {
    result.sort((a, b) => ((b as any).rating || 0) - ((a as any).rating || 0));
  } else if (sortBy.value === "name_asc") {
    result.sort((a, b) => (a.room_number || "").localeCompare(b.room_number || ""));
  }

  return result;
});

onMounted(() => {
  fetchRooms();
});
</script>
