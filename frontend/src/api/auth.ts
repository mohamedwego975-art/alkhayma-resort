import apiClient from './client'

export interface UserRegister {
  email: string
  password: string
  full_name: string
  phone?: string
}

export interface UserLogin {
  email: string
  password: string
}

export interface Token {
  access_token: string
  token_type: string
}

export interface User {
  id: number
  email: string
  full_name: string
  phone?: string
  role: string
  is_active: boolean
  created_at: string
}

export const authApi = {
  register: (data: UserRegister) => 
    apiClient.post<User>('/auth/register', data),
  
  login: (data: UserLogin) => 
    apiClient.post<Token>('/auth/login', data),
  
  getMe: () => 
    apiClient.get<User>('/auth/me'),
  
  logout: () => 
    apiClient.post('/auth/logout'),
}
