import axios from 'axios'
import type { ChatResponse, TokenResponse } from '../types/chat'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
})

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export async function login(username: string, password: string): Promise<TokenResponse> {
  const response = await api.post('/api/auth/token/', { username, password })
  const { access, refresh } = response.data
  localStorage.setItem('access_token', access)
  localStorage.setItem('refresh_token', refresh)
  return { access, refresh }
}

export async function sendQuery(query: string): Promise<ChatResponse> {
  const response = await api.post('/api/chat/', { query })
  return response.data
}

export function logout(): void {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

export function isAuthenticated(): boolean {
  return !!localStorage.getItem('access_token')
}
