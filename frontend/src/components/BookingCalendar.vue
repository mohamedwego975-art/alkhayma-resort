<template>
  <div class="card">
    <h3 class="text-xl font-bold text-ocean-deep-900 mb-4">{{ $t("booking.selectDates") }}</h3>

    <!-- Date Range Selector -->
    <div class="grid grid-cols-2 gap-4 mb-4">
      <div>
        <label class="block text-sm font-medium text-ocean-deep-700 mb-2">{{
          $t("booking.checkIn")
        }}</label>
        <input
          v-model="checkIn"
          type="date"
          :min="minDate"
          class="w-full px-4 py-3 rounded-lg border border-ocean-deep-200 focus:border-ocean-deep-500 focus:ring-2 focus:ring-ocean-deep-200"
          @change="calculateTotal"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-ocean-deep-700 mb-2">{{
          $t("booking.checkOut")
        }}</label>
        <input
          v-model="checkOut"
          type="date"
          :min="checkIn || minDate"
          class="w-full px-4 py-3 rounded-lg border border-ocean-deep-200 focus:border-ocean-deep-500 focus:ring-2 focus:ring-ocean-deep-200"
          @change="calculateTotal"
        />
      </div>
    </div>

    <!-- Guests Selector -->
    <div class="mb-4">
      <label class="block text-sm font-medium text-ocean-deep-700 mb-2">{{
        $t("booking.guests")
      }}</label>
      <div class="flex items-center gap-4">
        <button
          @click="decrementGuests"
          :disabled="guests <= 1"
          class="w-10 h-10 rounded-lg border border-ocean-deep-300 hover:bg-ocean-deep-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          -
        </button>
        <span class="flex-1 text-center font-semibold text-ocean-deep-900"
          >{{ guests }} {{ $t("booking.guests") }}</span
        >
        <button
          @click="incrementGuests"
          :disabled="guests >= maxCapacity"
          class="w-10 h-10 rounded-lg border border-ocean-deep-300 hover:bg-ocean-deep-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          +
        </button>
      </div>
    </div>

    <!-- Price Breakdown -->
    <div v-if="nights > 0" class="bg-ocean-deep-50 rounded-lg p-4 mb-4 space-y-2">
      <div class="flex justify-between text-sm">
        <span class="text-ocean-deep-700"
          >${{ pricePerNight }} × {{ nights }} {{ $t("booking.nights") }}</span
        >
        <span class="font-medium text-ocean-deep-900">${{ subtotal }}</span>
      </div>
      <div class="flex justify-between text-sm">
        <span class="text-ocean-deep-700">{{ $t("booking.serviceFee") }}</span>
        <span class="font-medium text-ocean-deep-900">${{ serviceFee }}</span>
      </div>
      <div class="flex justify-between text-sm">
        <span class="text-ocean-deep-700">{{ $t("booking.taxes") }}</span>
        <span class="font-medium text-ocean-deep-900">${{ taxes }}</span>
      </div>
      <div class="border-t border-ocean-deep-200 pt-2 flex justify-between font-bold text-lg">
        <span class="text-ocean-deep-900">{{ $t("booking.total") }}</span>
        <span class="text-ocean-deep-900">${{ total }}</span>
      </div>
    </div>

    <!-- Availability Status -->
    <div v-if="checkIn && checkOut" class="mb-4">
      <div v-if="checking" class="flex items-center gap-2 text-ocean-deep-600">
        <div class="animate-spin">⏳</div>
        <span>{{ $t("booking.checkingAvailability") }}</span>
      </div>
      <div v-else-if="available" class="flex items-center gap-2 text-green-600">
        <span>✅</span>
        <span>{{ $t("booking.available") }}</span>
      </div>
      <div v-else class="flex items-center gap-2 text-red-600">
        <span>❌</span>
        <span>{{ $t("booking.notAvailable") }}</span>
      </div>
    </div>

    <!-- Book Button -->
    <button
      @click="handleBook"
      :disabled="!canBook"
      class="w-full btn-primary py-4 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {{ $t("booking.bookNow") }}
    </button>

    <!-- Cancellation Policy -->
    <p class="text-xs text-ocean-deep-600 text-center mt-4">
      {{ $t("booking.cancellationPolicy") }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { useNotificationStore } from "@/stores/notifications";

const { t } = useI18n();
const router = useRouter();
const notificationStore = useNotificationStore();

const props = withDefaults(
  defineProps<{
    productId: number;
    pricePerNight: number;
    maxCapacity: number;
    serviceFeePercent?: number;
    taxPercent?: number;
  }>(),
  {
    serviceFeePercent: 10,
    taxPercent: 14,
  },
);

const checkIn = ref("");
const checkOut = ref("");
const guests = ref(2);
const checking = ref(false);
const available = ref(true);

const minDate = computed(() => {
  const today = new Date();
  return today.toISOString().split("T")[0];
});

const nights = computed(() => {
  if (!checkIn.value || !checkOut.value) return 0;
  // Use UTC to avoid timezone issues
  const start = new Date(checkIn.value + "T00:00:00Z");
  const end = new Date(checkOut.value + "T00:00:00Z");
  const diff = end.getTime() - start.getTime();
  return Math.ceil(diff / (1000 * 60 * 60 * 24));
});

const subtotal = computed(() => props.pricePerNight * nights.value);
const serviceFee = computed(() => Math.round(subtotal.value * (props.serviceFeePercent / 100)));
const taxes = computed(() => Math.round(subtotal.value * (props.taxPercent / 100)));
const total = computed(() => subtotal.value + serviceFee.value + taxes.value);

const canBook = computed(() => {
  return (
    checkIn.value &&
    checkOut.value &&
    nights.value > 0 &&
    available.value &&
    guests.value <= props.maxCapacity
  );
});

const incrementGuests = () => {
  if (guests.value < props.maxCapacity) guests.value++;
};

const decrementGuests = () => {
  if (guests.value > 1) guests.value--;
};

const calculateTotal = () => {
  if (checkIn.value && checkOut.value) {
    checkAvailability();
  }
};

const checkAvailability = async () => {
  if (!checkIn.value || !checkOut.value) return;

  checking.value = true;
  try {
    // TODO: Connect to actual availability API
    // const response = await availabilityApi.check({
    //   productId: props.productId,
    //   checkIn: checkIn.value,
    //   checkOut: checkOut.value
    // })
    // available.value = response.data.available

    // For now, simulate availability check based on dates
    // In production, replace with actual API call
    await new Promise((resolve) => setTimeout(resolve, 500));

    // Simple logic: dates must be at least 1 night apart
    available.value = nights.value > 0;
  } catch (error) {
    console.error("Availability check failed:", error);
    available.value = false;
  } finally {
    checking.value = false;
  }
};

const handleBook = () => {
  if (!canBook.value) return;

  // Use in-memory state instead of sessionStorage for security
  // Pass minimal non-sensitive data via router query params
  const queryParams = {
    productId: props.productId.toString(),
    checkIn: checkIn.value,
    checkOut: checkOut.value,
    guests: guests.value.toString(),
    nights: nights.value.toString(),
  };

  notificationStore.success(t("booking.redirecting"));

  // Redirect to booking page with query params
  // The booking page will fetch full details from API using productId
  router.push({ path: `/booking/${props.productId}`, query: queryParams });
};

watch([checkIn, checkOut], () => {
  if (checkIn.value && checkOut.value && new Date(checkOut.value) <= new Date(checkIn.value)) {
    checkOut.value = "";
  }
});
</script>
