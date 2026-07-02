import { Bot, X, LogOut } from 'lucide-react'
import { ChatMessageBubble } from './ChatMessage'
import { ChatInput } from './ChatInput'
import { TypingIndicator } from './TypingIndicator'
import { useChat } from '../hooks/useChat'
import { logout, isAuthenticated } from '../api/client'

interface Props {
  onClose: () => void
}

export function ChatWidget({ onClose }: Props) {
  const { messages, isTyping, sendMessage, scrollRef } = useChat()

  const handleLogout = () => {
    logout()
    window.location.reload()
  }

  return (
    <div className="fixed bottom-20 right-4 w-[calc(100vw-2rem)] sm:w-96 h-[600px] max-h-[calc(100vh-6rem)] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden chat-slide-up z-50">
      {/* Header */}
      <div className="bg-bot-green-500 text-white px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
            <Bot size={20} />
          </div>
          <div>
            <h3 className="font-semibold text-sm">Green Bot</h3>
            <span className="text-xs opacity-90">● Online</span>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {isAuthenticated() && (
            <button onClick={handleLogout} className="text-white/80 hover:text-white p-1" aria-label="Logout">
              <LogOut size={18} />
            </button>
          )}
          <button onClick={onClose} className="text-white/80 hover:text-white p-1" aria-label="Close chat">
            <X size={20} />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 bg-gray-50">
        {messages.map((msg) => (
          <ChatMessageBubble key={msg.id} message={msg} />
        ))}
        {isTyping && <TypingIndicator />}
      </div>

      {/* Input */}
      <ChatInput onSend={sendMessage} disabled={isTyping} />
    </div>
  )
}
