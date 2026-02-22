import apiClient from './client'

export interface Review {
  id: number
  product_id: number
  product_name?: string
  user_name: string
  user_email?: string
  rating: number
  comment: string
  country?: string
  flag?: string
  created_at: string
  is_approved: boolean
}

export const reviewApi = {
  getByProductId: (productId: number) =>
    apiClient.get<Review[]>(`/reviews?product_id=${productId}`),

  create: (data: Omit<Review, 'id' | 'created_at' | 'is_approved'>) =>
    apiClient.post<Review>('/reviews', data),
}
