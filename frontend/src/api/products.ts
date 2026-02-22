import apiClient from "./client";

export interface Product {
  id: number;
  name: string;
  name_ar: string;
  type: string;
  base_price: number;
  capacity?: number;
  is_active: boolean;
  created_at: string;
  description?: string;
  description_ar?: string;
}

export interface ProductCreate {
  name: string;
  name_ar: string;
  type: string;
  base_price: number;
  capacity?: number;
  is_active?: boolean;
  description?: string;
  description_ar?: string;
}

export const productApi = {
  // Guest endpoints
  getAll: (skip = 0, limit = 100) =>
    apiClient.get<Product[]>("/products", { params: { skip, limit } }),

  getById: (id: number) => apiClient.get<Product>(`/products/${id}`),

  getByType: (type: string) =>
    apiClient.get<Product[]>("/products", { params: { product_type: type } }),

  // Admin endpoints
  adminCreate: (data: ProductCreate) => apiClient.post<Product>("/products", data),

  adminUpdate: (id: number, data: Partial<ProductCreate>) =>
    apiClient.patch<Product>(`/products/admin/${id}`, data),

  adminDelete: (id: number) => apiClient.delete(`/products/admin/${id}`),

  adminToggleActive: (id: number, isActive: boolean) =>
    apiClient.patch<Product>(`/products/admin/${id}/active`, { is_active: isActive }),
};
