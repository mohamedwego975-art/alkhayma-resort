import apiClient from "./client";

export interface Room {
  id: number;
  room_number: string;
  room_type: string;
  status: string;
  price_per_night: number;
  capacity: number;
  description_en?: string;
  description_ar?: string;
  amenities?: string;
  is_active: boolean;
  rating?: number;
  review_count?: number;
  created_at: string;
}

export interface RoomCreate {
  room_number: string;
  room_type: string;
  price_per_night: number;
  capacity: number;
  description_en?: string;
  description_ar?: string;
  amenities?: string;
  is_active?: boolean;
}

export const roomApi = {
  // Guest endpoints
  getAll: () => apiClient.get<Room[]>("/rooms"),

  getAvailable: (checkIn: string, checkOut: string, roomType?: string) =>
    apiClient.get<Room[]>("/rooms/available", {
      params: { check_in: checkIn, check_out: checkOut, room_type: roomType },
    }),

  getById: (id: number) => apiClient.get<Room>(`/rooms/${id}`),

  // Admin endpoints
  adminGetAll: (skip = 0, limit = 100) =>
    apiClient.get<Room[]>("/rooms/admin/all", { params: { skip, limit } }),

  adminCreate: (data: RoomCreate) => apiClient.post<Room>("/rooms/admin", data),

  adminUpdate: (id: number, data: Partial<RoomCreate>) =>
    apiClient.patch<Room>(`/rooms/admin/${id}`, data),

  adminDelete: (id: number) => apiClient.delete(`/rooms/admin/${id}`),

  adminUpdateStatus: (id: number, status: string) =>
    apiClient.patch<Room>(`/rooms/admin/${id}/status`, { status }),

  adminToggleActive: (id: number, isActive: boolean) =>
    apiClient.patch<Room>(`/rooms/admin/${id}/active`, { is_active: isActive }),
};
