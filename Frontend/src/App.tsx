import { useState, useEffect } from 'react'
import { MessageCircle } from 'lucide-react'
import { ChatWidget } from './components/ChatWidget'
import { LoginScreen } from './components/LoginScreen'
import { isAuthenticated } from './api/client'

export default function App() {
  const [chatOpen, setChatOpen] = useState(false)
  const [authed, setAuthed] = useState(isAuthenticated())

  useEffect(() => {
    setAuthed(isAuthenticated())
  }, [])

  if (!authed) {
    return <LoginScreen onLogin={() => setAuthed(true)} />
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-bot-green-50 to-gray-100">
      {/* Landing page content */}
      <div className="container mx-auto px-4 py-16 text-center">
        <div className="w-20 h-20 bg-bot-green-500 rounded-3xl flex items-center justify-center mx-auto mb-6">
          <span className="text-4xl">🤖</span>
        </div>
        <h1 className="text-4xl font-bold text-gray-800 mb-3">Green Bot</h1>
        <p className="text-gray-500 max-w-md mx-auto mb-8">
          Your AI-powered assistant. Click the chat button below to start a conversation.
        </p>
        <button
          onClick={() => setChatOpen(true)}
          className="inline-flex items-center gap-2 bg-bot-green-500 text-white px-6 py-3 rounded-full font-medium hover:bg-bot-green-600 transition-colors"
        >
          <MessageCircle size={20} />
          Start Chatting
        </button>
      </div>

      {/* Floating chat button */}
      {!chatOpen && (
        <button
          onClick={() => setChatOpen(true)}
          className="fixed bottom-4 right-4 w-14 h-14 bg-bot-green-500 text-white rounded-full shadow-lg flex items-center justify-center hover:bg-bot-green-600 transition-all hover:scale-110 z-50"
          aria-label="Open chat"
        >
          <MessageCircle size={24} />
        </button>
      )}

      {/* Chat widget */}
      {chatOpen && <ChatWidget onClose={() => setChatOpen(false)} />}
    </div>
  )
}
