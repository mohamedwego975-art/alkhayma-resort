<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 py-8 px-4">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Complete Your Booking
        </h1>
        <p class="text-gray-600 dark:text-gray-400">
          Just a few steps to secure your perfect getaway
        </p>
      </div>

      <!-- Progress Bar -->
      <div class="mb-8">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-medium text-gray-600 dark:text-gray-400">
            Step {{ currentStep }} of 4
          </span>
          <span class="text-sm font-medium gradient-text">
            {{ Math.round((currentStep / 4) * 100) }}%
          </span>
        </div>
        <div class="h-3 bg-gray-200 dark:bg-gray-800 rounded-full overflow-hidden">
          <div
            class="h-full bg-gradient-to-r from-ocean-deep-500 to-teal-glow-500 transition-all duration-500 ease-out"
            :style="{ width: `${(currentStep / 4) * 100}%` }"
          ></div>
        </div>
        <div class="flex justify-between mt-2">
          <span
            v-for="step in 4"
            :key="step"
            class="text-xs font-medium transition-colors"
            :class="
              currentStep >= step
                ? 'text-ocean-deep-600 dark:text-ocean-deep-400'
                : 'text-gray-400 dark:text-gray-600'
            "
          >
            {{ ["Summary", "Extras", "Guest Info", "Payment"][step - 1] }}
          </span>
        </div>
      </div>

      <!-- Step 1: Summary -->
      <div
        v-if="currentStep === 1"
        class="bg-white dark:bg-gray-900 rounded-2xl shadow-lg p-6 md:p-8"
      >
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
          <span
            class="w-10 h-10 rounded-full bg-ocean-deep-100 dark:bg-ocean-deep-900 text-ocean-deep-600 flex items-center justify-center"
            >1</span
          >
          Booking Summary
        </h2>

        <!-- Product Details -->
        <div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-6 mb-6">
          <div class="flex items-start gap-4">
            <div
              class="w-24 h-24 rounded-xl bg-gradient-to-br from-ocean-deep-400 to-teal-glow-500 flex items-center justify-center text-4xl flex-shrink-0"
            >
              {{ productType === "room" ? "🏨" : productType === "beach" ? "🏖️" : "🎁" }}
            </div>
            <div class="flex-1">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white">{{ productName }}</h3>
              <p class="text-gray-600 dark:text-gray-400 mt-1">{{ productDescription }}</p>
              <div class="mt-3 flex flex-wrap gap-2">
                <span
                  class="badge bg-ocean-deep-100 dark:bg-ocean-deep-900 text-ocean-deep-700 dark:text-ocean-deep-300"
                >
                  {{ formatDate(checkIn || "") }} - {{ formatDate(checkOut || "") }}
                </span>
                <span class="badge bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                  {{ nights }} nights
                </span>
                <span class="badge bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                  {{ guests }} {{ guests === 1 ? "guest" : "guests" }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Quantity Selector -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Quantity
          </label>
          <div class="flex items-center gap-4">
            <button
              @click="quantity = Math.max(1, quantity - 1)"
              class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 flex items-center justify-center transition-colors"
            >
              −
            </button>
            <span class="text-xl font-bold text-gray-900 dark:text-white w-12 text-center">{{
              quantity
            }}</span>
            <button
              @click="quantity++"
              class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 flex items-center justify-center transition-colors"
            >
              +
            </button>
          </div>
        </div>

        <!-- Price Summary -->
        <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
          <div class="space-y-2 mb-4">
            <div class="flex justify-between text-gray-600 dark:text-gray-400">
              <span>Base Price ({{ nights }} nights × ${{ basePricePerNight }})</span>
              <span>${{ basePrice }}</span>
            </div>
            <div
              v-if="addonsTotal > 0"
              class="flex justify-between text-gray-600 dark:text-gray-400"
            >
              <span>Add-ons</span>
              <span>${{ addonsTotal }}</span>
            </div>
            <div v-if="discountAmount > 0" class="flex justify-between text-green-600">
              <span>Discount</span>
              <span>-${{ discountAmount }}</span>
            </div>
          </div>
          <div
            class="flex justify-between items-center pt-4 border-t border-gray-200 dark:border-gray-700"
          >
            <span class="text-lg font-bold text-gray-900 dark:text-white">Total</span>
            <span class="text-3xl font-bold gradient-text">${{ totalPrice }}</span>
          </div>
        </div>

        <!-- Navigation -->
        <div class="flex justify-end mt-8">
          <button @click="nextStep" class="btn-primary px-8 py-3 text-lg">
            Continue to Extras →
          </button>
        </div>
      </div>

      <!-- Step 2: Extras -->
      <div
        v-if="currentStep === 2"
        class="bg-white dark:bg-gray-900 rounded-2xl shadow-lg p-6 md:p-8"
      >
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
          <span
            class="w-10 h-10 rounded-full bg-ocean-deep-100 dark:bg-ocean-deep-900 text-ocean-deep-600 flex items-center justify-center"
            >2</span
          >
          Add Extras
        </h2>

        <!-- Add-ons -->
        <div class="space-y-4 mb-8">
          <div
            v-for="addon in availableAddons"
            :key="addon.id"
            class="flex items-center justify-between p-4 border-2 rounded-xl transition-all cursor-pointer"
            :class="
              selectedAddons.includes(addon.id)
                ? 'border-ocean-deep-500 bg-ocean-deep-50 dark:bg-ocean-deep-900/20'
                : 'border-gray-200 dark:border-gray-700 hover:border-ocean-deep-300'
            "
            @click="toggleAddon(addon.id)"
          >
            <div class="flex items-center gap-4">
              <div
                class="w-12 h-12 rounded-xl bg-gradient-to-br flex items-center justify-center text-2xl"
                :class="addon.gradient || 'from-gray-400 to-gray-500'"
              >
                {{ addon.icon }}
              </div>
              <div>
                <h4 class="font-bold text-gray-900 dark:text-white">{{ addon.name }}</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400">{{ addon.description }}</p>
              </div>
            </div>
            <div class="flex items-center gap-4">
              <span class="text-xl font-bold text-ocean-deep-600 dark:text-ocean-deep-400"
                >+${{ addon.price }}</span
              >
              <div
                class="w-6 h-6 rounded-full border-2 flex items-center justify-center"
                :class="
                  selectedAddons.includes(addon.id)
                    ? 'border-ocean-deep-500 bg-ocean-deep-500 text-white'
                    : 'border-gray-300 dark:border-gray-600'
                "
              >
                <svg
                  v-if="selectedAddons.includes(addon.id)"
                  class="w-4 h-4"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fill-rule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- Loyalty Points -->
        <div
          class="bg-gradient-to-r from-sand-gold-100 to-sand-gold-50 dark:from-sand-gold-900/30 dark:to-sand-gold-800/20 rounded-xl p-6 mb-6"
        >
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-3">
              <span class="text-3xl">⭐</span>
              <div>
                <h4 class="font-bold text-gray-900 dark:text-white">Loyalty Points</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  You have {{ loyaltyPoints }} points available
                </p>
              </div>
            </div>
            <span class="text-2xl font-bold text-sand-gold-600">{{ loyaltyPoints }}</span>
          </div>

          <div v-if="loyaltyPoints > 0" class="space-y-3">
            <label class="flex items-center gap-3 cursor-pointer">
              <input
                v-model="useLoyaltyPoints"
                type="checkbox"
                class="w-5 h-5 rounded border-gray-300 text-sand-gold-600 focus:ring-sand-gold-500"
              />
              <span class="text-gray-700 dark:text-gray-300">Use points for discount</span>
            </label>

            <div v-if="useLoyaltyPoints" class="flex items-center gap-4">
              <input
                v-model.number="pointsToRedeem"
                type="range"
                min="0"
                :max="Math.min(loyaltyPoints, Math.floor(totalPrice))"
                class="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
              <span class="text-lg font-bold text-sand-gold-600 w-20 text-right"
                >{{ pointsToRedeem }} pts</span
              >
            </div>

            <p v-if="useLoyaltyPoints && pointsToRedeem > 0" class="text-sm text-green-600">
              Save ${{ (pointsToRedeem / 100).toFixed(2) }} with {{ pointsToRedeem }} points
            </p>
          </div>
        </div>

        <!-- Real-time Price -->
        <div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-4 mb-6">
          <div class="flex justify-between items-center">
            <span class="text-gray-600 dark:text-gray-400">Current Total</span>
            <span class="text-2xl font-bold gradient-text">${{ totalPrice }}</span>
          </div>
        </div>

        <!-- Navigation -->
        <div class="flex justify-between">
          <button @click="prevStep" class="btn-secondary px-6 py-3">← Back</button>
          <button @click="nextStep" class="btn-primary px-8 py-3">Continue →</button>
        </div>
      </div>

      <!-- Step 3: Guest Info -->
      <div
        v-if="currentStep === 3"
        class="bg-white dark:bg-gray-900 rounded-2xl shadow-lg p-6 md:p-8"
      >
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
          <span
            class="w-10 h-10 rounded-full bg-ocean-deep-100 dark:bg-ocean-deep-900 text-ocean-deep-600 flex items-center justify-center"
            >3</span
          >
          Guest Information
        </h2>

        <form @submit.prevent="validateAndNext" class="space-y-6">
          <div class="grid md:grid-cols-2 gap-6">
            <!-- Name -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Full Name <span class="text-red-500">*</span>
              </label>
              <input
                v-model="guestInfo.name"
                type="text"
                required
                class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 focus:border-ocean-deep-500 focus:ring-2 focus:ring-ocean-deep-200 dark:bg-gray-800 dark:text-white transition-all"
                placeholder="John Doe"
              />
            </div>

            <!-- Email -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Email Address <span class="text-red-500">*</span>
              </label>
              <input
                v-model="guestInfo.email"
                type="email"
                required
                class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 focus:border-ocean-deep-500 focus:ring-2 focus:ring-ocean-deep-200 dark:bg-gray-800 dark:text-white transition-all"
                placeholder="john@example.com"
              />
            </div>
          </div>

          <!-- Phone -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Phone Number <span class="text-red-500">*</span>
            </label>
            <div class="flex gap-2">
              <select
                v-model="guestInfo.countryCode"
                class="w-24 px-3 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 focus:border-ocean-deep-500 dark:bg-gray-800 dark:text-white"
              >
                <option value="+20">🇪🇬 +20</option>
                <option value="+1">🇺🇸 +1</option>
                <option value="+44">🇬🇧 +44</option>
                <option value="+49">🇩🇪 +49</option>
                <option value="+33">🇫🇷 +33</option>
              </select>
              <input
                v-model="guestInfo.phone"
                type="tel"
                required
                class="flex-1 px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 focus:border-ocean-deep-500 focus:ring-2 focus:ring-ocean-deep-200 dark:bg-gray-800 dark:text-white transition-all"
                placeholder="123 456 7890"
              />
            </div>
          </div>

          <!-- Special Requests -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Special Requests
            </label>
            <textarea
              v-model="guestInfo.specialRequests"
              rows="4"
              class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 focus:border-ocean-deep-500 focus:ring-2 focus:ring-ocean-deep-200 dark:bg-gray-800 dark:text-white transition-all resize-none"
              placeholder="Any special requirements, dietary restrictions, or requests..."
            ></textarea>
          </div>

          <!-- Validation Errors -->
          <div
            v-if="validationErrors.length > 0"
            class="bg-red-50 dark:bg-red-900/20 border-2 border-red-200 dark:border-red-800 rounded-xl p-4"
          >
            <div class="flex items-center gap-2 mb-2">
              <span class="text-red-500">⚠️</span>
              <span class="font-bold text-red-700 dark:text-red-400"
                >Please fix the following:</span
              >
            </div>
            <ul class="list-disc list-inside text-red-600 dark:text-red-400 text-sm">
              <li v-for="error in validationErrors" :key="error">{{ error }}</li>
            </ul>
          </div>

          <!-- Navigation -->
          <div class="flex justify-between pt-4">
            <button type="button" @click="prevStep" class="btn-secondary px-6 py-3">← Back</button>
            <button type="submit" class="btn-primary px-8 py-3">Continue to Payment →</button>
          </div>
        </form>
      </div>

      <!-- Step 4: Payment -->
      <div
        v-if="currentStep === 4"
        class="bg-white dark:bg-gray-900 rounded-2xl shadow-lg p-6 md:p-8"
      >
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
          <span
            class="w-10 h-10 rounded-full bg-ocean-deep-100 dark:bg-ocean-deep-900 text-ocean-deep-600 flex items-center justify-center"
            >4</span
          >
          Payment
        </h2>

        <!-- Order Summary -->
        <div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-6 mb-6">
          <h3 class="font-bold text-gray-900 dark:text-white mb-4">Order Summary</h3>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-600 dark:text-gray-400">{{ productName }}</span>
              <span class="font-medium">${{ basePrice }}</span>
            </div>
            <div v-if="addonsTotal > 0" class="flex justify-between">
              <span class="text-gray-600 dark:text-gray-400">Add-ons</span>
              <span class="font-medium">${{ addonsTotal }}</span>
            </div>
            <div v-if="discountAmount > 0" class="flex justify-between text-green-600">
              <span>Loyalty Discount</span>
              <span class="font-medium">-${{ discountAmount }}</span>
            </div>
            <div
              class="border-t border-gray-200 dark:border-gray-700 pt-2 mt-2 flex justify-between text-lg"
            >
              <span class="font-bold text-gray-900 dark:text-white">Total</span>
              <span class="font-bold gradient-text">${{ totalPrice }}</span>
            </div>
          </div>
        </div>

        <!-- Payment Method -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">
            Select Payment Method
          </label>
          <div class="grid md:grid-cols-2 gap-4">
            <button
              @click="paymentMethod = 'paymob'"
              class="p-4 border-2 rounded-xl transition-all flex items-center gap-4"
              :class="
                paymentMethod === 'paymob'
                  ? 'border-ocean-deep-500 bg-ocean-deep-50 dark:bg-ocean-deep-900/20'
                  : 'border-gray-200 dark:border-gray-700 hover:border-ocean-deep-300'
              "
            >
              <div
                class="w-12 h-12 rounded-xl bg-blue-500 flex items-center justify-center text-white font-bold text-lg"
              >
                P
              </div>
              <div class="text-left">
                <div class="font-bold text-gray-900 dark:text-white">Paymob</div>
                <div class="text-sm text-gray-600 dark:text-gray-400">Cards, Wallet, Fawry</div>
              </div>
            </button>

            <button
              @click="paymentMethod = 'stripe'"
              class="p-4 border-2 rounded-xl transition-all flex items-center gap-4"
              :class="
                paymentMethod === 'stripe'
                  ? 'border-ocean-deep-500 bg-ocean-deep-50 dark:bg-ocean-deep-900/20'
                  : 'border-gray-200 dark:border-gray-700 hover:border-ocean-deep-300'
              "
            >
              <div
                class="w-12 h-12 rounded-xl bg-purple-500 flex items-center justify-center text-white font-bold text-lg"
              >
                S
              </div>
              <div class="text-left">
                <div class="font-bold text-gray-900 dark:text-white">Stripe</div>
                <div class="text-sm text-gray-600 dark:text-gray-400">Credit Cards, Apple Pay</div>
              </div>
            </button>
          </div>
        </div>

        <!-- Terms -->
        <div class="mb-6">
          <label class="flex items-start gap-3 cursor-pointer">
            <input
              v-model="agreedToTerms"
              type="checkbox"
              class="w-5 h-5 mt-0.5 rounded border-gray-300 text-ocean-deep-600 focus:ring-ocean-deep-500"
            />
            <span class="text-sm text-gray-600 dark:text-gray-400">
              I agree to the
              <a href="#" class="text-ocean-deep-600 hover:underline">Terms & Conditions</a> and
              <a href="#" class="text-ocean-deep-600 hover:underline">Cancellation Policy</a>
            </span>
          </label>
        </div>

        <!-- Security Note -->
        <div class="flex items-center gap-3 mb-6 p-4 bg-green-50 dark:bg-green-900/20 rounded-xl">
          <span class="text-2xl">🔒</span>
          <div>
            <div class="font-medium text-green-800 dark:text-green-400">Secure Payment</div>
            <div class="text-sm text-green-700 dark:text-green-500">
              Your payment information is encrypted and secure
            </div>
          </div>
        </div>

        <!-- Navigation -->
        <div class="flex justify-between">
          <button @click="prevStep" class="btn-secondary px-6 py-3">← Back</button>
          <button
            @click="processPayment"
            :disabled="!agreedToTerms || processingPayment"
            class="btn-primary px-8 py-3 text-lg relative"
            :class="{ 'opacity-50 cursor-not-allowed': !agreedToTerms || processingPayment }"
          >
            <span v-if="processingPayment" class="flex items-center gap-2">
              <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                  fill="none"
                ></circle>
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              Processing...
            </span>
            <span v-else> Pay ${{ totalPrice }} → </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { bookingApi, apiClient } from "@/api";
import { useMeta } from "@/composables/useSEO";

// SEO
useMeta({
  title: "Complete Your Booking - الخيمة Beach Resort",
  description:
    "Secure your booking at الخيمة Beach Resort. Choose add-ons, enter guest information, and complete payment.",
  keywords: "booking, reservation, payment, vacation booking",
});

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

// Step management
const currentStep = ref(1);
const processingPayment = ref(false);
const idempotencyKey = ref("");

// Generate idempotency key on mount
onMounted(() => {
  idempotencyKey.value = crypto.randomUUID();

  // Check if user is authenticated
  if (!authStore.isAuthenticated) {
    router.push({ name: "login", query: { redirect: route.fullPath } });
    return;
  }

  // Load booking params from query or localStorage
  loadBookingParams();

  // Fetch loyalty points
  fetchLoyaltyPoints();
});

// Booking params from route query
const productId = ref(Number(route.query.productId) || 0);
const productType = ref((route.query.type as string) || "room");
const productName = ref((route.query.name as string) || "Luxury Room");
const productDescription = ref((route.query.description as string) || "Comfortable accommodation");
const checkIn = ref((route.query.checkIn as string) || new Date().toISOString().split("T")[0]);
const checkOut = ref(
  (route.query.checkOut as string) || new Date(Date.now() + 86400000).toISOString().split("T")[0],
);
const guests = ref(Number(route.query.guests) || 1);
const basePricePerNight = ref(Number(route.query.price) || 100);

// Quantity
const quantity = ref(1);

// Loyalty
const loyaltyPoints = ref(0);
const useLoyaltyPoints = ref(false);
const pointsToRedeem = ref(0);

// Add-ons
const selectedAddons = ref<number[]>([]);
const availableAddons = ref([
  {
    id: 1,
    name: "VIP Beach Access",
    description: "Private cabana with premium amenities",
    price: 65,
    icon: "🏖️",
    gradient: "from-sand-gold-400 to-sand-gold-600",
  },
  {
    id: 2,
    name: "Dinner Package",
    description: "3-course meal at our restaurant",
    price: 50,
    icon: "🍽️",
    gradient: "from-red-400 to-orange-500",
  },
  {
    id: 3,
    name: "Airport Transfer",
    description: "Private car pickup and drop-off",
    price: 40,
    icon: "🚗",
    gradient: "from-blue-400 to-blue-600",
  },
  {
    id: 4,
    name: "Spa Treatment",
    description: "60-minute relaxing massage",
    price: 80,
    icon: "💆",
    gradient: "from-purple-400 to-pink-500",
  },
]);

// Guest info
const guestInfo = ref({
  name: authStore.user?.full_name || "",
  email: authStore.user?.email || "",
  phone: "",
  countryCode: "+20",
  specialRequests: "",
});

// Payment
const paymentMethod = ref<"paymob" | "stripe">("paymob");
const agreedToTerms = ref(false);
const validationErrors = ref<string[]>([]);

// Computed values
const nights = computed(() => {
  const start = new Date(checkIn.value || new Date());
  const end = new Date(checkOut.value || new Date(Date.now() + 86400000));
  const diff = end.getTime() - start.getTime();
  return Math.max(1, Math.ceil(diff / (1000 * 60 * 60 * 24)));
});

const basePrice = computed(() => {
  return nights.value * basePricePerNight.value * quantity.value;
});

const addonsTotal = computed(() => {
  return selectedAddons.value.reduce((sum, addonId) => {
    const addon = availableAddons.value.find((a) => a.id === addonId);
    return sum + (addon?.price || 0);
  }, 0);
});

const discountAmount = computed(() => {
  if (useLoyaltyPoints.value && pointsToRedeem.value > 0) {
    return Math.floor(pointsToRedeem.value / 100);
  }
  return 0;
});

const totalPrice = computed(() => {
  return Math.max(0, basePrice.value + addonsTotal.value - discountAmount.value);
});

// Methods
function loadBookingParams() {
  // Try to load from localStorage if not in query
  const saved = localStorage.getItem("bookingParams");
  if (saved && !route.query.productId) {
    const params = JSON.parse(saved);
    productId.value = params.productId;
    productType.value = params.type;
    productName.value = params.name;
    checkIn.value = params.checkIn;
    checkOut.value = params.checkOut;
    guests.value = params.guests;
    basePricePerNight.value = params.price;
  }
}

async function fetchLoyaltyPoints() {
  try {
    const response = await apiClient.get("/loyalty/balance");
    loyaltyPoints.value = response.data.balance || 0;
  } catch (e) {
    console.error("Failed to fetch loyalty points:", e);
  }
}

function toggleAddon(addonId: number) {
  const index = selectedAddons.value.indexOf(addonId);
  if (index > -1) {
    selectedAddons.value.splice(index, 1);
  } else {
    selectedAddons.value.push(addonId);
  }
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function validateGuestInfo() {
  validationErrors.value = [];

  if (!guestInfo.value.name.trim()) {
    validationErrors.value.push("Full name is required");
  }

  if (!guestInfo.value.email.trim()) {
    validationErrors.value.push("Email is required");
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(guestInfo.value.email)) {
    validationErrors.value.push("Please enter a valid email address");
  }

  if (!guestInfo.value.phone.trim()) {
    validationErrors.value.push("Phone number is required");
  }

  return validationErrors.value.length === 0;
}

function validateAndNext() {
  if (validateGuestInfo()) {
    nextStep();
  }
}

function nextStep() {
  if (currentStep.value < 4) {
    currentStep.value++;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
}

function prevStep() {
  if (currentStep.value > 1) {
    currentStep.value--;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
}

async function processPayment() {
  if (!agreedToTerms.value) return;

  processingPayment.value = true;

  try {
    // Create booking with proper defaults
    const today = new Date().toISOString().split("T")[0];
    const tomorrow = new Date(Date.now() + 86400000).toISOString().split("T")[0];

    const bookingData = {
      room_id: productId.value,
      product_id: productId.value,
      product_type: productType.value,
      check_in: (checkIn.value || today) as string,
      check_out: (checkOut.value || tomorrow) as string,
      guests: guests.value,
      quantity: quantity.value,
      guest_name: guestInfo.value.name,
      guest_email: guestInfo.value.email,
      guest_phone: `${guestInfo.value.countryCode} ${guestInfo.value.phone}`,
      special_requests: guestInfo.value.specialRequests,
      addons: selectedAddons.value,
      points_redeemed: useLoyaltyPoints.value ? pointsToRedeem.value : 0,
      total_price: totalPrice.value,
      payment_method: paymentMethod.value,
      idempotency_key: idempotencyKey.value,
    };

    const response = await bookingApi.create(bookingData);
    const booking: any = response.data;

    // Redirect to payment gateway or confirmation
    if (paymentMethod.value === "paymob" && booking?.payment_url) {
      window.location.href = booking.payment_url;
    } else if (paymentMethod.value === "stripe" && booking?.client_secret) {
      // Handle Stripe payment - redirect to Stripe checkout
      router.push({
        name: "payment-stripe",
        params: { bookingId: booking.id },
        query: { client_secret: booking.client_secret },
      });
    } else {
      // Redirect to confirmation page
      router.push({
        name: "booking-confirmation",
        params: { id: booking.id },
        query: { status: "pending" },
      });
    }
  } catch (error: any) {
    console.error("Booking failed:", error);
    alert(error.response?.data?.error || "Failed to create booking. Please try again.");
    processingPayment.value = false;
  }
}
</script>
