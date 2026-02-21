import { defineStore } from "pinia";
import { ref } from "vue";

export type NotificationType = "success" | "error" | "warning" | "info";

export interface Notification {
  id: string;
  message: string;
  type: NotificationType;
  duration?: number;
  action?: {
    label: string;
    callback: () => void;
  };
}

export const useNotificationStore = defineStore("notification", () => {
  const notifications = ref<Notification[]>([]);
  let nextId = 0;

  function addNotification(notification: Omit<Notification, "id">) {
    const id = `notification-${nextId++}`;
    const notif: Notification = {
      ...notification,
      id,
      duration: notification.duration ?? 4000,
    };

    notifications.value.push(notif);

    if (notif.duration && notif.duration > 0) {
      setTimeout(() => {
        removeNotification(id);
      }, notif.duration);
    }

    return id;
  }

  function removeNotification(id: string) {
    const index = notifications.value.findIndex((n) => n.id === id);
    if (index !== -1) {
      notifications.value.splice(index, 1);
    }
  }

  function clearNotifications(type?: NotificationType) {
    if (type) {
      notifications.value = notifications.value.filter((n) => n.type !== type);
    } else {
      notifications.value = [];
    }
  }

  function success(message: string, duration?: number) {
    return addNotification({ message, type: "success", duration });
  }

  function error(message: string, duration?: number) {
    return addNotification({ message, type: "error", duration: duration ?? 6000 });
  }

  function warning(message: string, duration?: number) {
    return addNotification({ message, type: "warning", duration });
  }

  function info(message: string, duration?: number) {
    return addNotification({ message, type: "info", duration });
  }

  return {
    notifications,
    addNotification,
    removeNotification,
    clearNotifications,
    success,
    error,
    warning,
    info,
  };
});
