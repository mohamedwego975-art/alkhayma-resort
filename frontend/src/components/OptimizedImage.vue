<template>
  <img 
    :src="src" 
    :alt="alt"
    :width="width"
    :height="height"
    :loading="loading"
    :class="className"
    @load="onLoad"
    @error="onError"
  />
</template>

<script setup lang="ts">
interface Props {
  src: string
  alt: string
  width?: number
  height?: number
  loading?: 'lazy' | 'eager'
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  loading: 'lazy'
})

const emit = defineEmits<{
  load: []
  error: []
}>()

const onLoad = () => emit('load')
const onError = () => emit('error')
</script>
