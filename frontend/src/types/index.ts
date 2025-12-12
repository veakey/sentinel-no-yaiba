export interface User {
  guid: string
  username: string
  email: string
  role: 'admin' | 'client'
  is_active: boolean
}

export interface Threat {
  id: string
  title: string
  description: string
  severity: 'critical' | 'high' | 'medium' | 'low'
  status: 'active' | 'resolved' | 'pending'
  provider: string
  detectedAt: string
  resolvedAt?: string
  metadata?: Record<string, any>
}

export interface Provider {
  guid: string
  name: string
  type: 'ninja' | 'malwarebytes'
  base_url: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface ThreatsResponse {
  [providerName: string]: {
    threats?: Threat[]
    error?: string
    status?: string
  }
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface LoginCredentials {
  username: string
  password: string
}

