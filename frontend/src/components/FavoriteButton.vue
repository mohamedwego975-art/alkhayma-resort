<template>
  <button
    @click="toggleFavorite"
    :title="isFavorited ? 'Remove from favorites' : 'Add to favorites'"
    class="inline-flex items-center justify-center p-2 rounded-lg transition-all"
    :class="[
      'focus:outline-none focus:ring-2 focus:ring-offset-2 dark:focus:ring-offset-gray-900 focus:ring-ocean-deep-500',
      isFavorited
        ? 'bg-red-50 dark:bg-red-950/30 text-red-500 dark:text-red-400 hover:bg-red-100 dark:hover:bg-red-950/50'
        : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700',
    ]"
  >
    <svg
      class="w-6 h-6 transition-transform"
      :class="{ 'scale-125': isFavorited }"
      :fill="isFavorited ? 'currentColor' : 'none'"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
      />
    </svg>
  </button>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useFavoritesStore } from "@/stores/favorites";

interface Props {
  itemId: number;
}

const props = defineProps<Props>();
const favoritesStore = useFavoritesStore();

const isFavorited = computed(() => favoritesStore.isFavorite(props.itemId));

const toggleFavorite = () => {
  favoritesStore.toggleFavorite(props.itemId);
};
</script>

<style scoped>
button {
  aspect-ratio: 1;
}
</style>
