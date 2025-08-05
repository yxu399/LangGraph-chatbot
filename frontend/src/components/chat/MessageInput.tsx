import { useState, useRef, useEffect } from 'react'
import { Send, Paperclip, Mic, Square, Loader2 } from 'lucide-react'
import { cn } from '@/lib/utils'

interface MessageInputProps {
  onSendMessage: (content: string) => void
  disabled?: boolean
  isLoading?: boolean
  placeholder?: string
}

export function MessageInput({ 
  onSendMessage, 
  disabled = false, 
  isLoading = false,
  placeholder = "Type your message..." 
}: MessageInputProps) {
  const [input, setInput] = useState('')
  const [isRecording, setIsRecording] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Auto-resize textarea
  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current
    if (textarea) {
      textarea.style.height = 'auto'
      textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px'
    }
  }

  useEffect(() => {
    adjustTextareaHeight()
  }, [input])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!input.trim() || disabled || isLoading) return
    
    onSendMessage(input.trim())
    setInput('')
    
    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleVoiceToggle = () => {
    setIsRecording(!isRecording)
    // Voice recording logic would go here
  }

  const canSend = input.trim().length > 0 && !disabled && !isLoading

  return (
    <div className="border-t border-gray-200 bg-white">
      <div className="max-w-4xl mx-auto p-4">
        <form onSubmit={handleSubmit} className="relative">
          <div className="flex items-end gap-3">
            {/* Attachment Button */}
            <button
              type="button"
              className="flex-shrink-0 p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              disabled={disabled}
              title="Attach file"
            >
              <Paperclip className="h-5 w-5" />
            </button>

            {/* Input Container */}
            <div className="flex-1 relative">
              <div className={cn(
                "relative border border-gray-300 rounded-xl bg-white shadow-sm transition-all duration-200",
                "focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-500/20",
                disabled && "opacity-50 cursor-not-allowed"
              )}>
                <textarea
                  ref={textareaRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder={placeholder}
                  disabled={disabled}
                  className={cn(
                    "w-full resize-none border-0 bg-transparent px-4 py-3 text-gray-900 placeholder-gray-500",
                    "focus:outline-none focus:ring-0 min-h-[44px] max-h-[120px]",
                    "text-sm leading-6"
                  )}
                  rows={1}
                />

                {/* Character Counter (optional) */}
                {input.length > 200 && (
                  <div className="absolute bottom-2 right-2 text-xs text-gray-400">
                    {input.length}/1000
                  </div>
                )}
              </div>

              {/* Quick Actions Hint */}
              {input.length === 0 && (
                <div className="absolute bottom-1 left-4 text-xs text-gray-400 pointer-events-none">
                  Press <kbd className="px-1 py-0.5 bg-gray-100 rounded text-xs">Enter</kbd> to send, <kbd className="px-1 py-0.5 bg-gray-100 rounded text-xs">Shift + Enter</kbd> for new line
                </div>
              )}
            </div>

            {/* Voice/Send Button */}
            <div className="flex-shrink-0">
              {canSend ? (
                <button
                  type="submit"
                  disabled={!canSend}
                  className={cn(
                    "p-2 rounded-lg transition-all duration-200 transform",
                    "bg-blue-600 hover:bg-blue-700 text-white shadow-sm",
                    "hover:scale-105 active:scale-95",
                    "disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                  )}
                  title="Send message"
                >
                  {isLoading ? (
                    <Loader2 className="h-5 w-5 animate-spin" />
                  ) : (
                    <Send className="h-5 w-5" />
                  )}
                </button>
              ) : (
                <button
                  type="button"
                  onClick={handleVoiceToggle}
                  className={cn(
                    "p-2 rounded-lg transition-all duration-200",
                    isRecording
                      ? "bg-red-500 hover:bg-red-600 text-white animate-pulse"
                      : "text-gray-500 hover:text-gray-700 hover:bg-gray-100"
                  )}
                  disabled={disabled}
                  title={isRecording ? "Stop recording" : "Voice message"}
                >
                  {isRecording ? (
                    <Square className="h-5 w-5" />
                  ) : (
                    <Mic className="h-5 w-5" />
                  )}
                </button>
              )}
            </div>
          </div>

          {/* Recording Indicator */}
          {isRecording && (
            <div className="mt-2 flex items-center gap-2 text-sm text-red-600">
              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
              Recording... Click to stop
            </div>
          )}

          {/* Loading State */}
          {isLoading && (
            <div className="mt-2 flex items-center gap-2 text-sm text-gray-500">
              <Loader2 className="h-4 w-4 animate-spin" />
              AI is thinking...
            </div>
          )}
        </form>

        {/* Quick Suggestions (when empty) */}
        {input.length === 0 && !disabled && (
          <div className="mt-3 flex gap-2 flex-wrap">
            <button
              onClick={() => setInput("I'm feeling stressed about work. Can you help?")}
              className="px-3 py-1.5 text-xs bg-pink-50 text-pink-700 rounded-full hover:bg-pink-100 transition-colors"
            >
              💝 Emotional support
            </button>
            <button
              onClick={() => setInput("Explain how machine learning works")}
              className="px-3 py-1.5 text-xs bg-blue-50 text-blue-700 rounded-full hover:bg-blue-100 transition-colors"
            >
              🧠 Technical question
            </button>
            <button
              onClick={() => setInput("Help me solve this problem step by step")}
              className="px-3 py-1.5 text-xs bg-green-50 text-green-700 rounded-full hover:bg-green-100 transition-colors"
            >
              ⚡ Problem solving
            </button>
          </div>
        )}
      </div>
    </div>
  )
}