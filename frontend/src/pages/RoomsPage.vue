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

      <!-- Filters Section -->
      <div class="mb-8 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Sort by
          </label>
          <select
            v-model="sortBy"
            class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-ocean-deep-500"
          >
            <option value="price">Price: Low to High</option>
            <option value="-price">Price: High to Low</option>
            <option value="rating">Rating: High to Low</option>
            <option value="capacity">Capacity: High to Low</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Min Price
          </label>
          <input
            v-model.number="minPrice"
            type="number"
            placeholder="$0"
            class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-ocean-deep-500"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Max Price
          </label>
          <input
            v-model.number="maxPrice"
            type="number"
            placeholder="$1000"
            class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-ocean-deep-500"
          />
        </div>
      </div>

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
const sortBy = ref("price");
const minPrice = ref(0);
const maxPrice = ref(1000);

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
    return room.price_per_night >= minPrice.value && room.price_per_night <= maxPrice.value;
  });

  // Sort
  if (sortBy.value === "price") {
    result.sort((a, b) => a.price_per_night - b.price_per_night);
  } else if (sortBy.value === "-price") {
    result.sort((a, b) => b.price_per_night - a.price_per_night);
  } else if (sortBy.value === "rating") {
    result.sort((a, b) => ((b as any).rating || 0) - ((a as any).rating || 0));
  } else if (sortBy.value === "capacity") {
    result.sort((a, b) => b.capacity - a.capacity);
  }

  return result;
});

onMounted(() => {
  fetchRooms();
});
</script>
