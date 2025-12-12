import { create } from 'zustand'
import type { Threat, ThreatsResponse } from '@/types'
import { threatsApi } from '@/services/api'
import { mockThreatsResponse } from '@/services/mockData'

interface ThreatsState {
  threats: Threat[]
  threatsByProvider: ThreatsResponse
  isLoading: boolean
  error: string | null
  lastUpdate: Date | null
  fetchThreats: (forceRefresh?: boolean) => Promise<void>
  getThreatsBySeverity: (severity: Threat['severity']) => Threat[]
  getThreatsByStatus: (status: Threat['status']) => Threat[]
  getThreatsByProvider: (provider: string) => Threat[]
}

export const useThreatsStore = create<ThreatsState>((set, get) => ({
  threats: [],
  threatsByProvider: {},
  isLoading: false,
  error: null,
  lastUpdate: null,

  fetchThreats: async (forceRefresh = false) => {
    set({ isLoading: true, error: null })
    try {
      // Try real API first, fallback to mock
      try {
        const data = await threatsApi.getThreats({ force_refresh: forceRefresh })
        const allThreats: Threat[] = []
        Object.values(data).forEach((providerData) => {
          if (providerData.threats) {
            allThreats.push(...providerData.threats)
          }
        })
        set({
          threats: allThreats,
          threatsByProvider: data,
          lastUpdate: new Date(),
          isLoading: false,
        })
      } catch {
        // Use mock data
        const allThreats: Threat[] = []
        Object.values(mockThreatsResponse).forEach((providerData) => {
          if (providerData.threats) {
            allThreats.push(...providerData.threats)
          }
        })
        set({
          threats: allThreats,
          threatsByProvider: mockThreatsResponse,
          lastUpdate: new Date(),
          isLoading: false,
        })
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch threats',
        isLoading: false,
      })
    }
  },

  getThreatsBySeverity: (severity) => {
    return get().threats.filter((t) => t.severity === severity)
  },

  getThreatsByStatus: (status) => {
    return get().threats.filter((t) => t.status === status)
  },

  getThreatsByProvider: (provider) => {
    return get().threats.filter((t) => t.provider === provider)
  },
}))

