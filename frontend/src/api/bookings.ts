import apiClient from './client'

export interface BookingCreate {
  room_id: number
  product_id?: number
  product_type?: string
  check_in: string
  check_out: string
  guests: number
  quantity?: number
  guest_name?: string
  guest_email?: string
  guest_phone?: string
  special_requests?: string
  addons?: number[]
  points_redeemed?: number
  total_price: number
  payment_method?: string
  idempotency_key?: string
}

export interface Booking {
  id: number
  user_id: number
  room_id: number
  product_id?: number
  product_type?: string
  check_in: string
  check_out: string
  guests: number
  quantity?: number
  guest_name?: string
  guest_email?: string
  guest_phone?: string
  special_requests?: string
  addons?: number[]
  points_redeemed?: number
  total_price: number
  status: string
  payment_url?: string
  client_secret?: string
  created_at: string
}

export const bookingApi = {
  create: (data: BookingCreate) =>
    apiClient.post<Booking>('/bookings', data),

  getMyBookings: () =>
    apiClient.get<Booking[]>('/bookings/my-bookings'),

  getById: (id: number) =>
    apiClient.get<Booking>(`/bookings/${id}`),
}
