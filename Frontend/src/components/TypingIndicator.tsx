export function TypingIndicator() {
  return (
    <div className="flex gap-2.5 mb-3 flex-row">
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 text-gray-600 flex items-center justify-center">
        <span className="text-sm">🤖</span>
      </div>
      <div className="bg-white rounded-2xl rounded-bl-sm shadow-sm border border-gray-100 px-4 py-3">
        <div className="flex gap-1.5">
          <span className="typing-dot w-2 h-2 bg-gray-400 rounded-full" />
          <span className="typing-dot w-2 h-2 bg-gray-400 rounded-full" />
          <span className="typing-dot w-2 h-2 bg-gray-400 rounded-full" />
        </div>
      </div>
    </div>
  )
}
