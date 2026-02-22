<template>
  <Transition name="fade-scale">
    <div v-if="isVisible" class="upsell-modal-overlay" @click.self="close">
      <div class="upsell-modal">
        <!-- Close Button -->
        <button @click="close" class="close-btn" aria-label="Close">✕</button>

        <!-- Header -->
        <div class="modal-header">
          <span class="upgrade-icon">✨</span>
          <h3>{{ $t("upsell.title") }}</h3>
          <p class="subtitle">{{ $t("upsell.subtitle") }}</p>
        </div>

        <!-- Current vs Upgrade -->
        <div class="comparison">
          <div class="current-option">
            <h4>{{ $t("upsell.current") }}</h4>
            <div class="option-card current">
              <span class="icon">{{ currentItem.icon }}</span>
              <span class="name">{{ currentItem.name }}</span>
              <span class="price">{{ formatPrice(currentItem.price) }}</span>
            </div>
          </div>

          <div class="arrow">➜</div>

          <div class="upgrade-option">
            <h4>{{ $t("upsell.upgrade") }}</h4>
            <div class="option-card upgrade">
              <span class="badge">{{ $t("upsell.recommended") }}</span>
              <span class="icon">{{ upgradeItem.icon }}</span>
              <span class="name">{{ upgradeItem.name }}</span>
              <span class="price">{{ formatPrice(upgradeItem.price) }}</span>
              <ul class="benefits">
                <li v-for="(benefit, index) in upgradeItem.benefits" :key="index">
                  ✓ {{ benefit }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Savings Badge -->
        <div v-if="savings > 0" class="savings-badge">
          {{ $t("upsell.savings", { amount: formatPrice(savings) }) }}
        </div>

        <!-- Urgency Message -->
        <div class="urgency">
          <span class="clock">⏰</span>
          <p>{{ $t("upsell.limitedOffer") }}</p>
          <div class="countdown" v-if="timeRemaining > 0">
            {{ formatCountdown(timeRemaining) }}
          </div>
        </div>

        <!-- Actions -->
        <div class="actions">
          <button @click="acceptUpgrade" class="btn-upgrade">
            {{ $t("upsell.upgradeNow") }}
          </button>
          <button @click="close" class="btn-decline">
            {{ $t("upsell.noThanks") }}
          </button>
        </div>

        <!-- Trust Indicators -->
        <div class="trust">
          <span>🔒 {{ $t("upsell.secure") }}</span>
          <span>✓ {{ $t("upsell.instant") }}</span>
          <span>↩ {{ $t("upsell.refundable") }}</span>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useI18n } from "vue-i18n";

const { t: _ } = useI18n();

interface UpsellItem {
  id: string;
  name: string;
  icon: string;
  price: number;
  benefits?: string[];
}

const props = defineProps<{
  modelValue: boolean;
  currentItem: UpsellItem;
  upgradeItem: UpsellItem;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: boolean];
  accept: [item: UpsellItem];
  decline: [];
}>();

const isVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});

const timeRemaining = ref(900); // 15 minutes in seconds
let countdownInterval: number | null = null;

const savings = computed(() => {
  return Math.max(0, props.currentItem.price - props.upgradeItem.price);
});

const formatPrice = (price: number): string => {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(price);
};

const formatCountdown = (seconds: number): string => {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, "0")}`;
};

const close = () => {
  isVisible.value = false;
  emit("decline");
};

const acceptUpgrade = () => {
  emit("accept", props.upgradeItem);
  isVisible.value = false;
};

onMounted(() => {
  countdownInterval = window.setInterval(() => {
    if (timeRemaining.value > 0) {
      timeRemaining.value--;
    }
  }, 1000);
});

onUnmounted(() => {
  if (countdownInterval) {
    clearInterval(countdownInterval);
  }
});
</script>

<style scoped>
.upsell-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.upsell-modal {
  background: white;
  border-radius: 20px;
  max-width: 500px;
  width: 100%;
  padding: 32px;
  position: relative;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #666;
  padding: 4px;
}

.modal-header {
  text-align: center;
  margin-bottom: 24px;
}

.upgrade-icon {
  font-size: 48px;
  display: block;
  margin-bottom: 12px;
}

.modal-header h3 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
}

.subtitle {
  color: #666;
  margin: 0;
  font-size: 14px;
}

.comparison {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.current-option,
.upgrade-option {
  flex: 1;
  min-width: 150px;
}

.current-option h4,
.upgrade-option h4 {
  font-size: 12px;
  text-transform: uppercase;
  color: #888;
  margin: 0 0 8px 0;
  text-align: center;
}

.option-card {
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.option-card.current {
  background: #f5f5f5;
  border: 2px solid #ddd;
}

.option-card.upgrade {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: 2px solid transparent;
  position: relative;
}

.badge {
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  background: #ffd700;
  color: #333;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 700;
}

.icon {
  font-size: 32px;
}

.name {
  font-weight: 600;
  font-size: 16px;
}

.price {
  font-size: 20px;
  font-weight: 700;
}

.benefits {
  list-style: none;
  padding: 0;
  margin: 8px 0 0 0;
  font-size: 12px;
  text-align: left;
}

.benefits li {
  margin: 4px 0;
}

.arrow {
  font-size: 24px;
  color: #667eea;
}

.savings-badge {
  background: #d4edda;
  color: #155724;
  padding: 12px 20px;
  border-radius: 12px;
  text-align: center;
  font-weight: 600;
  margin-bottom: 20px;
}

.urgency {
  background: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  margin-bottom: 20px;
}

.clock {
  font-size: 24px;
}

.urgency p {
  margin: 8px 0;
  font-size: 14px;
  color: #856404;
}

.countdown {
  font-size: 28px;
  font-weight: 700;
  color: #dc3545;
  font-family: monospace;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.btn-upgrade {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
}

.btn-upgrade:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.btn-decline {
  background: none;
  border: none;
  color: #666;
  padding: 12px;
  font-size: 14px;
  cursor: pointer;
  text-decoration: underline;
}

.trust {
  display: flex;
  justify-content: center;
  gap: 20px;
  font-size: 12px;
  color: #888;
}

/* Transitions */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.3s ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
}

.fade-scale-enter-from .upsell-modal,
.fade-scale-leave-to .upsell-modal {
  transform: scale(0.9);
}
</style>
