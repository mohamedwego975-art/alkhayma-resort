<template>
  <div id="app" class="min-h-screen flex flex-col bg-white dark:bg-gray-950 transition-colors">
    <Navbar />
    <NotificationCenter />
    <main class="flex-1">
      <RouterView />
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
import { onMounted } from "vue";
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";
import NotificationCenter from "@/components/NotificationCenter.vue";
import { useThemeStore } from "@/stores/theme";

const themeStore = useThemeStore();

onMounted(() => {
  themeStore.initializeTheme();
  themeStore.watchSystemPreference();
});
</script>
