<template>
  <figure class="relative overflow-hidden rounded-lg bg-gray-200 dark:bg-gray-800">
    <!-- Placeholder/Blur -->
    <div
      v-if="!loaded"
      class="absolute inset-0 bg-gradient-to-br from-gray-200 to-gray-300 dark:from-gray-700 dark:to-gray-800 animate-pulse"
    />

    <!-- Image -->
    <img
      :src="src"
      :alt="alt"
      :width="width"
      :height="height"
      :loading="loading"
      :class="[
        className,
        'transition-opacity duration-500',
        { 'opacity-0': !loaded, 'opacity-100': loaded }
      ]"
      @load="onLoad"
      @error="onError"
    />

    <!-- Caption -->
    <figcaption v-if="caption" class="sr-only">{{ caption }}</figcaption>
  </figure>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  src: string
  alt: string
  caption?: string
  width?: number
  height?: number
  loading?: 'lazy' | 'eager'
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  loading: 'lazy',
  className: 'w-full h-auto object-cover'
})

const emit = defineEmits<{
  load: []
  error: []
}>()

const loaded = ref(false)

const onLoad = () => {
  loaded.value = true
  emit('load')
}

const onError = () => {
  loaded.value = true
  emit('error')
}
</script>

<style scoped>
figure {
  aspect-ratio: auto;
}
</style>
}>()

const onLoad = () => emit('load')
const onError = () => emit('error')
</script>
