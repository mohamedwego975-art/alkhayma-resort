import apiClient from './client'

export interface BookingCreate {
  room_id: number
  check_in: string
  check_out: string
  guests: number
  total_price: number
}

export interface Booking {
  id: number
  user_id: number
  room_id: number
  check_in: string
  check_out: string
  guests: number
  total_price: number
  status: string
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
