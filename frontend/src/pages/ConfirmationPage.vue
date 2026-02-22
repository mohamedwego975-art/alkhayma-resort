<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 py-8 px-4">
    <div class="max-w-3xl mx-auto">
      <!-- Success Header -->
      <div class="text-center mb-8">
        <div
          class="w-20 h-20 rounded-full bg-green-100 dark:bg-green-900 mx-auto mb-4 flex items-center justify-center"
        >
          <svg
            class="w-10 h-10 text-green-600 dark:text-green-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 13l4 4L19 7"
            ></path>
          </svg>
        </div>
        <h1 class="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Booking Confirmed!
        </h1>
        <p class="text-gray-600 dark:text-gray-400">Thank you for choosing الخيمة Beach Resort</p>
      </div>

      <!-- Booking Card -->
      <div class="bg-white dark:bg-gray-900 rounded-2xl shadow-lg overflow-hidden mb-6">
        <!-- Booking ID Banner -->
        <div class="bg-gradient-to-r from-ocean-deep-500 to-teal-glow-500 px-6 py-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-white/80 text-sm">Booking Reference</p>
              <p class="text-white text-2xl font-bold tracking-wider">#{{ bookingId }}</p>
            </div>
            <div class="text-right">
              <p class="text-white/80 text-sm">Status</p>
              <span class="px-3 py-1 rounded-full text-sm font-bold" :class="statusBadgeClass">
                {{ bookingStatus }}
              </span>
            </div>
          </div>
        </div>

        <div class="p-6 md:p-8">
          <!-- Product Details -->
          <div
            class="flex items-start gap-4 mb-6 pb-6 border-b border-gray-200 dark:border-gray-700"
          >
            <div
              class="w-20 h-20 rounded-xl bg-gradient-to-br from-ocean-deep-400 to-teal-glow-500 flex items-center justify-center text-3xl flex-shrink-0"
            >
              {{ productIcon }}
            </div>
            <div class="flex-1">
              <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-1">
                {{ productName }}
              </h2>
              <p class="text-gray-600 dark:text-gray-400 text-sm">{{ productDescription }}</p>
              <div class="mt-3 flex flex-wrap gap-2">
                <span class="badge bg-ocean-deep-100 dark:bg-ocean-deep-900 text-ocean-deep-700">
                  {{ formatDate(checkIn) }} - {{ formatDate(checkOut) }}
                </span>
                <span class="badge bg-gray-100 dark:bg-gray-800 text-gray-700">
                  {{ guests }} {{ guests === 1 ? "guest" : "guests" }}
                </span>
              </div>
            </div>
          </div>

          <!-- QR Code Section -->
          <div
            class="flex flex-col md:flex-row items-center gap-6 mb-6 pb-6 border-b border-gray-200 dark:border-gray-700"
          >
            <div class="bg-white p-4 rounded-xl shadow-inner">
              <!-- QR Code Placeholder - In production, use a QR library -->
              <div
                class="w-32 h-32 bg-gray-900 rounded-lg flex items-center justify-center text-white text-xs text-center p-2"
              >
                <div>
                  <div class="text-4xl mb-1">📱</div>
                  <div>QR Code</div>
                  <div class="text-[10px] opacity-70">#{{ bookingId }}</div>
                </div>
              </div>
            </div>
            <div class="flex-1 text-center md:text-left">
              <h3 class="font-bold text-gray-900 dark:text-white mb-2">Digital Voucher</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
                Show this QR code at check-in or download your booking voucher
              </p>
              <button
                @click="downloadVoucher"
                class="btn-primary text-sm inline-flex items-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  ></path>
                </svg>
                Download Voucher (PDF)
              </button>
            </div>
          </div>

          <!-- Price Summary -->
          <div class="mb-6 pb-6 border-b border-gray-200 dark:border-gray-700">
            <h3 class="font-bold text-gray-900 dark:text-white mb-4">Price Breakdown</h3>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400"
                  >{{ productName }} ({{ nights }} nights)</span
                >
                <span>${{ basePrice }}</span>
              </div>
              <div v-if="addonsTotal > 0" class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">Add-ons</span>
                <span>${{ addonsTotal }}</span>
              </div>
              <div v-if="discountAmount > 0" class="flex justify-between text-green-600">
                <span>Points Discount</span>
                <span>-${{ discountAmount }}</span>
              </div>
              <div
                class="flex justify-between items-center pt-3 border-t border-gray-200 dark:border-gray-700"
              >
                <span class="font-bold text-lg text-gray-900 dark:text-white">Total Paid</span>
                <span class="font-bold text-2xl gradient-text">${{ totalPrice }}</span>
              </div>
            </div>
          </div>

          <!-- Guest Information -->
          <div class="mb-6">
            <h3 class="font-bold text-gray-900 dark:text-white mb-4">Guest Information</h3>
            <div class="grid md:grid-cols-2 gap-4 text-sm">
              <div>
                <p class="text-gray-500 dark:text-gray-500">Name</p>
                <p class="font-medium text-gray-900 dark:text-white">{{ guestName }}</p>
              </div>
              <div>
                <p class="text-gray-500 dark:text-gray-500">Email</p>
                <p class="font-medium text-gray-900 dark:text-white">{{ guestEmail }}</p>
              </div>
              <div>
                <p class="text-gray-500 dark:text-gray-500">Phone</p>
                <p class="font-medium text-gray-900 dark:text-white">{{ guestPhone }}</p>
              </div>
              <div v-if="specialRequests">
                <p class="text-gray-500 dark:text-gray-500">Special Requests</p>
                <p class="font-medium text-gray-900 dark:text-white">{{ specialRequests }}</p>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="grid md:grid-cols-2 gap-4">
            <!-- WhatsApp Share -->
            <a
              :href="whatsappShareUrl"
              target="_blank"
              class="flex items-center justify-center gap-2 px-6 py-3 bg-green-500 hover:bg-green-600 text-white font-bold rounded-xl transition-colors"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path
                  d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.982 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"
                />
              </svg>
              Share on WhatsApp
            </a>

            <!-- Add to Calendar -->
            <a
              :href="calendarUrl"
              target="_blank"
              class="flex items-center justify-center gap-2 px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-bold rounded-xl transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                ></path>
              </svg>
              Add to Calendar
            </a>
          </div>
        </div>
      </div>

      <!-- Review Prompt (only if booking is completed) -->
      <div
        v-if="bookingStatus === 'confirmed' || bookingStatus === 'completed'"
        class="bg-white dark:bg-gray-900 rounded-2xl shadow-lg p-6 md:p-8 mb-6"
      >
        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
          How was your experience?
        </h3>
        <p class="text-gray-600 dark:text-gray-400 mb-4">
          We value your feedback. Share your experience and help other travelers!
        </p>

        <div class="flex items-center gap-2 mb-4">
          <button
            v-for="star in 5"
            :key="star"
            @click="rating = star"
            class="text-3xl transition-colors"
            :class="star <= rating ? 'text-yellow-400' : 'text-gray-300 dark:text-gray-600'"
          >
            ★
          </button>
        </div>

        <textarea
          v-model="reviewComment"
          rows="3"
          class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 focus:border-ocean-deep-500 focus:ring-2 focus:ring-ocean-deep-200 dark:bg-gray-800 dark:text-white transition-all resize-none mb-4"
          placeholder="Tell us about your stay..."
        ></textarea>

        <button
          @click="submitReview"
          :disabled="!rating || submittingReview"
          class="btn-primary w-full"
          :class="{ 'opacity-50 cursor-not-allowed': !rating || submittingReview }"
        >
          {{ submittingReview ? "Submitting..." : "Submit Review" }}
        </button>
      </div>

      <!-- Navigation -->
      <div class="flex justify-center gap-4">
        <router-link to="/account" class="btn-primary px-8 py-3"> View My Bookings → </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { bookingApi, reviewApi } from "@/api";
import { useMeta } from "@/composables/useSEO";

// SEO
useMeta({
  title: "Booking Confirmed - الخيمة Beach Resort",
  description:
    "Your booking has been confirmed at الخيمة Beach Resort. View your booking details and download your voucher.",
  keywords: "booking confirmed, reservation, vacation booking",
});

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

// Booking details
const bookingId = ref((route.params.id as string) || "");
const bookingStatus = ref((route.query.status as string) || "pending");
const productName = ref("");
const productDescription = ref("");
const checkIn = ref("");
const checkOut = ref("");
const guests = ref(1);
const basePrice = ref(0);
const addonsTotal = ref(0);
const discountAmount = ref(0);
const totalPrice = ref(0);
const guestName = ref("");
const guestEmail = ref("");
const guestPhone = ref("");
const specialRequests = ref("");

// Review
const rating = ref(0);
const reviewComment = ref("");
const submittingReview = ref(false);

const productIcon = computed(() => {
  if (productName.value.toLowerCase().includes("room")) return "🏨";
  if (productName.value.toLowerCase().includes("beach")) return "🏖️";
  return "🎁";
});

const nights = computed(() => {
  if (!checkIn.value || !checkOut.value) return 0;
  const start = new Date(checkIn.value);
  const end = new Date(checkOut.value);
  return Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
});

const statusBadgeClass = computed(() => {
  switch (bookingStatus.value) {
    case "confirmed":
    case "completed":
      return "bg-green-500/20 text-green-300";
    case "pending":
      return "bg-yellow-500/20 text-yellow-300";
    case "cancelled":
      return "bg-red-500/20 text-red-300";
    default:
      return "bg-gray-500/20 text-gray-300";
  }
});

const whatsappShareUrl = computed(() => {
  const text = `I just booked at الخيمة Beach Resort! 🏖️

Booking #${bookingId.value}
${productName.value}
${formatDate(checkIn.value || "")} - ${formatDate(checkOut.value || "")}

Book your stay too at ${window.location.origin}`;
  return `https://wa.me/?text=${encodeURIComponent(text)}`;
});

const calendarUrl = computed(() => {
  const title = encodeURIComponent(`Stay at الخيمة Beach Resort - ${productName.value}`);
  const details = encodeURIComponent(`Booking #${bookingId.value}\n${productDescription.value}`);
  const location = encodeURIComponent("الخيمة Beach Resort, Red Sea, Egypt");
  const checkInValue = (checkIn.value || new Date().toISOString().split("T")[0]) as string;
  const checkOutValue = (checkOut.value ||
    new Date(Date.now() + 86400000).toISOString().split("T")[0]) as string;
  const start = checkInValue.replace(/-/g, "");
  const end = checkOutValue.replace(/-/g, "");
  return `https://www.google.com/calendar/render?action=TEMPLATE&text=${title}&dates=${start}/${end}&details=${details}&location=${location}`;
});

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push({ name: "login", query: { redirect: route.fullPath } });
    return;
  }

  await fetchBookingDetails();
});

async function fetchBookingDetails() {
  try {
    const response = await bookingApi.getById(Number(bookingId.value));
    const booking = response.data as any;

    if (booking) {
      bookingStatus.value = booking.status || "pending";
      checkIn.value = booking.check_in || "";
      checkOut.value = booking.check_out || "";
      guests.value = booking.guests || 1;
      basePrice.value =
        (booking.total_price || 0) -
        (booking.addons?.reduce((sum: number) => {
          // Calculate addon prices - simplified for now
          return sum + 0;
        }, 0) || 0);
      totalPrice.value = booking.total_price || 0;
      guestName.value = booking.guest_name || "";
      guestEmail.value = booking.guest_email || "";
      guestPhone.value = booking.guest_phone || "";
      specialRequests.value = booking.special_requests || "";
    }

    // Try to get product details from localStorage or query params as fallback
    const savedParams = localStorage.getItem("bookingParams");
    if (savedParams) {
      const params = JSON.parse(savedParams);
      productName.value = params.name || "Luxury Room";
      productDescription.value = params.description || "";
    } else {
      productName.value = "Luxury Room";
      productDescription.value = "Comfortable accommodation at الخيمة Beach Resort";
    }
  } catch (error) {
    console.error("Failed to fetch booking details:", error);
    // Use fallback data from query params
    productName.value = (route.query.name as string) || "Luxury Room";
    productDescription.value = (route.query.description as string) || "";
    checkIn.value = ((route.query.checkIn as string) ||
      new Date().toISOString().split("T")[0]) as string;
    checkOut.value = ((route.query.checkOut as string) ||
      new Date(Date.now() + 86400000).toISOString().split("T")[0]) as string;
  }
}

function formatDate(dateString: string | undefined) {
  if (!dateString) return "";
  return new Date(dateString).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function downloadVoucher() {
  // In a real implementation, this would generate a PDF
  // For now, we'll create a simple print-friendly view
  const voucherContent = `
    BOOKING VOUCHER - الخيمة Beach Resort
    =====================================

    Booking Reference: #${bookingId.value}

    Guest: ${guestName.value}
    Email: ${guestEmail.value}
    Phone: ${guestPhone.value}

    Product: ${productName.value}
    Dates: ${formatDate(checkIn.value)} - ${formatDate(checkOut.value)}
    Guests: ${guests.value}

    Total: $${totalPrice.value}

    Please present this voucher at check-in.

    Thank you for choosing الخيمة Beach Resort!
  `;

  const blob = new Blob([voucherContent], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `booking-voucher-${bookingId.value}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

async function submitReview() {
  if (!rating.value) return;

  submittingReview.value = true;
  try {
    await reviewApi.create({
      product_id: Number(bookingId.value),
      user_name: guestName.value,
      rating: rating.value,
      comment: reviewComment.value,
      country: "Unknown",
    });

    alert("Thank you for your review!");
    rating.value = 0;
    reviewComment.value = "";
  } catch (error) {
    console.error("Failed to submit review:", error);
    alert("Failed to submit review. Please try again.");
  } finally {
    submittingReview.value = false;
  }
}
</script>
