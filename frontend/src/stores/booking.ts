import { defineStore } from 'pinia'
import { ref } from 'vue'
import { bookingApi, type Booking, type BookingCreate } from '@/api'

export const useBookingStore = defineStore('booking', () => {
  const bookings = ref<Booking[]>([])
  const currentBooking = ref<Booking | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function createBooking(data: BookingCreate) {
    loading.value = true
    error.value = null
    try {
      const response = await bookingApi.create(data)
      currentBooking.value = response.data
      return response.data
    } catch (e: any) {
      error.value = e.response?.data?.error || 'Booking failed'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchMyBookings() {
    loading.value = true
    error.value = null
    try {
      const response = await bookingApi.getMyBookings()
      bookings.value = response.data
    } catch (e: any) {
      error.value = e.response?.data?.error || 'Failed to fetch bookings'
    } finally {
      loading.value = false
    }
  }

  async function fetchBooking(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await bookingApi.getById(id)
      currentBooking.value = response.data
      return response.data
    } catch (e: any) {
      error.value = e.response?.data?.error || 'Failed to fetch booking'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    bookings,
    currentBooking,
    loading,
    error,
    createBooking,
    fetchMyBookings,
    fetchBooking,
  }
})
