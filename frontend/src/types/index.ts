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

export interface Ticket {
  id: string
  title: string
  description: string
  status: 'open' | 'in_progress' | 'resolved' | 'closed'
  priority: 'low' | 'medium' | 'high' | 'critical'
  assignedTo?: string
  createdBy: string
  createdAt: string
  updatedAt: string
  relatedThreats?: string[]
  tags?: string[]
}

export interface Endpoint {
  id: string
  name: string
  url: string
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
  description: string
  requiresAuth: boolean
  rateLimit?: number
  lastChecked?: string
  status: 'active' | 'inactive' | 'error'
}

export interface SecurityReport {
  id: string
  title: string
  type: 'summary' | 'detailed' | 'incident'
  generatedAt: string
  period: {
    start: string
    end: string
  }
  summary: {
    totalThreats: number
    criticalThreats: number
    resolvedThreats: number
    activeThreats: number
  }
  details?: Record<string, any>
}
