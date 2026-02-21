export interface User {
  id: number
  email: string
  full_name: string
  phone: string | null
  role: 'customer' | 'admin' | 'superadmin'
  is_active: boolean
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export type ProductType = 
  | 'room_standard' | 'room_deluxe' | 'room_suite'
  | 'beach_umbrella' | 'beach_cabana'
  | 'restaurant_table' | 'cafe_seating'
  | 'water_sports' | 'boat_rental' | 'diving'
  | 'event_wedding' | 'event_conference' | 'event_party'

export interface Product {
  id: number
  name: string
  name_ar: string
  slug: string
  type: ProductType
  base_price: string
  capacity: number
  description: string | null
  description_ar: string | null
  images: string[]
  amenities: string[]
  tags: string[]
  min_age: number | null
  max_weight_kg: number | null
  duration_minutes: number | null
  time_slots: string[]
  is_active: boolean
  sort_order: number
  created_at: string
  updated_at: string
}

export interface Booking {
  id: number
  user_id: number
  status: 'pending' | 'confirmed' | 'cancelled' | 'completed'
  check_in: string
  check_out: string
  total_price: string
  created_at: string
}
