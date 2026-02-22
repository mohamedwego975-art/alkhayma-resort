<template>
  <div class="settings-page">
    <div class="page-header">
      <h1>{{ $t("admin.settings") }}</h1>
      <p class="subtitle">{{ $t("admin.manageSystemSettings") }}</p>
    </div>

    <!-- Error Banner -->
    <div v-if="error" class="error-banner" role="alert">
      <span>⚠️ {{ error }}</span>
      <button @click="error = null">✕</button>
    </div>

    <!-- Success Banner -->
    <div v-if="success" class="success-banner" role="status">
      <span>✓ {{ success }}</span>
      <button @click="success = null">✕</button>
    </div>

    <!-- Settings Sections -->
    <div class="settings-container">
      <!-- General Settings -->
      <section class="settings-section">
        <div class="section-header">
          <h2>{{ $t("admin.generalSettings") }}</h2>
        </div>
        <form @submit.prevent="saveGeneralSettings" class="settings-form">
          <div class="form-group">
            <label for="resort_name">{{ $t("admin.resortName") }}</label>
            <input
              id="resort_name"
              v-model="settings.resort_name"
              type="text"
              class="form-input"
              placeholder="Alkhayma Resort"
            />
          </div>
          <div class="form-group">
            <label for="resort_email">{{ $t("admin.resortEmail") }}</label>
            <input
              id="resort_email"
              v-model="settings.resort_email"
              type="email"
              class="form-input"
              placeholder="info@alkhayma.com"
            />
          </div>
          <div class="form-group">
            <label for="resort_phone">{{ $t("admin.resortPhone") }}</label>
            <input
              id="resort_phone"
              v-model="settings.resort_phone"
              type="tel"
              class="form-input"
              placeholder="+20 123 4567890"
            />
          </div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="saving">
              {{ saving ? $t("common.saving") : $t("common.save") }}
            </button>
          </div>
        </form>
      </section>

      <!-- Booking Settings -->
      <section class="settings-section">
        <div class="section-header">
          <h2>{{ $t("admin.bookingSettings") }}</h2>
        </div>
        <form @submit.prevent="saveBookingSettings" class="settings-form">
          <div class="form-group">
            <label for="checkin_time">{{ $t("admin.checkInTime") }}</label>
            <input
              id="checkin_time"
              v-model="settings.check_in_time"
              type="time"
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="checkout_time">{{ $t("admin.checkOutTime") }}</label>
            <input
              id="checkout_time"
              v-model="settings.check_out_time"
              type="time"
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="min_stay">{{ $t("admin.minimumStay") }} (nights)</label>
            <input
              id="min_stay"
              v-model.number="settings.minimum_stay"
              type="number"
              min="1"
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="cancellation_days">{{ $t("admin.cancellationPolicy") }} (days)</label>
            <input
              id="cancellation_days"
              v-model.number="settings.cancellation_days"
              type="number"
              min="0"
              class="form-input"
            />
          </div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="saving">
              {{ saving ? $t("common.saving") : $t("common.save") }}
            </button>
          </div>
        </form>
      </section>

      <!-- Payment Settings -->
      <section class="settings-section">
        <div class="section-header">
          <h2>{{ $t("admin.paymentSettings") }}</h2>
        </div>
        <form @submit.prevent="savePaymentSettings" class="settings-form">
          <div class="form-group">
            <label>
              <input v-model="settings.enable_stripe" type="checkbox" />
              {{ $t("admin.enableStripe") }}
            </label>
          </div>
          <div class="form-group">
            <label>
              <input v-model="settings.enable_paymob" type="checkbox" />
              {{ $t("admin.enablePaymob") }}
            </label>
          </div>
          <div class="form-group">
            <label for="currency">{{ $t("admin.currency") }}</label>
            <select id="currency" v-model="settings.currency" class="form-input">
              <option value="EGP">Egyptian Pound (EGP)</option>
              <option value="USD">US Dollar (USD)</option>
              <option value="EUR">Euro (EUR)</option>
              <option value="SAR">Saudi Riyal (SAR)</option>
              <option value="AED">UAE Dirham (AED)</option>
            </select>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="saving">
              {{ saving ? $t("common.saving") : $t("common.save") }}
            </button>
          </div>
        </form>
      </section>

      <!-- System Settings -->
      <section class="settings-section">
        <div class="section-header">
          <h2>{{ $t("admin.systemSettings") }}</h2>
        </div>
        <form class="settings-form">
          <div class="setting-row">
            <div class="setting-info">
              <h4>{{ $t("admin.maintenanceMode") }}</h4>
              <p>{{ $t("admin.maintenanceModeDesc") }}</p>
            </div>
            <label class="toggle-switch">
              <input v-model="settings.maintenance_mode" type="checkbox" />
              <span class="toggle"></span>
            </label>
          </div>

          <div class="setting-row">
            <div class="setting-info">
              <h4>{{ $t("admin.allBookingsEmail") }}</h4>
              <p>{{ $t("admin.sendEmailNotifications") }}</p>
            </div>
            <label class="toggle-switch">
              <input v-model="settings.send_confirmation_emails" type="checkbox" />
              <span class="toggle"></span>
            </label>
          </div>

          <div class="form-actions">
            <button
              type="button"
              @click="saveSystemSettings"
              class="btn btn-primary"
              :disabled="saving"
            >
              {{ saving ? $t("common.saving") : $t("common.save") }}
            </button>
          </div>
        </form>
      </section>

      <!-- System Information -->
      <section class="settings-section">
        <div class="section-header">
          <h2>{{ $t("admin.systemInfo") }}</h2>
        </div>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">{{ $t("admin.version") }}</span>
            <span class="value">1.0.0</span>
          </div>
          <div class="info-item">
            <span class="label">{{ $t("admin.environment") }}</span>
            <span class="value">{{ environment }}</span>
          </div>
          <div class="info-item">
            <span class="label">{{ $t("admin.lastUpdate") }}</span>
            <span class="value">{{ lastUpdate }}</span>
          </div>
          <div class="info-item">
            <span class="label">{{ $t("admin.apiVersion") }}</span>
            <span class="value">v1</span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const error = ref<string | null>(null);
const success = ref<string | null>(null);
const saving = ref(false);
const environment = "Production";
const lastUpdate = new Date().toLocaleDateString();

const settings = ref({
  // General
  resort_name: "Alkhayma Resort",
  resort_email: "info@alkhayma.com",
  resort_phone: "+201001234567",

  // Booking
  check_in_time: "15:00",
  check_out_time: "11:00",
  minimum_stay: 1,
  cancellation_days: 7,

  // Payment
  enable_stripe: true,
  enable_paymob: true,
  currency: "EGP",

  // System
  maintenance_mode: false,
  send_confirmation_emails: true,
});

async function saveGeneralSettings() {
  saving.value = true;
  error.value = null;
  try {
    // API call would go here
    await new Promise((resolve) => setTimeout(resolve, 500));
    success.value = "General settings saved successfully";
    setTimeout(() => (success.value = null), 3000);
  } catch (err: unknown) {
    error.value = "Failed to save settings";
  } finally {
    saving.value = false;
  }
}

async function saveBookingSettings() {
  saving.value = true;
  error.value = null;
  try {
    // API call would go here
    await new Promise((resolve) => setTimeout(resolve, 500));
    success.value = "Booking settings saved successfully";
    setTimeout(() => (success.value = null), 3000);
  } catch (err: unknown) {
    error.value = "Failed to save settings";
  } finally {
    saving.value = false;
  }
}

async function savePaymentSettings() {
  saving.value = true;
  error.value = null;
  try {
    // API call would go here
    await new Promise((resolve) => setTimeout(resolve, 500));
    success.value = "Payment settings saved successfully";
    setTimeout(() => (success.value = null), 3000);
  } catch (err: unknown) {
    error.value = "Failed to save settings";
  } finally {
    saving.value = false;
  }
}

async function saveSystemSettings() {
  saving.value = true;
  error.value = null;
  try {
    // API call would go here
    await new Promise((resolve) => setTimeout(resolve, 500));
    success.value = "System settings saved successfully";
    setTimeout(() => (success.value = null), 3000);
  } catch (err: unknown) {
    error.value = "Failed to save settings";
  } finally {
    saving.value = false;
  }
}
</script>

<style scoped>
.settings-page {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 1.875rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  color: #1f2937;
}

.subtitle {
  color: #6b7280;
  margin: 0;
  font-size: 0.95rem;
}

.error-banner,
.success-banner {
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.error-banner {
  background: #fee2e2;
  border: 1px solid #f87171;
  color: #991b1b;
}

.success-banner {
  background: #d1fae5;
  border: 1px solid #6ee7b7;
  color: #065f46;
}

.error-banner button,
.success-banner button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.settings-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.settings-section {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.section-header {
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #f3f4f6;
  padding-bottom: 1rem;
}

.section-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: #1f2937;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #374151;
  font-size: 0.9rem;
}

.form-group input[type="checkbox"] {
  width: auto;
  margin-right: 0.5rem;
}

.form-input {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary, #4f46e5);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.btn {
  padding: 0.625rem 1.25rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: var(--color-primary, #4f46e5);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #4338ca;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.setting-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.5rem;
}

.setting-info h4 {
  margin: 0 0 0.25rem 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1f2937;
}

.setting-info p {
  margin: 0;
  font-size: 0.85rem;
  color: #6b7280;
}

.toggle-switch {
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.toggle-switch input {
  display: none;
}

.toggle {
  display: inline-block;
  width: 2.5rem;
  height: 1.25rem;
  background: #cbd5e1;
  border-radius: 999px;
  position: relative;
  transition: background 0.2s;
  margin: 0 0.5rem;
}

.toggle-switch input:checked + .toggle {
  background: var(--color-primary, #4f46e5);
}

.toggle::after {
  content: "";
  position: absolute;
  width: 1rem;
  height: 1rem;
  background: white;
  border-radius: 50%;
  top: 0.125rem;
  left: 0.125rem;
  transition: transform 0.2s;
}

.toggle-switch input:checked + .toggle::after {
  transform: translateX(1.25rem);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item .label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-item .value {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
}
</style>
