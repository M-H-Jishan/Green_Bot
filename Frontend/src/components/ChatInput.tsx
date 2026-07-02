import { useState, type KeyboardEvent } from 'react'
import { Send } from 'lucide-react'

interface Props {
  onSend: (message: string) => void
  disabled: boolean
}

export function ChatInput({ onSend, disabled }: Props) {
  const [text, setText] = useState('')

  const handleSend = () => {
    if (text.trim() && !disabled) {
      onSend(text)
      setText('')
    }
  }

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="p-3 border-t border-gray-200 bg-white flex gap-2 items-center">
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type your message..."
        disabled={disabled}
        className="flex-1 px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-full text-sm outline-none focus:border-bot-green-500 focus:bg-white transition-colors disabled:opacity-50"
      />
      <button
        onClick={handleSend}
        disabled={disabled || !text.trim()}
        className="w-10 h-10 flex-shrink-0 rounded-full bg-bot-green-500 text-white flex items-center justify-center hover:bg-bot-green-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
        aria-label="Send message"
      >
        <Send size={18} />
      </button>
    </div>
  )
}
