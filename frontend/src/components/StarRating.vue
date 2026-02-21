<template>
  <div class="flex items-center gap-2">
    <div class="flex gap-0.5">
      <button
        v-for="star in 5"
        :key="star"
        @click="rating = star"
        @mouseenter="hoveredStar = star"
        @mouseleave="hoveredStar = 0"
        class="text-2xl transition-all hover:scale-110"
        :title="`${star} ${star === 1 ? 'star' : 'stars'}`"
      >
        {{ (hoveredStar || rating) >= star ? "⭐" : "☆" }}
      </button>
    </div>
    <span v-if="showLabel" class="text-sm text-gray-600 dark:text-gray-400"> {{ rating }}/5 </span>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

interface Props {
  modelValue?: number;
  readonly?: boolean;
  showLabel?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: 0,
  readonly: false,
  showLabel: true,
});

const emit = defineEmits<{ "update:modelValue": [value: number] }>();

const rating = ref(props.modelValue);
const hoveredStar = ref(0);
</script>
