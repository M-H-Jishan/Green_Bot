export interface ChatMessage {
  id: string
  text: string
  sender: 'user' | 'bot'
  source?: string
  timestamp: number
}

export interface ChatResponse {
  response: string
  source: string
  source_url: string | null
  success: boolean
  error_message: string | null
}

export interface TokenResponse {
  access: string
  refresh: string
}
