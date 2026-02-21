<template>
  <div class="flex items-center justify-center min-h-80 text-center">
    <div>
      <div class="text-8xl mb-4 opacity-40">{{ icon }}</div>
      <h3 class="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-2">{{ title }}</h3>
      <p v-if="message" class="text-gray-600 dark:text-gray-400 mb-6">{{ message }}</p>
      <button v-if="retryFn" @click="retryFn" class="btn-primary text-sm">
        {{ retryLabel }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  icon?: string;
  title: string;
  message?: string;
  retryLabel?: string;
  retryFn?: () => void;
}

withDefaults(defineProps<Props>(), {
  icon: "❌",
  retryLabel: "Try Again",
});
</script>
