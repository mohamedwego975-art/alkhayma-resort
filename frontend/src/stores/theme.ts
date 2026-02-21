import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useThemeStore = defineStore("theme", () => {
  const isDark = ref<boolean>(false);

  // Initialize from localStorage
  function initializeTheme() {
    const saved = localStorage.getItem("alkhayma-theme");
    if (saved) {
      isDark.value = JSON.parse(saved);
    } else {
      // Check system preference
      isDark.value = window.matchMedia("(prefers-color-scheme: dark)").matches;
    }
    applyTheme();
  }

  // Apply theme to document
  function applyTheme() {
    const root = document.documentElement;
    if (isDark.value) {
      root.classList.add("dark");
      root.style.colorScheme = "dark";
    } else {
      root.classList.remove("dark");
      root.style.colorScheme = "light";
    }
    localStorage.setItem("alkhayma-theme", JSON.stringify(isDark.value));
  }

  // Toggle theme
  function toggleTheme() {
    isDark.value = !isDark.value;
    applyTheme();
  }

  // Set specific theme
  function setTheme(dark: boolean) {
    isDark.value = dark;
    applyTheme();
  }

  // Watch for system theme changes
  function watchSystemPreference() {
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    const handleChange = (e: MediaQueryListEvent) => {
      const saved = localStorage.getItem("alkhayma-theme");
      // Only update if user hasn't manually set preference
      if (!saved) {
        isDark.value = e.matches;
        applyTheme();
      }
    };

    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener("change", handleChange);
    }
  }

  const themeClass = computed(() => (isDark.value ? "dark" : "light"));
  const themeIcon = computed(() => (isDark.value ? "🌙" : "☀️"));

  return {
    isDark,
    toggleTheme,
    setTheme,
    initializeTheme,
    watchSystemPreference,
    themeClass,
    themeIcon,
  };
});
