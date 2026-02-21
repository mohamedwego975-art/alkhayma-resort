import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useFavoritesStore = defineStore("favorites", () => {
  const favorites = ref<number[]>([]);

  // Initialize from localStorage
  function initialize() {
    const saved = localStorage.getItem("alkhayma-favorites");
    if (saved) {
      favorites.value = JSON.parse(saved);
    }
  }

  // Toggle favorite
  function toggleFavorite(id: number) {
    const index = favorites.value.indexOf(id);
    if (index > -1) {
      favorites.value.splice(index, 1);
    } else {
      favorites.value.push(id);
    }
    saveFavorites();
  }

  // Add favorite
  function addFavorite(id: number) {
    if (!favorites.value.includes(id)) {
      favorites.value.push(id);
      saveFavorites();
    }
  }

  // Remove favorite
  function removeFavorite(id: number) {
    const index = favorites.value.indexOf(id);
    if (index > -1) {
      favorites.value.splice(index, 1);
      saveFavorites();
    }
  }

  // Check if is favorite
  function isFavorite(id: number) {
    return favorites.value.includes(id);
  }

  // Save to localStorage
  function saveFavorites() {
    localStorage.setItem("alkhayma-favorites", JSON.stringify(favorites.value));
  }

  // Clear all favorites
  function clearFavorites() {
    favorites.value = [];
    saveFavorites();
  }

  const count = computed(() => favorites.value.length);

  return {
    favorites,
    initialize,
    toggleFavorite,
    addFavorite,
    removeFavorite,
    isFavorite,
    clearFavorites,
    count,
  };
});
