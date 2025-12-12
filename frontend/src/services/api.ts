import axios from 'axios'
import type { TokenResponse, LoginCredentials, User, ThreatsResponse } from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor for token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/api/auth/refresh`, {
            refresh_token: refreshToken,
          })
          const { access_token, refresh_token } = response.data
          localStorage.setItem('access_token', access_token)
          localStorage.setItem('refresh_token', refresh_token)
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return apiClient(originalRequest)
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<TokenResponse> => {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)
    
    const response = await axios.post(`${API_BASE_URL}/api/auth/login`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get('/api/auth/me')
    return response.data
  },
}

export const threatsApi = {
  getThreats: async (params?: {
    force_refresh?: boolean
    severity?: string
    status?: string
  }): Promise<ThreatsResponse> => {
    const response = await apiClient.get('/api/threats', { params })
    return response.data
  },
}

export interface Provider {
  guid: string
  name: string
  type: 'ninja' | 'malwarebytes'
  base_url?: string
  is_active: boolean
  created_at: string
  updated_at: string
  config?: {
    client_id?: string
    client_secret?: string
    [key: string]: any
  }
}

export interface ProviderCreateRequest {
  name: string
  type: 'ninja' | 'malwarebytes'
  api_key?: string
  base_url?: string
  config?: {
    client_id?: string
    client_secret?: string
    [key: string]: any
  }
  is_active?: boolean
}

export interface ProviderUpdateRequest {
  name?: string
  api_key?: string
  base_url?: string
  config?: {
    client_id?: string
    client_secret?: string
    [key: string]: any
  }
  is_active?: boolean
}

export const providersApi = {
  getProviders: async (): Promise<Provider[]> => {
    const response = await apiClient.get('/api/admin/providers')
    return response.data
  },

  getProvider: async (guid: string): Promise<Provider> => {
    const response = await apiClient.get(`/api/admin/providers/${guid}`)
    return response.data
  },

  createProvider: async (data: ProviderCreateRequest): Promise<Provider> => {
    const response = await apiClient.post('/api/admin/providers', data)
    return response.data
  },

  updateProvider: async (guid: string, data: ProviderUpdateRequest): Promise<Provider> => {
    const response = await apiClient.put(`/api/admin/providers/${guid}`, data)
    return response.data
  },

  deleteProvider: async (guid: string): Promise<void> => {
    await apiClient.delete(`/api/admin/providers/${guid}`)
  },
}

export default apiClient

