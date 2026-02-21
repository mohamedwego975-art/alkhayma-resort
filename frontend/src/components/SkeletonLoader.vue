<template>
  <component :is="wrapper" :class="wrapperClass">
    <div
      v-for="n in count"
      :key="n"
      :style="{ height: height, width: width }"
      class="animate-pulse rounded-lg bg-gray-200 dark:bg-gray-700"
    />
  </component>
</template>

<script setup lang="ts">
interface Props {
  count?: number;
  height?: string;
  width?: string;
  wrapper?: string;
  cols?: number;
}

const props = withDefaults(defineProps<Props>(), {
  count: 3,
  height: "100px",
  width: "100%",
  wrapper: "div",
  cols: 1,
});

import { computed } from "vue";

const wrapperClass = computed(() => {
  if (props.cols === 1) return "space-y-3";
  if (props.cols === 2) return "grid grid-cols-2 gap-4";
  if (props.cols === 3) return "grid grid-cols-3 gap-4";
  return "grid grid-cols-1 gap-4";
});
</script>
