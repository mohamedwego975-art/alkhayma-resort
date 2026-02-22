<template>
  <div class="card mb-6">
    <div class="flex flex-col md:flex-row gap-4">
      <!-- Search Input -->
      <div class="flex-1">
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            :placeholder="$t('search.placeholder')"
            class="w-full pl-10 pr-4 py-3 rounded-lg border border-ocean-deep-200 focus:border-ocean-deep-500 focus:ring-2 focus:ring-ocean-deep-200 transition-all"
            @input="handleSearch"
          />
          <span class="absolute left-3 top-1/2 -translate-y-1/2 text-ocean-deep-400">🔍</span>
        </div>
      </div>

      <!-- Filters Button -->
      <button
        @click="showFilters = !showFilters"
        class="btn-secondary flex items-center gap-2 whitespace-nowrap"
      >
        <span>🎛️</span>
        {{ $t("search.filters") }}
        <span
          v-if="activeFiltersCount > 0"
          class="bg-ocean-deep-600 text-white rounded-full w-5 h-5 text-xs flex items-center justify-center"
        >
          {{ activeFiltersCount }}
        </span>
      </button>

      <!-- Sort -->
      <select
        v-model="sortBy"
        class="px-4 py-3 rounded-lg border border-ocean-deep-200 focus:border-ocean-deep-500 focus:ring-2 focus:ring-ocean-deep-200 transition-all"
        @change="handleSort"
      >
        <option value="price_asc">{{ $t("search.price_low") }}</option>
        <option value="price_desc">{{ $t("search.price_high") }}</option>
        <option value="rating_desc">{{ $t("search.rating_high") }}</option>
        <option value="name_asc">{{ $t("search.name_az") }}</option>
      </select>
    </div>

    <!-- Advanced Filters Panel -->
    <Transition name="slide-down">
      <div v-if="showFilters" class="mt-6 pt-6 border-t border-ocean-deep-200">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Price Range -->
          <div>
            <label class="block text-sm font-medium text-ocean-deep-900 mb-2">
              {{ $t("search.priceRange") }}
            </label>
            <div class="flex items-center gap-3">
              <input
                v-model.number="filters.minPrice"
                type="number"
                :placeholder="$t('search.min')"
                class="w-full px-3 py-2 rounded-lg border border-ocean-deep-200 focus:border-ocean-deep-500"
                @input="handleFilterChange"
              />
              <span class="text-ocean-deep-600">-</span>
              <input
                v-model.number="filters.maxPrice"
                type="number"
                :placeholder="$t('search.max')"
                class="w-full px-3 py-2 rounded-lg border border-ocean-deep-200 focus:border-ocean-deep-500"
                @input="handleFilterChange"
              />
            </div>
          </div>

          <!-- Room Type -->
          <div>
            <label class="block text-sm font-medium text-ocean-deep-900 mb-2">
              {{ $t("search.roomType") }}
            </label>
            <select
              v-model="filters.roomType"
              class="w-full px-3 py-2 rounded-lg border border-ocean-deep-200 focus:border-ocean-deep-500"
              @change="handleFilterChange"
            >
              <option value="">{{ $t("search.all") }}</option>
              <option value="standard">{{ $t("rooms.standard") }}</option>
              <option value="deluxe">{{ $t("rooms.deluxe") }}</option>
              <option value="suite">{{ $t("rooms.suite") }}</option>
              <option value="villa">{{ $t("rooms.villa") }}</option>
            </select>
          </div>

          <!-- Capacity -->
          <div>
            <label class="block text-sm font-medium text-ocean-deep-900 mb-2">
              {{ $t("search.guests") }}
            </label>
            <select
              v-model.number="filters.capacity"
              class="w-full px-3 py-2 rounded-lg border border-ocean-deep-200 focus:border-ocean-deep-500"
              @change="handleFilterChange"
            >
              <option :value="0">{{ $t("search.any") }}</option>
              <option :value="1">1 {{ $t("search.guest") }}</option>
              <option :value="2">2 {{ $t("search.guests") }}</option>
              <option :value="3">3 {{ $t("search.guests") }}</option>
              <option :value="4">4+ {{ $t("search.guests") }}</option>
            </select>
          </div>

          <!-- Amenities -->
          <div class="md:col-span-3">
            <label class="block text-sm font-medium text-ocean-deep-900 mb-2">
              {{ $t("search.amenities") }}
            </label>
            <div class="flex flex-wrap gap-3">
              <label
                v-for="amenity in amenitiesList"
                :key="amenity.value"
                class="flex items-center gap-2 px-4 py-2 rounded-lg border border-ocean-deep-200 cursor-pointer hover:border-ocean-deep-500 transition-colors"
                :class="{
                  'bg-ocean-deep-50 border-ocean-deep-500': filters.amenities.includes(
                    amenity.value,
                  ),
                }"
              >
                <input
                  v-model="filters.amenities"
                  type="checkbox"
                  :value="amenity.value"
                  class="rounded text-ocean-deep-600 focus:ring-ocean-deep-500"
                  @change="handleFilterChange"
                />
                <span class="text-sm">{{ amenity.icon }} {{ amenity.label }}</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Clear Filters -->
        <div class="mt-4 flex justify-end">
          <button
            @click="clearFilters"
            class="text-sm text-ocean-deep-600 hover:text-ocean-deep-900 font-medium"
          >
            {{ $t("search.clearFilters") }}
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const emit = defineEmits(["search", "filter", "sort"]);

const searchQuery = ref("");
const sortBy = ref("price_asc");
const showFilters = ref(false);

const filters = ref({
  minPrice: null as number | null,
  maxPrice: null as number | null,
  roomType: "",
  capacity: 0,
  amenities: [] as string[],
});

const amenitiesList = computed(() => [
  { value: "wifi", label: t("amenities.wifi"), icon: "📶" },
  { value: "ac", label: t("amenities.ac"), icon: "❄️" },
  { value: "tv", label: t("amenities.tv"), icon: "📺" },
  { value: "minibar", label: t("amenities.minibar"), icon: "🍷" },
  { value: "balcony", label: t("amenities.balcony"), icon: "🌅" },
  { value: "jacuzzi", label: t("amenities.jacuzzi"), icon: "🛁" },
  { value: "kitchen", label: t("amenities.kitchen"), icon: "🍳" },
  { value: "seaView", label: t("amenities.seaView"), icon: "🌊" },
]);

const activeFiltersCount = computed(() => {
  let count = 0;
  if (filters.value.minPrice) count++;
  if (filters.value.maxPrice) count++;
  if (filters.value.roomType) count++;
  if (filters.value.capacity > 0) count++;
  count += filters.value.amenities.length;
  return count;
});

const handleSearch = () => {
  emit("search", searchQuery.value);
};

const handleFilterChange = () => {
  emit("filter", filters.value);
};

const handleSort = () => {
  emit("sort", sortBy.value);
};

const clearFilters = () => {
  filters.value = {
    minPrice: null,
    maxPrice: null,
    roomType: "",
    capacity: 0,
    amenities: [],
  };
  handleFilterChange();
};
</script>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  max-height: 0;
  overflow: hidden;
}

.slide-down-enter-to,
.slide-down-leave-from {
  opacity: 1;
  max-height: 500px;
}
</style>
