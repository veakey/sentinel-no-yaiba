import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import type { User } from '@/types'
import { authApi } from '@/services/api'
import { mockUsers } from '@/services/mockData'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => void
  checkAuth: () => Promise<void>
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (username: string, password: string) => {
        set({ isLoading: true })
        try {
          // Try real API first, fallback to mock
          try {
            const tokens = await authApi.login({ username, password })
            localStorage.setItem('access_token', tokens.access_token)
            localStorage.setItem('refresh_token', tokens.refresh_token)
            const user = await authApi.getCurrentUser()
            set({ user, isAuthenticated: true, isLoading: false })
          } catch {
            // Mock authentication for development
            const mockUser = mockUsers.find((u) => u.username === username)
            if (mockUser && password === 'password') {
              localStorage.setItem('access_token', 'mock-access-token')
              localStorage.setItem('refresh_token', 'mock-refresh-token')
              set({ user: mockUser, isAuthenticated: true, isLoading: false })
            } else {
              throw new Error('Invalid credentials')
            }
          }
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      logout: () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        set({ user: null, isAuthenticated: false })
      },

      checkAuth: async () => {
        set({ isLoading: true })
        const token = localStorage.getItem('access_token')
        if (!token) {
          set({ user: null, isAuthenticated: false, isLoading: false })
          return
        }

        try {
          const user = await authApi.getCurrentUser()
          set({ user, isAuthenticated: true, isLoading: false })
        } catch (error) {
          // If token is invalid, clear it and logout
          console.error('Auth check failed:', error)
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          set({ user: null, isAuthenticated: false, isLoading: false })
        }
      },
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ user: state.user, isAuthenticated: state.isAuthenticated }),
    }
  )
)

