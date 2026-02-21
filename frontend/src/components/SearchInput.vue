<template>
  <div class="relative">
    <div class="relative">
      <input
        v-model="searchQuery"
        type="text"
        :placeholder="placeholder"
        class="w-full px-4 py-3 pr-10 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-ocean-deep-500 transition-all"
      />
      <svg
        class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
        />
      </svg>
    </div>

    <!-- Results Dropdown -->
    <transition name="dropdown">
      <div
        v-show="searchQuery && isOpen"
        class="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg shadow-lg z-40 max-h-96 overflow-y-auto"
      >
        <div v-if="loading" class="p-4 text-center text-gray-500 dark:text-gray-400">
          Loading...
        </div>
        <template v-else-if="results.length > 0">
          <button
            v-for="result in results"
            :key="result"
            @click="selectResult(result)"
            class="w-full text-left px-4 py-3 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors border-b border-gray-200 dark:border-gray-700 last:border-b-0"
          >
            <p class="text-gray-900 dark:text-white font-medium">{{ result }}</p>
          </button>
        </template>
        <div v-else class="p-4 text-center text-gray-500 dark:text-gray-400">No results found</div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { onClickOutside } from "@vueuse/core";

interface Props {
  placeholder?: string;
  items: string[];
  loading?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: "Search...",
  loading: false,
});

const emit = defineEmits<{ select: [value: string] }>();

const searchQuery = ref("");
const isOpen = ref(false);
const container = ref<HTMLElement>();

const results = ref<string[]>([]);

watch(searchQuery, (value) => {
  if (value) {
    isOpen.value = true;
    results.value = props.items.filter((item) => item.toLowerCase().includes(value.toLowerCase()));
  } else {
    isOpen.value = false;
    results.value = [];
  }
});

const selectResult = (result: string) => {
  emit("select", result);
  searchQuery.value = "";
  isOpen.value = false;
};

onClickOutside(container, () => {
  isOpen.value = false;
});
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
