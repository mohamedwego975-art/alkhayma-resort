<template>
  <nav class="glass sticky top-0 z-50 border-b border-white/20 dark:border-white/10">
    <div class="container-responsive">
      <div class="flex justify-between items-center h-20">
        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-3 group">
          <div
            class="w-12 h-12 rounded-xl bg-gradient-to-br from-ocean-deep-500 to-teal-glow-500 flex items-center justify-center text-2xl transform group-hover:scale-110 transition-transform"
          >
            🏖️
          </div>
          <div>
            <span class="heading-display text-2xl gradient-text block">الخيمة</span>
            <span class="text-xs text-gray-600 dark:text-gray-400">Beach Resort</span>
          </div>
        </router-link>

        <!-- Desktop Menu -->
        <div class="hidden md:flex items-center gap-8">
          <router-link
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            class="text-gray-700 dark:text-gray-300 hover:text-ocean-deep-600 dark:hover:text-ocean-deep-400 font-medium transition-all relative group"
            active-class="text-ocean-deep-600 dark:text-ocean-deep-400"
          >
            {{ link.label }}
            <span
              class="absolute bottom-0 left-0 w-0 h-0.5 bg-ocean-deep-600 dark:bg-ocean-deep-400 group-hover:w-full transition-all duration-300"
            ></span>
          </router-link>

          <!-- Auth Section -->
          <div
            v-if="authStore.isAuthenticated"
            class="flex items-center gap-4 ml-4 pl-4 border-l border-gray-200 dark:border-gray-700"
          >
            <router-link
              v-if="authStore.user?.role === 'admin'"
              to="/dashboard"
              class="text-gray-700 dark:text-gray-300 hover:text-ocean-deep-600 dark:hover:text-ocean-deep-400 font-medium"
            >
              <span class="flex items-center gap-2"> <span>📊</span> Dashboard </span>
            </router-link>
            <router-link
              to="/account"
              class="text-gray-700 dark:text-gray-300 hover:text-ocean-deep-600 dark:hover:text-ocean-deep-400 font-medium"
            >
              <span class="flex items-center gap-2"> <span>👤</span> Account </span>
            </router-link>
            <button
              @click="handleLogout"
              class="text-gray-700 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 font-medium"
            >
              Logout
            </button>
          </div>
          <div
            v-else
            class="flex items-center gap-3 ml-4 pl-4 border-l border-gray-200 dark:border-gray-700"
          >
            <router-link
              to="/login"
              class="text-gray-700 dark:text-gray-300 hover:text-ocean-deep-600 dark:hover:text-ocean-deep-400 font-medium"
            >
              Login
            </router-link>
            <router-link to="/register" class="btn-primary text-sm px-4 py-2">
              Register
            </router-link>
          </div>

          <!-- Theme Switcher -->
          <ThemeSwitcher />
        </div>

        <!-- Mobile Menu Button -->
        <div class="md:hidden flex items-center gap-3">
          <ThemeSwitcher />
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <svg
              class="w-6 h-6 text-gray-700 dark:text-gray-300"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                v-if="!mobileMenuOpen"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Menu -->
      <div
        v-if="mobileMenuOpen"
        class="md:hidden py-4 border-t border-gray-200 dark:border-gray-700 animate-slide-down"
      >
        <router-link
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          @click="mobileMenuOpen = false"
          class="block py-3 text-gray-700 dark:text-gray-300 hover:text-ocean-deep-600 dark:hover:text-ocean-deep-400 font-medium hover:bg-gray-50 dark:hover:bg-gray-800/50 px-4 rounded-lg transition-colors"
        >
          {{ link.label }}
        </router-link>

        <div
          v-if="authStore.isAuthenticated"
          class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700"
        >
          <router-link
            to="/account"
            @click="mobileMenuOpen = false"
            class="block py-3 text-gray-700 dark:text-gray-300 hover:text-ocean-deep-600 dark:hover:text-ocean-deep-400 font-medium hover:bg-gray-50 dark:hover:bg-gray-800/50 px-4 rounded-lg"
          >
            👤 Account
          </router-link>
          <button
            @click="handleLogout"
            class="block w-full text-left py-3 text-gray-700 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 font-medium hover:bg-gray-50 dark:hover:bg-gray-800/50 px-4 rounded-lg"
          >
            Logout
          </button>
        </div>
        <div v-else class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 space-y-2 px-4">
          <router-link
            to="/login"
            @click="mobileMenuOpen = false"
            class="block py-3 text-center text-gray-700 dark:text-gray-300 hover:text-ocean-deep-600 dark:hover:text-ocean-deep-400 font-medium border border-gray-300 dark:border-gray-600 rounded-lg hover:border-ocean-deep-600 dark:hover:border-ocean-deep-400 transition-colors"
          >
            Login
          </router-link>
          <router-link
            to="/register"
            @click="mobileMenuOpen = false"
            class="block btn-primary text-center"
          >
            Register
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import ThemeSwitcher from "./ThemeSwitcher.vue";

const router = useRouter();
const authStore = useAuthStore();
const mobileMenuOpen = ref(false);

const navLinks = [
  { path: "/", label: "Home" },
  { path: "/rooms", label: "Rooms" },
  { path: "/beach", label: "Beach" },
];

function handleLogout() {
  authStore.logout();
  mobileMenuOpen.value = false;
  router.push("/");
}
</script>

<style scoped>
@keyframes slide-down {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-down {
  animation: slide-down 0.3s ease-out;
}
</style>
