import { create } from 'zustand'
import { malwarebytesApi } from '@/services/api'

interface DetectionSummary {
  threats: any[]
  groups: any[]
  endpoints: any[]
  summary: {
    total: number
    critical: number
    high: number
    medium: number
    low: number
  }
}

interface DetectionState {
  data: DetectionSummary | null
  isLoading: boolean
  error: string | null
  fetchDetectionSummary: () => Promise<void>
}

export const useDetectionStore = create<DetectionState>((set) => ({
  data: null,
  isLoading: false,
  error: null,

  fetchDetectionSummary: async () => {
    set({ isLoading: true, error: null })
    try {
      const data = await malwarebytesApi.getDetectionSummary()
      set({ data, isLoading: false })
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || error.message || 'Failed to fetch detection summary',
        isLoading: false,
      })
    }
  },
}))

