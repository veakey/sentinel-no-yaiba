import { create } from 'zustand'
import { providersApi, type Provider, type ProviderCreateRequest, type ProviderUpdateRequest } from '@/services/api'

interface ProvidersState {
  providers: Provider[]
  isLoading: boolean
  error: string | null
  fetchProviders: () => Promise<void>
  createProvider: (data: ProviderCreateRequest) => Promise<Provider>
  updateProvider: (guid: string, data: ProviderUpdateRequest) => Promise<Provider>
  deleteProvider: (guid: string) => Promise<void>
}

export const useProvidersStore = create<ProvidersState>((set) => ({
  providers: [],
  isLoading: false,
  error: null,

  fetchProviders: async () => {
    set({ isLoading: true, error: null })
    try {
      const providers = await providersApi.getProviders()
      set({ providers, isLoading: false })
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || error.message || 'Failed to fetch providers',
        isLoading: false,
      })
    }
  },

  createProvider: async (data: ProviderCreateRequest) => {
    set({ isLoading: true, error: null })
    try {
      const provider = await providersApi.createProvider(data)
      set((state) => ({
        providers: [...state.providers, provider],
        isLoading: false,
      }))
      return provider
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to create provider'
      set({ error: errorMessage, isLoading: false })
      throw error
    }
  },

  updateProvider: async (guid: string, data: ProviderUpdateRequest) => {
    set({ isLoading: true, error: null })
    try {
      const updated = await providersApi.updateProvider(guid, data)
      set((state) => ({
        providers: state.providers.map((p) => (p.guid === guid ? updated : p)),
        isLoading: false,
      }))
      return updated
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to update provider'
      set({ error: errorMessage, isLoading: false })
      throw error
    }
  },

  deleteProvider: async (guid: string) => {
    set({ isLoading: true, error: null })
    try {
      await providersApi.deleteProvider(guid)
      set((state) => ({
        providers: state.providers.filter((p) => p.guid !== guid),
        isLoading: false,
      }))
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to delete provider'
      set({ error: errorMessage, isLoading: false })
      throw error
    }
  },
}))

