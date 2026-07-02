import { useState, useCallback, useRef, useEffect } from 'react'
import type { ChatMessage } from '../types/chat'
import { sendQuery } from '../api/client'

const generateId = () => `${Date.now()}-${Math.random().toString(36).slice(2)}`

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      text: "Hello! I'm Green Bot. How can I help you today?",
      sender: 'bot',
      source: 'system',
      timestamp: Date.now(),
    },
  ])
  const [isTyping, setIsTyping] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const scrollRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = useCallback(() => {
    requestAnimationFrame(() => {
      if (scrollRef.current) {
        scrollRef.current.scrollTop = scrollRef.current.scrollHeight
      }
    })
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages, isTyping, scrollToBottom])

  const sendMessage = useCallback(async (text: string) => {
    if (!text.trim() || isTyping) return

    setError(null)

    const userMsg: ChatMessage = {
      id: generateId(),
      text: text.trim(),
      sender: 'user',
      timestamp: Date.now(),
    }
    setMessages((prev) => [...prev, userMsg])
    setIsTyping(true)

    try {
      const result = await sendQuery(text.trim())
      const botMsg: ChatMessage = {
        id: generateId(),
        text: result.response,
        sender: 'bot',
        source: result.source,
        timestamp: Date.now(),
      }
      setMessages((prev) => [...prev, botMsg])
    } catch (err: unknown) {
      const errorMsg: ChatMessage = {
        id: generateId(),
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        source: 'error',
        timestamp: Date.now(),
      }
      setMessages((prev) => [...prev, errorMsg])
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setIsTyping(false)
    }
  }, [isTyping])

  return { messages, isTyping, error, sendMessage, scrollRef }
}
