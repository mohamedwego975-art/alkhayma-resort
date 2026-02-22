<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <div class="relative bg-gradient-to-br from-ocean-deep-900 via-ocean-deep-700 to-teal-glow-600 py-20 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <span class="inline-block px-4 py-2 mb-4 text-sm font-medium text-white bg-white/10 backdrop-blur-md rounded-full border border-white/20">
          📞 Get in Touch
        </span>
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-4">
          Contact Us
        </h1>
        <p class="text-xl text-white/90 max-w-2xl mx-auto">
          We'd love to hear from you. Reach out for bookings, inquiries, or just to say hello!
        </p>
      </div>
    </div>

    <!-- Contact Section -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-950">
      <div class="max-w-6xl mx-auto">
        <div class="grid lg:grid-cols-3 gap-8">
          <!-- Contact Info Cards -->
          <div class="lg:col-span-1 space-y-6">
            <div class="bg-gray-50 dark:bg-gray-900 rounded-2xl p-6">
              <div class="w-12 h-12 rounded-xl bg-ocean-deep-100 dark:bg-ocean-deep-900 flex items-center justify-center text-2xl mb-4">
                📍
              </div>
              <h3 class="font-bold text-gray-900 dark:text-white mb-2">Address</h3>
              <p class="text-gray-600 dark:text-gray-400">
                South Sinai Governorate<br>
                Sharm El Sheikh, Egypt<br>
                Red Sea Coast
              </p>
            </div>

            <div class="bg-gray-50 dark:bg-gray-900 rounded-2xl p-6">
              <div class="w-12 h-12 rounded-xl bg-ocean-deep-100 dark:bg-ocean-deep-900 flex items-center justify-center text-2xl mb-4">
                📞
              </div>
              <h3 class="font-bold text-gray-900 dark:text-white mb-2">Phone</h3>
              <p class="text-gray-600 dark:text-gray-400">
                +20 69 123 4567<br>
                +20 100 123 4567 (WhatsApp)
              </p>
            </div>

            <div class="bg-gray-50 dark:bg-gray-900 rounded-2xl p-6">
              <div class="w-12 h-12 rounded-xl bg-ocean-deep-100 dark:bg-ocean-deep-900 flex items-center justify-center text-2xl mb-4">
                ✉️
              </div>
              <h3 class="font-bold text-gray-900 dark:text-white mb-2">Email</h3>
              <p class="text-gray-600 dark:text-gray-400">
                info@alkhayma-resort.com<br>
                bookings@alkhayma-resort.com
              </p>
            </div>

            <div class="bg-gray-50 dark:bg-gray-900 rounded-2xl p-6">
              <div class="w-12 h-12 rounded-xl bg-ocean-deep-100 dark:bg-ocean-deep-900 flex items-center justify-center text-2xl mb-4">
                🕐
              </div>
              <h3 class="font-bold text-gray-900 dark:text-white mb-2">Working Hours</h3>
              <p class="text-gray-600 dark:text-gray-400">
                Front Desk: 24/7<br>
                Reservations: 8AM - 10PM<br>
                Restaurant: 7AM - 11PM
              </p>
            </div>
          </div>

          <!-- Contact Form -->
          <div class="lg:col-span-2">
            <div class="bg-white dark:bg-gray-900 rounded-2xl shadow-lg p-8">
              <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Send us a Message</h2>
              
              <form @submit.prevent="submitForm" class="space-y-6">
                <div class="grid md:grid-cols-2 gap-6">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Full Name *
                    </label>
                    <input
                      v-model="form.name"
                      type="text"
                      required
                      class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 focus:border-ocean-deep-500 focus:ring-2 focus:ring-ocean-deep-200 dark:bg-gray-800 dark:text-white transition-all"
                      placeholder="Your name"
                    >
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Email Address *
                    </label>
                    <input
                      v-model="form.email"
                      type="email"
                      required
                      class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 focus:border-ocean-deep-500 focus:ring-2 focus:ring-ocean-deep-200 dark:bg-gray-800 dark:text-white transition-all"
                      placeholder="your@email.com"
                    >
                  </div>
                </div>

                <div class="grid md:grid-cols-2 gap-6">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Phone Number
                    </label>
                    <input
                      v-model="form.phone"
                      type="tel"
                      class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 focus:border-ocean-deep-500 focus:ring-2 focus:ring-ocean-deep-200 dark:bg-gray-800 dark:text-white transition-all"
                      placeholder="+20 XXX XXX XXXX"
                    >
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Subject *
                    </label>
                    <select
                      v-model="form.subject"
                      required
                      class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 focus:border-ocean-deep-500 focus:ring-2 focus:ring-ocean-deep-200 dark:bg-gray-800 dark:text-white transition-all"
                    >
                      <option value="">Select a subject</option>
                      <option value="booking">Booking Inquiry</option>
                      <option value="general">General Question</option>
                      <option value="feedback">Feedback</option>
                      <option value="complaint">Complaint</option>
                      <option value="event">Event Planning</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Message *
                  </label>
                  <textarea
                    v-model="form.message"
                    rows="5"
                    required
                    class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 focus:border-ocean-deep-500 focus:ring-2 focus:ring-ocean-deep-200 dark:bg-gray-800 dark:text-white transition-all resize-none"
                    placeholder="How can we help you?"
                  ></textarea>
                </div>

                <div class="flex items-start gap-3">
                  <input
                    v-model="form.newsletter"
                    type="checkbox"
                    class="w-5 h-5 mt-0.5 rounded border-gray-300 text-ocean-deep-600 focus:ring-ocean-deep-500"
                  >
                  <label class="text-sm text-gray-600 dark:text-gray-400">
                    Subscribe to our newsletter for exclusive offers and updates
                  </label>
                </div>

                <button
                  type="submit"
                  :disabled="submitting"
                  class="btn-primary w-full md:w-auto px-8 py-4 text-lg"
                >
                  <span v-if="submitting">Sending...</span>
                  <span v-else>Send Message →</span>
                </button>
              </form>

              <!-- Success Message -->
              <div v-if="submitted" class="mt-6 p-4 bg-green-50 dark:bg-green-900/20 border-2 border-green-200 dark:border-green-800 rounded-xl">
                <div class="flex items-center gap-3">
                  <span class="text-2xl">✅</span>
                  <div>
                    <p class="font-bold text-green-800 dark:text-green-400">Message Sent!</p>
                    <p class="text-sm text-green-700 dark:text-green-500">We'll get back to you within 24 hours.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Map Section -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-gray-900">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-8">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Find Us</h2>
          <p class="text-gray-600 dark:text-gray-400">Located on the beautiful Red Sea coast</p>
        </div>
        
        <!-- Map Placeholder -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg overflow-hidden">
          <div class="aspect-video bg-gradient-to-br from-ocean-deep-100 to-teal-glow-100 dark:from-ocean-deep-900 dark:to-teal-glow-900 flex items-center justify-center">
            <div class="text-center">
              <span class="text-6xl mb-4">🗺️</span>
              <p class="text-gray-600 dark:text-gray-400">Interactive Map</p>
              <p class="text-sm text-gray-500 dark:text-gray-500">Al-Khayma Beach Resort, Sharm El Sheikh</p>
              <a 
                href="https://maps.google.com/?q=Sharm+El+Sheikh,Egypt" 
                target="_blank"
                class="inline-block mt-4 btn-secondary text-sm"
              >
                Open in Google Maps
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ Teaser -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-950">
      <div class="max-w-4xl mx-auto text-center">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Have Questions?</h2>
        <p class="text-gray-600 dark:text-gray-400 mb-6">
          Check out our frequently asked questions for quick answers.
        </p>
        <router-link to="/faq" class="btn-primary">
          View FAQ →
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { apiClient } from '@/api'
import { useMeta } from '@/composables/useSEO'

// SEO
useMeta({
  title: 'Contact Us - الخيمة Beach Resort',
  description: 'Contact الخيمة Beach Resort for bookings, inquiries, and support. Located in Sharm El Sheikh on the Red Sea coast.',
  keywords: 'contact, Sharm El Sheikh, Red Sea resort, booking inquiry, Egypt'
})

const form = ref({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: '',
  newsletter: false
})

const submitting = ref(false)
const submitted = ref(false)

async function submitForm() {
  submitting.value = true
  try {
    await apiClient.post('/contact', form.value)
    submitted.value = true
    form.value = {
      name: '',
      email: '',
      phone: '',
      subject: '',
      message: '',
      newsletter: false
    }
  } catch (error) {
    console.error('Failed to send message:', error)
    alert('Failed to send message. Please try again.')
  } finally {
    submitting.value = false
  }
}
</script>
