<template>
  <nav
    class="flex items-center gap-2 text-sm px-4 py-3 bg-gray-50 dark:bg-gray-900 rounded-lg overflow-x-auto"
  >
    <router-link
      to="/"
      class="text-ocean-deep-600 dark:text-ocean-deep-400 hover:text-ocean-deep-700 dark:hover:text-ocean-deep-300 transition-colors flex items-center gap-2"
    >
      <span>🏠</span>
      <span>Home</span>
    </router-link>

    <span v-for="(crumb, index) in breadcrumbs" :key="index" class="flex items-center gap-2">
      <span class="text-gray-400">›</span>
      <component
        :is="crumb.to ? 'router-link' : 'span'"
        :to="crumb.to"
        :class="{
          'text-ocean-deep-600 dark:text-ocean-deep-400 hover:text-ocean-deep-700 dark:hover:text-ocean-deep-300 transition-colors':
            crumb.to,
          'text-gray-700 dark:text-gray-300': !crumb.to,
        }"
      >
        {{ crumb.label }}
      </component>
    </span>
  </nav>
</template>

<script setup lang="ts">
interface Breadcrumb {
  label: string;
  to?: string;
}

withDefaults(defineProps<{ breadcrumbs: Breadcrumb[] }>(), {});
</script>

<style scoped>
nav {
  -webkit-mask-image: linear-gradient(
    90deg,
    transparent,
    black 20px,
    black calc(100% - 20px),
    transparent
  );
  mask-image: linear-gradient(90deg, transparent, black 20px, black calc(100% - 20px), transparent);
}
</style>
