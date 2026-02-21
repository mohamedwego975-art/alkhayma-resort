<template>
  <div
    class="fixed top-4 right-4 z-[9999] pointer-events-none space-y-3 max-w-sm w-full px-4 md:px-0"
  >
    <transition-group name="notification" tag="div" class="space-y-3">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        :class="[
          'notification-item p-4 rounded-lg shadow-lg backdrop-blur-md pointer-events-auto',
          'animate-slide-in-right',
          notificationClasses[notification.type],
        ]"
        role="alert"
      >
        <div class="flex items-start gap-3">
          <span class="text-xl flex-shrink-0 mt-0.5">
            {{ notificationIcon[notification.type] }}
          </span>
          <div class="flex-1">
            <p class="text-sm font-medium leading-tight">
              {{ notification.message }}
            </p>
          </div>
          <button
            @click="removeNotification(notification.id)"
            class="flex-shrink-0 text-lg opacity-60 hover:opacity-100 transition-opacity"
            aria-label="Close notification"
          >
            ✕
          </button>
        </div>

        <!-- Progress bar -->
        <div
          v-if="notification.duration && notification.duration > 0"
          class="mt-2 h-1 rounded-full opacity-40"
          :class="notificationProgressClasses[notification.type]"
          :style="{
            animation: `progress ${notification.duration}ms linear forwards`,
          }"
        />
      </div>
    </transition-group>
  </div>
</template>

<script setup lang="ts">
import { useNotificationStore } from "@/stores/notifications";
import { computed } from "vue";

const notificationStore = useNotificationStore();

const notifications = computed(() => notificationStore.notifications);

const notificationClasses = {
  success:
    "bg-green-50 dark:bg-green-950/50 text-green-900 dark:text-green-200 border border-green-200 dark:border-green-800",
  error:
    "bg-red-50 dark:bg-red-950/50 text-red-900 dark:text-red-200 border border-red-200 dark:border-red-800",
  warning:
    "bg-amber-50 dark:bg-amber-950/50 text-amber-900 dark:text-amber-200 border border-amber-200 dark:border-amber-800",
  info: "bg-blue-50 dark:bg-blue-950/50 text-blue-900 dark:text-blue-200 border border-blue-200 dark:border-blue-800",
};

const notificationProgressClasses = {
  success: "bg-green-500",
  error: "bg-red-500",
  warning: "bg-amber-500",
  info: "bg-blue-500",
};

const notificationIcon = {
  success: "✓",
  error: "✕",
  warning: "⚠",
  info: "ℹ",
};

const removeNotification = (id: string) => {
  notificationStore.removeNotification(id);
};
</script>

<style scoped>
@keyframes slide-in-right {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes progress {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}

.animate-slide-in-right {
  animation: slide-in-right 0.3s ease-out;
}

.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
