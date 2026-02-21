import apiClient from './client'

export interface Room {
  id: number
  room_number: string
  room_type: string
  status: string
  price_per_night: number
  capacity: number
  description_en?: string
  description_ar?: string
  amenities?: string
  is_active: boolean
  created_at: string
}

export const roomApi = {
  getAll: () => 
    apiClient.get<Room[]>('/rooms'),
  
  getAvailable: (checkIn: string, checkOut: string, roomType?: string) => 
    apiClient.get<Room[]>('/rooms/available', { 
      params: { check_in: checkIn, check_out: checkOut, room_type: roomType } 
    }),
  
  getById: (id: number) => 
    apiClient.get<Room>(`/rooms/${id}`),
}
