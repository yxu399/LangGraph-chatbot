import { useEffect, useRef } from 'react'
import { Message } from './Message'

// Define the interface directly to avoid import issues
interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  status?: 'sending' | 'sent' | 'error' | 'received';
  messageType?: 'emotional' | 'logical';
  agentUsed?: 'therapist' | 'logical';
}

interface MessageListProps {
  messages: ChatMessage[]
  isTyping?: boolean
  typingAgent?: 'therapist' | 'logical'
}

function TypingIndicator({ agent }: { agent?: 'therapist' | 'logical' }) {
  return (
    <div className="flex gap-3 max-w-4xl mx-auto px-4 py-4">
      {/* Avatar */}
      <div className={`
        flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center
        ${agent === 'therapist' ? 'bg-pink-100 text-pink-600' : 'bg-blue-100 text-blue-600'}
      `}>
        {agent === 'therapist' ? '💝' : '🧠'}
      </div>

      {/* Typing Animation */}
      <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3 shadow-sm">
        <div className="flex items-center gap-1">
          <div className="flex gap-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
          </div>
          <span className="text-xs text-gray-500 ml-2">
            {agent === 'therapist' ? 'Emotional' : 'Logical'} assistant is thinking...
          </span>
        </div>
      </div>
    </div>
  )
}

export function MessageList({ messages, isTyping, typingAgent }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isTyping])

  if (messages.length === 0 && !isTyping) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center max-w-md">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            💬
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Start a conversation
          </h3>
          <p className="text-gray-600">
            Send a message and let our intelligent AI routing system determine 
            the best response approach for you.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div 
      ref={containerRef}
      className="flex-1 overflow-y-auto bg-gray-50"
    >
      <div className="min-h-full py-4">
        {messages.map((message, index) => (
          <Message
            key={message.id}
            message={message}
            isLatest={index === messages.length - 1}
          />
        ))}
        
        {isTyping && (
          <TypingIndicator agent={typingAgent} />
        )}
        
        <div ref={messagesEndRef} />
      </div>
    </div>
  )
}