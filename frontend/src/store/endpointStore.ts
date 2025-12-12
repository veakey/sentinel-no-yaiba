import { create } from 'zustand'
import { malwarebytesApi } from '@/services/api'

interface EndpointSummary {
  endpoints: any[]
  policies: any[]
  summary: {
    total: number
    os_distribution: Record<string, number>
    protection_status: {
      protected: number
      unprotected: number
    }
    policy_distribution: Record<string, number>
    activity_distribution: {
      active: number
      inactive: number
    }
  }
}

interface EndpointState {
  data: EndpointSummary | null
  isLoading: boolean
  error: string | null
  fetchEndpointSummary: () => Promise<void>
}

export const useEndpointStore = create<EndpointState>((set) => ({
  data: null,
  isLoading: false,
  error: null,

  fetchEndpointSummary: async () => {
    set({ isLoading: true, error: null })
    try {
      const data = await malwarebytesApi.getEndpointSummary()
      set({ data, isLoading: false })
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || error.message || 'Failed to fetch endpoint summary',
        isLoading: false,
      })
    }
  },
}))

