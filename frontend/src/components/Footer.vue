<template>
  <footer
    class="relative bg-gradient-to-br from-gray-900 via-ocean-deep-900 to-gray-900 dark:from-slate-950 dark:via-gray-900 dark:to-slate-950 text-white overflow-hidden transition-colors"
  >
    <!-- Background Pattern -->
    <div class="absolute inset-0 opacity-5">
      <div
        class="absolute inset-0"
        style="
          background-image: radial-gradient(circle, #ffffff 1px, transparent 1px);
          background-size: 30px 30px;
        "
      ></div>
    </div>

    <div class="container-responsive section-padding relative z-10">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-12">
        <!-- About -->
        <div>
          <div class="flex items-center gap-3 mb-6">
            <div
              class="w-12 h-12 rounded-xl bg-gradient-to-br from-ocean-deep-500 to-teal-glow-500 flex items-center justify-center text-2xl"
            >
              🏖️
            </div>
            <div>
              <h3 class="heading-display text-xl gradient-text">الخيمة</h3>
              <span class="text-xs text-gray-400">Beach Resort</span>
            </div>
          </div>
          <p class="text-gray-400 text-sm leading-relaxed">
            Experience luxury by the Red Sea. Your perfect escape awaits at Egypt's premier beach
            destination.
          </p>
        </div>

        <!-- Quick Links -->
        <div>
          <h4 class="font-bold mb-6 text-lg">Quick Links</h4>
          <ul class="space-y-3">
            <li>
              <router-link
                to="/"
                class="text-gray-400 hover:text-white transition-colors inline-flex items-center gap-2 group"
              >
                <span class="transform group-hover:translate-x-1 transition-transform">→</span>
                Home
              </router-link>
            </li>
            <li>
              <router-link
                to="/rooms"
                class="text-gray-400 hover:text-white transition-colors inline-flex items-center gap-2 group"
              >
                <span class="transform group-hover:translate-x-1 transition-transform">→</span>
                Rooms
              </router-link>
            </li>
            <li>
              <router-link
                to="/beach"
                class="text-gray-400 hover:text-white transition-colors inline-flex items-center gap-2 group"
              >
                <span class="transform group-hover:translate-x-1 transition-transform">→</span>
                Beach
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Contact -->
        <div>
          <h4 class="font-bold mb-6 text-lg">Contact Us</h4>
          <ul class="space-y-4 text-sm">
            <li class="flex items-start gap-3 text-gray-400">
              <span class="text-ocean-deep-400 text-lg">📧</span>
              <div>
                <div class="text-white font-medium mb-1">Email</div>
                <a
                  href="mailto:info@alkhayma-resort.com"
                  class="hover:text-white transition-colors"
                >
                  info@alkhayma-resort.com
                </a>
              </div>
            </li>
            <li class="flex items-start gap-3 text-gray-400">
              <span class="text-ocean-deep-400 text-lg">📞</span>
              <div>
                <div class="text-white font-medium mb-1">Phone</div>
                <a href="tel:+201234567890" class="hover:text-white transition-colors">
                  +20 123 456 7890
                </a>
              </div>
            </li>
            <li class="flex items-start gap-3 text-gray-400">
              <span class="text-ocean-deep-400 text-lg">📍</span>
              <div>
                <div class="text-white font-medium mb-1">Location</div>
                Red Sea, Egypt
              </div>
            </li>
          </ul>
        </div>

        <!-- Social & Newsletter -->
        <div>
          <h4 class="font-bold mb-6 text-lg">Stay Connected</h4>
          <div class="flex gap-3 mb-6">
            <a
              href="#"
              class="w-12 h-12 rounded-xl bg-white/10 hover:bg-white/20 flex items-center justify-center transition-all hover:scale-110 backdrop-blur-sm"
            >
              <span class="text-xl">f</span>
            </a>
            <a
              href="#"
              class="w-12 h-12 rounded-xl bg-white/10 hover:bg-white/20 flex items-center justify-center transition-all hover:scale-110 backdrop-blur-sm"
            >
              <span class="text-xl">𝕏</span>
            </a>
            <a
              href="#"
              class="w-12 h-12 rounded-xl bg-white/10 hover:bg-white/20 flex items-center justify-center transition-all hover:scale-110 backdrop-blur-sm"
            >
              <span class="text-xl">in</span>
            </a>
            <a
              href="#"
              class="w-12 h-12 rounded-xl bg-white/10 hover:bg-white/20 flex items-center justify-center transition-all hover:scale-110 backdrop-blur-sm"
            >
              <span class="text-xl">📷</span>
            </a>
          </div>
          <div class="glass-dark rounded-xl p-4">
            <p class="text-sm text-gray-300 mb-3">Subscribe to our newsletter</p>
            <div class="flex gap-2">
              <input
                type="email"
                placeholder="Your email"
                class="flex-1 px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-sm text-white placeholder:text-gray-400 focus:outline-none focus:border-ocean-deep-400 focus:bg-white/20 transition-colors"
              />
              <button class="btn-primary text-sm px-4">→</button>
            </div>
          </div>
        </div>
      </div>

      <div class="divider"></div>

      <div
        class="flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-gray-400"
      >
        <p>&copy; {{ currentYear }} الخيمة Beach Resort. All rights reserved.</p>
        <div class="flex gap-6">
          <a href="#" class="hover:text-white transition-colors">Privacy Policy</a>
          <a href="#" class="hover:text-white transition-colors">Terms of Service</a>
          <a href="#" class="hover:text-white transition-colors">Sitemap</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from "vue";

const currentYear = computed(() => new Date().getFullYear());
</script>
