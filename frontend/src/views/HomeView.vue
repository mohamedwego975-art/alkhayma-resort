<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-blue-600 to-teal-600 text-white py-32">
      <div class="max-w-7xl mx-auto px-4 text-center">
        <h1 class="text-6xl font-bold mb-6">مرحباً بك في منتجع الخيمة</h1>
        <p class="text-2xl mb-8">استمتع بالفخامة على البحر الأحمر</p>
        <router-link to="/rooms" class="inline-block bg-white text-blue-600 px-8 py-4 rounded-lg font-bold text-lg hover:bg-gray-100 transition">
          احجز الآن
        </router-link>
      </div>
    </div>
    
    <!-- Featured Rooms -->
    <div class="max-w-7xl mx-auto px-4 py-20">
      <h2 class="text-4xl font-bold mb-12 text-center">الغرف المميزة</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div v-for="i in 3" :key="i" class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition">
          <div class="h-64 bg-gradient-to-br from-blue-400 to-teal-400"></div>
          <div class="p-6">
            <h3 class="text-2xl font-bold mb-2">غرفة ديلوكس {{ i }}</h3>
            <p class="text-gray-600 mb-4">إطلالة على البحر مع جميع المرافق</p>
            <div class="flex items-center justify-between">
              <span class="text-3xl font-bold text-blue-600">$100</span>
              <span class="text-gray-500">/ ليلة</span>
            </div>
            <router-link to="/rooms" class="mt-4 block text-center bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition font-semibold">
              عرض التفاصيل
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Services -->
    <div class="bg-white py-20">
      <div class="max-w-7xl mx-auto px-4">
        <h2 class="text-4xl font-bold mb-12 text-center">خدماتنا</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="service in services" :key="service.name" class="text-center p-6">
            <div class="text-6xl mb-4">{{ service.icon }}</div>
            <h3 class="text-2xl font-bold mb-2">{{ service.name }}</h3>
            <p class="text-gray-600">{{ service.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA -->
    <div class="bg-gradient-to-r from-teal-600 to-blue-600 text-white py-20">
      <div class="max-w-4xl mx-auto px-4 text-center">
        <h2 class="text-5xl font-bold mb-6">جاهز للحجز؟</h2>
        <p class="text-xl mb-8">احجز الآن واستمتع بعطلة لا تُنسى</p>
        <router-link to="/rooms" class="inline-block bg-white text-blue-600 px-10 py-4 rounded-lg font-bold text-lg hover:bg-gray-100 transition">
          استكشف الغرف
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const services = [
  { name: 'شاطئ خاص', description: 'شاطئ خاص مع كبائن VIP', icon: '🏖️' },
  { name: 'مطعم فاخر', description: 'مأكولات عالمية على البحر', icon: '🍽️' },
  { name: 'أنشطة مائية', description: 'رياضات وأنشطة مثيرة', icon: '🏄' },
]
</script>
