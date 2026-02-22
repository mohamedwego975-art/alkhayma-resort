<template>
  <div class="map-container">
    <GoogleMap
      :api-key="apiKey"
      :center="center"
      :zoom="zoom"
      :map-type-id="mapTypeId"
      :options="mapOptions"
      style="width: 100%; height: 100%"
    >
      <Marker
        v-for="(marker, index) in markers"
        :key="index"
        :options="marker"
        @click="onMarkerClick(marker)"
      />
      <InfoWindow
        v-if="selectedMarker"
        :options="{ position: selectedMarker.position }"
        @closeclick="selectedMarker = null"
      >
        <div class="info-window">
          <h3 class="info-title">{{ selectedMarker.title }}</h3>
          <p class="info-description">{{ selectedMarker.description }}</p>
          <a
            v-if="selectedMarker.link"
            :href="selectedMarker.link"
            target="_blank"
            class="info-link"
          >
            {{ t('map.get_directions') }}
          </a>
        </div>
      </InfoWindow>
    </GoogleMap>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { GoogleMap, Marker, InfoWindow } from 'vue3-google-map'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

interface MapMarker {
  position: { lat: number; lng: number }
  title: string
  description?: string
  link?: string
  icon?: string
}

interface Props {
  center?: { lat: number; lng: number }
  zoom?: number
  markers?: MapMarker[]
  mapTypeId?: string
  height?: string
}

const props = withDefaults(defineProps<Props>(), {
  center: () => ({ lat: 31.2001, lng: 29.9187 }), // Alexandria, Egypt default
  zoom: 15,
  markers: () => [],
  mapTypeId: 'roadmap',
  height: '400px'
})

const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || ''
const selectedMarker = ref<MapMarker | null>(null)

const center = computed(() => props.center)
const zoom = computed(() => props.zoom)
const mapTypeId = computed(() => props.mapTypeId)

const mapOptions = {
  zoomControl: true,
  mapTypeControl: true,
  scaleControl: true,
  streetViewControl: true,
  rotateControl: true,
  fullscreenControl: true,
  styles: [
    {
      featureType: 'poi',
      elementType: 'labels',
      stylers: [{ visibility: 'off' }]
    }
  ]
}

const onMarkerClick = (marker: MapMarker) => {
  selectedMarker.value = marker
}

const defaultMarkers = computed<MapMarker[]>(() => {
  if (props.markers.length > 0) return props.markers
  
  // Default resort marker
  return [{
    position: props.center,
    title: t('map.resort_title', 'AlKhayma Beach Resort'),
    description: t('map.resort_description', 'Your luxury beach getaway in Alexandria'),
    link: `https://www.google.com/maps/dir/?api=1&destination=${props.center.lat},${props.center.lng}`
  }]
})
</script>

<style scoped>
.map-container {
  width: 100%;
  height: v-bind(height);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.info-window {
  padding: 12px;
  min-width: 200px;
}

.info-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #1f2937;
}

.info-description {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 12px;
}

.info-link {
  display: inline-block;
  padding: 8px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  transition: transform 0.2s;
}

.info-link:hover {
  transform: translateY(-1px);
}
</style>
