import { Bot, User } from 'lucide-react'
import type { ChatMessage } from '../types/chat'

interface Props {
  message: ChatMessage
}

export function ChatMessageBubble({ message }: Props) {
  const isUser = message.sender === 'user'

  return (
    <div className={`flex gap-2.5 mb-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        isUser ? 'bg-bot-green-500 text-white' : 'bg-gray-200 text-gray-600'
      }`}>
        {isUser ? <User size={16} /> : <Bot size={16} />}
      </div>
      <div className={`max-w-[75%] ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`px-4 py-2.5 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${
          isUser
            ? 'bg-bot-green-500 text-white rounded-br-sm'
            : 'bg-white text-gray-800 rounded-bl-sm shadow-sm border border-gray-100'
        }`}>
          {message.text}
        </div>
        {!isUser && message.source && message.source !== 'system' && message.source !== 'error' && (
          <span className="text-[10px] text-gray-400 mt-1 ml-1 block">
            Source: {message.source}
          </span>
        )}
      </div>
    </div>
  )
}
