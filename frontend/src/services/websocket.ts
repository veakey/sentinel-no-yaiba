type WebSocketMessage = {
  type: string
  data: any
}

type WebSocketCallbacks = {
  onThreatsUpdate?: (data: any) => void
  onError?: (error: Event) => void
  onConnect?: () => void
  onDisconnect?: () => void
}

class WebSocketClient {
  private ws: WebSocket | null = null
  private url: string
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 3000
  private callbacks: WebSocketCallbacks = {}
  private isConnecting = false

  constructor(url: string = 'ws://localhost:8000/ws') {
    this.url = url
  }

  connect(callbacks: WebSocketCallbacks = {}) {
    if (this.isConnecting || (this.ws && this.ws.readyState === WebSocket.OPEN)) {
      return
    }

    this.callbacks = callbacks
    this.isConnecting = true

    try {
      this.ws = new WebSocket(this.url)

      this.ws.onopen = () => {
        this.isConnecting = false
        this.reconnectAttempts = 0
        this.callbacks.onConnect?.()
      }

      this.ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          this.handleMessage(message)
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }

      this.ws.onerror = (error) => {
        this.isConnecting = false
        this.callbacks.onError?.(error)
      }

      this.ws.onclose = () => {
        this.isConnecting = false
        this.callbacks.onDisconnect?.()
        this.attemptReconnect()
      }
    } catch (error) {
      this.isConnecting = false
      console.error('WebSocket connection error:', error)
    }
  }

  private handleMessage(message: WebSocketMessage) {
    switch (message.type) {
      case 'threats_updated':
        this.callbacks.onThreatsUpdate?.(message.data)
        break
      default:
        console.log('Unknown message type:', message.type)
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached')
      return
    }

    this.reconnectAttempts++
    setTimeout(() => {
      this.connect(this.callbacks)
    }, this.reconnectDelay * this.reconnectAttempts)
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
    this.callbacks = {}
  }

  send(message: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message))
    } else {
      console.warn('WebSocket is not connected')
    }
  }

  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN
  }
}

export const wsClient = new WebSocketClient()

