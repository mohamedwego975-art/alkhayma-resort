export interface User {
  id: number
  email: string
  full_name: string
  role: 'guest' | 'admin' | 'staff' | 'superadmin'
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  user: User
}

export interface Product {
  id: number
  name: string
  name_ar: string
  type: 'room' | 'activity' | 'service'
  base_price: number
  capacity: number
  description: string
  images: string[]
}

export interface Booking {
  id: number
  user_id: number
  product_id: number
  check_in: string
  check_out: string
  guests: number
  total_price: number
  status: 'pending' | 'confirmed' | 'cancelled'
}
