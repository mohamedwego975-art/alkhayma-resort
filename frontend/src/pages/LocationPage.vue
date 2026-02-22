<template>
  <div class="location-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">{{ t("location.title") }}</h1>
        <p class="hero-subtitle">{{ t("location.subtitle") }}</p>
      </div>
    </section>

    <!-- Map Section -->
    <section class="map-section">
      <div class="container">
        <ResortMap :center="resortLocation" :zoom="16" :height="'500px'" :markers="markers" />
      </div>
    </section>

    <!-- Location Details -->
    <section class="details-section">
      <div class="container">
        <div class="details-grid">
          <!-- Address -->
          <div class="detail-card">
            <div class="detail-icon">📍</div>
            <h3 class="detail-title">{{ t("location.address") }}</h3>
            <p class="detail-content">
              {{ t("location.address_line1") }}<br />
              {{ t("location.address_line2") }}<br />
              {{ t("location.address_city") }}
            </p>
          </div>

          <!-- Contact -->
          <div class="detail-card">
            <div class="detail-icon">📞</div>
            <h3 class="detail-title">{{ t("location.contact") }}</h3>
            <p class="detail-content">
              {{ t("location.phone") }}<br />
              {{ t("location.email") }}
            </p>
          </div>

          <!-- Transportation -->
          <div class="detail-card">
            <div class="detail-icon">🚗</div>
            <h3 class="detail-title">{{ t("location.transportation") }}</h3>
            <p class="detail-content">
              {{ t("location.airport_distance") }}<br />
              {{ t("location.taxi_available") }}
            </p>
          </div>

          <!-- Nearby Attractions -->
          <div class="detail-card">
            <div class="detail-icon">🎯</div>
            <h3 class="detail-title">{{ t("location.nearby") }}</h3>
            <p class="detail-content">
              {{ t("location.attraction1") }}<br />
              {{ t("location.attraction2") }}<br />
              {{ t("location.attraction3") }}
            </p>
          </div>
        </div>

        <!-- CTA -->
        <div class="cta-section">
          <a :href="directionsLink" target="_blank" class="cta-button">
            {{ t("location.get_directions") }}
          </a>
        </div>
      </div>
    </section>

    <!-- Nearby Places -->
    <section class="nearby-section">
      <div class="container">
        <h2 class="section-title">{{ t("location.nearby_places") }}</h2>
        <div class="nearby-grid">
          <div v-for="place in nearbyPlaces" :key="place.name" class="nearby-card">
            <div class="nearby-icon">{{ place.icon }}</div>
            <h4 class="nearby-name">{{ place.name }}</h4>
            <p class="nearby-distance">{{ place.distance }}</p>
            <p class="nearby-description">{{ place.description }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import ResortMap from "@/components/ResortMap.vue";

const { t } = useI18n();

// Resort location - Alexandria, Egypt (example coordinates)
const resortLocation = {
  lat: 31.2001,
  lng: 29.9187,
};

const directionsLink = computed(() => {
  return `https://www.google.com/maps/dir/?api=1&destination=${resortLocation.lat},${resortLocation.lng}`;
});

const markers = computed(() => [
  {
    position: resortLocation,
    title: t("location.resort_name", "AlKhayma Beach Resort"),
    description: t("location.resort_description", "Luxury beach resort in Alexandria"),
    link: directionsLink.value,
  },
]);

const nearbyPlaces = [
  {
    icon: "🏛️",
    name: t("location.place_library", "Library of Alexandria"),
    distance: t("location.distance_15min", "15 min drive"),
    description: t("location.library_desc", "Ancient library and modern cultural center"),
  },
  {
    icon: "🏰",
    name: t("location.place_fort", "Qaitbay Citadel"),
    distance: t("location.distance_20min", "20 min drive"),
    description: t("location.fort_desc", "15th-century defensive fortress"),
  },
  {
    icon: "🌊",
    name: t("location.place_corniche", "Corniche"),
    distance: t("location.distance_5min", "5 min walk"),
    description: t("location.corniche_desc", "Scenic waterfront promenade"),
  },
  {
    icon: "🛍️",
    name: t("location.place_market", "Souk El Gomaa"),
    distance: t("location.distance_25min", "25 min drive"),
    description: t("location.market_desc", "Traditional Friday market"),
  },
];
</script>

<style scoped>
.location-page {
  min-height: 100vh;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 80px 20px;
  text-align: center;
  color: white;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 16px;
}

.hero-subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
}

/* Map Section */
.map-section {
  padding: 60px 20px;
  background: #f8fafc;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Details Section */
.details-section {
  padding: 60px 20px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.detail-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.detail-icon {
  font-size: 2.5rem;
  margin-bottom: 16px;
}

.detail-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 12px;
}

.detail-content {
  color: #6b7280;
  line-height: 1.6;
}

.cta-section {
  text-align: center;
}

.cta-button {
  display: inline-block;
  padding: 16px 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.1rem;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px -4px rgba(102, 126, 234, 0.5);
}

/* Nearby Section */
.nearby-section {
  padding: 60px 20px;
  background: #f8fafc;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  text-align: center;
  color: #1f2937;
  margin-bottom: 40px;
}

.nearby-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 24px;
}

.nearby-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.nearby-card:hover {
  transform: translateY(-4px);
}

.nearby-icon {
  font-size: 2.5rem;
  margin-bottom: 12px;
}

.nearby-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.nearby-distance {
  color: #667eea;
  font-weight: 500;
  margin-bottom: 8px;
}

.nearby-description {
  font-size: 0.9rem;
  color: #6b7280;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }

  .details-grid {
    grid-template-columns: 1fr;
  }
}
</style>
