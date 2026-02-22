import { ref, onMounted, onUnmounted } from 'vue'
import type { Ref } from 'vue'

interface WebSocketMessage {
  type: 'booking' | 'availability' | 'price_change' | 'notification'
  data: any
  timestamp: string
}

export function useRealtime(
  wsUrl: string = 'ws://localhost:8000/ws'
) {
  const isConnected: Ref<boolean> = ref(false)
  const lastMessage: Ref<WebSocketMessage | null> = ref(null)
  const error: Ref<string | null> = ref(null)
  
  let ws: WebSocket | null = null
  let reconnectAttempts = 0
  let reconnectTimeout: number | null = null
  const maxReconnectAttempts = 5

  const connect = () => {
    if (ws?.readyState === WebSocket.OPEN) return

    try {
      ws = new WebSocket(wsUrl)

      ws.onopen = () => {
        isConnected.value = true
        error.value = null
        reconnectAttempts = 0
        console.log('WebSocket connected')
      }

      ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          lastMessage.value = message
        } catch (err) {
          console.error('Failed to parse WebSocket message:', err)
        }
      }

      ws.onerror = (err) => {
        error.value = 'WebSocket error occurred'
        console.error('WebSocket error:', err)
      }

      ws.onclose = () => {
        isConnected.value = false
        console.log('WebSocket disconnected')
        
        // Attempt reconnection
        if (reconnectAttempts < maxReconnectAttempts) {
          reconnectAttempts++
          const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000)
          console.log(`Reconnecting in ${delay}ms (attempt ${reconnectAttempts})`)
          
          reconnectTimeout = window.setTimeout(() => {
            connect()
          }, delay)
        }
      }
    } catch (err) {
      error.value = 'Failed to create WebSocket connection'
      console.error('WebSocket creation error:', err)
    }
  }

  const disconnect = () => {
    if (reconnectTimeout) {
      clearTimeout(reconnectTimeout)
      reconnectTimeout = null
    }
    
    if (ws) {
      ws.close()
      ws = null
    }
    isConnected.value = false
  }

  const send = (message: any): boolean => {
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message))
      return true
    }
    return false
  }

  const subscribe = (channel: string) => {
    send({ type: 'subscribe', channel })
  }

  const unsubscribe = (channel: string) => {
    send({ type: 'unsubscribe', channel })
  }

  onMounted(() => {
    connect()
  })

  onUnmounted(() => {
    disconnect()
  })

  return {
    isConnected,
    lastMessage,
    error,
    connect,
    disconnect,
    send,
    subscribe,
    unsubscribe
  }
}
