import apiClient from "./client";

export interface UserRegister {
  email: string;
  password: string;
  full_name: string;
  phone?: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  phone?: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export const authApi = {
  // Auth endpoints
  register: (data: UserRegister) => apiClient.post<User>("/auth/register", data),

  login: (data: UserLogin) => apiClient.post<Token>("/auth/login", data),

  getMe: () => apiClient.get<User>("/auth/me"),

  logout: () => apiClient.post("/auth/logout"),

  // Admin endpoints
  adminGetAllUsers: (skip = 0, limit = 100) =>
    apiClient.get<User[]>("/auth/admin/users", { params: { skip, limit } }),

  adminUpdateUser: (id: number, data: Partial<User>) =>
    apiClient.patch<User>(`/auth/admin/users/${id}`, data),

  adminToggleUserActive: (id: number, isActive: boolean) =>
    apiClient.patch<User>(`/auth/admin/users/${id}/active`, { is_active: isActive }),

  adminDeleteUser: (id: number) => apiClient.delete(`/auth/admin/users/${id}`),
};
