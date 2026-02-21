<template>
  <router-link
    :to="`/rooms/${room.id}`"
    class="group flex flex-col h-full card overflow-hidden hover:shadow-2xl"
  >
    <!-- Image Section -->
    <div
      class="relative h-64 bg-gradient-to-br from-ocean-deep-400 to-ocean-deep-600 overflow-hidden"
    >
      <div class="absolute inset-0 bg-black/20 group-hover:bg-black/0 transition-colors" />
      <div class="absolute inset-0 flex items-center justify-center">
        <span class="text-white text-8xl transform group-hover:scale-110 transition-transform"
          >🏨</span
        >
      </div>

      <!-- Badges -->
      <div class="absolute top-4 left-4 right-4 flex justify-between items-start">
        <span v-if="room.room_type" class="badge badge-primary">
          {{ room.room_type }}
        </span>
        <FavoriteButton :item-id="room.id" />
      </div>

      <!-- Live Counter -->
      <LiveCounter
        v-if="room.id"
        :product-id="room.id"
        class="absolute bottom-4 left-4 glass-dark px-3 py-1 rounded-full text-white text-sm"
      />
    </div>

    <!-- Content Section -->
    <div class="flex flex-col flex-1 p-6">
      <!-- Title & Room Number -->
      <div class="mb-3">
        <div class="flex items-start justify-between gap-2 mb-2">
          <h3
            class="text-xl md:text-2xl font-bold text-gray-800 dark:text-white group-hover:text-ocean-deep-600 dark:group-hover:text-ocean-deep-400 transition-colors"
          >
            Room {{ room.room_number }}
          </h3>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-400">
          Capacity: {{ room.capacity }} {{ room.capacity === 1 ? "guest" : "guests" }}
        </p>
      </div>

      <!-- Rating -->
      <div class="mb-4 flex items-center gap-3">
        <div class="flex gap-0.5">
          <span v-for="n in 5" :key="n" class="text-lg">
            {{ n <= (room.rating || 4) ? "⭐" : "☆" }}
          </span>
        </div>
        <span class="text-sm text-gray-600 dark:text-gray-400"> {{ room.rating || 4 }}/5 </span>
      </div>

      <!-- Amenities -->
      <div class="mb-4 space-y-2">
        <div class="flex flex-wrap gap-2">
          <span class="badge bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 text-xs">
            📶 WiFi
          </span>
          <span class="badge bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 text-xs">
            ❄️ AC
          </span>
          <span class="badge bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 text-xs">
            📺 TV
          </span>
          <span class="badge bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 text-xs">
            🥃 Bar
          </span>
        </div>
      </div>

      <!-- Price & CTA -->
      <div
        class="mt-auto flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700"
      >
        <div>
          <span class="text-sm text-gray-600 dark:text-gray-400">from</span>
          <span class="ml-1 text-2xl md:text-3xl font-bold gradient-text"
            >${{ room.price_per_night }}</span
          >
          <span class="text-sm text-gray-600 dark:text-gray-400">/night</span>
        </div>
        <span class="btn-primary text-sm px-6 py-2 line-clamp-1"> View Details → </span>
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import FavoriteButton from "./FavoriteButton.vue";
import LiveCounter from "./smart/LiveCounter.vue";

interface Room {
  id: number;
  room_number: string;
  room_type: string;
  capacity: number;
  price_per_night: number;
  rating?: number;
  [key: string]: any;
}

defineProps<{ room: Room }>();
</script>
