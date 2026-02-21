import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import i18n from "./i18n";
import { useFavoritesStore } from "@/stores/favorites";
import "./style.css";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);

// Initialize stores
const favoritesStore = useFavoritesStore();
favoritesStore.initialize();

app.use(router);
app.use(i18n);

app.mount("#app");

// Handle service worker updates
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    window.location.reload();
  });
}
