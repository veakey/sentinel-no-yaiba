import { useEffect, useRef } from 'react'
import { wsClient } from '@/services/websocket'
import { useThreatsStore } from '@/store/threatsStore'

export function useWebSocket() {
  const { fetchThreats } = useThreatsStore()
  const isConnectedRef = useRef(false)

  useEffect(() => {
    if (isConnectedRef.current) {
      return
    }

    wsClient.connect({
      onConnect: () => {
        isConnectedRef.current = true
        console.log('WebSocket connected')
      },
      onDisconnect: () => {
        isConnectedRef.current = false
        console.log('WebSocket disconnected')
      },
      onThreatsUpdate: (data) => {
        console.log('Threats updated via WebSocket:', data)
        // Refresh threats when update is received
        fetchThreats(false)
      },
      onError: (error) => {
        console.error('WebSocket error:', error)
      },
    })

    return () => {
      wsClient.disconnect()
      isConnectedRef.current = false
    }
  }, [fetchThreats])

  return {
    isConnected: wsClient.isConnected(),
  }
}

