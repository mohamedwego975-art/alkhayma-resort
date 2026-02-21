<template>
  <teleport to="body">
    <transition name="modal">
      <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="closeModal" />

        <!-- Modal -->
        <div
          class="relative bg-white dark:bg-gray-900 rounded-xl shadow-2xl max-w-md w-full"
          @click.stop
        >
          <!-- Header -->
          <div
            v-if="title || $slots.header"
            class="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700"
          >
            <div v-if="title" class="heading-display text-xl text-gray-900 dark:text-white">
              {{ title }}
            </div>
            <slot name="header" />
            <button
              @click="closeModal"
              class="p-1 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
            >
              ✕
            </button>
          </div>

          <!-- Body -->
          <div class="p-6">
            <slot />
          </div>

          <!-- Footer -->
          <div
            v-if="$slots.footer"
            class="flex gap-3 p-6 border-t border-gray-200 dark:border-gray-700"
          >
            <slot name="footer" />
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup lang="ts">
import { useVModel } from "@vueuse/core";

interface Props {
  modelValue: boolean;
  title?: string;
}

const props = defineProps<Props>();
const emit = defineEmits<{ "update:modelValue": [value: boolean] }>();

const isOpen = useVModel(props, "modelValue", emit);

const closeModal = () => {
  isOpen.value = false;
};
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-to,
.modal-leave-from {
  opacity: 1;
}
</style>
