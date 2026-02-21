<template>
  <button
    @click="themeStore.toggleTheme()"
    class="relative inline-flex items-center justify-center w-10 h-10 rounded-lg transition-all duration-300"
    :class="[
      'hover:bg-gray-200 dark:hover:bg-gray-700',
      'focus:outline-none focus:ring-2 focus:ring-offset-2',
      'dark:focus:ring-offset-gray-950 focus:ring-ocean-deep-500',
    ]"
    :title="`Switch to ${themeStore.isDark ? 'light' : 'dark'} mode`"
    :aria-label="`Switch to ${themeStore.isDark ? 'light' : 'dark'} mode`"
  >
    <!-- Sun Icon -->
    <transition name="theme-fade" mode="out-in">
      <div v-if="!themeStore.isDark" key="sun" class="absolute text-xl">☀️</div>
      <!-- Moon Icon -->
      <div v-else key="moon" class="absolute text-xl">🌙</div>
    </transition>
  </button>
</template>

<script setup lang="ts">
import { useThemeStore } from "@/stores/theme";

const themeStore = useThemeStore();
</script>

<style scoped>
.theme-fade-enter-active,
.theme-fade-leave-active {
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}

.theme-fade-enter-from {
  opacity: 0;
  transform: rotate(-180deg) scale(0);
}

.theme-fade-leave-to {
  opacity: 0;
  transform: rotate(180deg) scale(0);
}

.theme-fade-enter-to,
.theme-fade-leave-from {
  opacity: 1;
  transform: rotate(0) scale(1);
}
</style>
