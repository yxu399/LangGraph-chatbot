import { Brain, Heart, User, Copy, RotateCcw, Check, Clock, AlertCircle } from 'lucide-react'
import { useState } from 'react'
import { cn } from '@/lib/utils'
import { formatTime } from '@/lib/utils'

// Define the interface directly in this file to avoid import issues
interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  status?: 'sending' | 'sent' | 'error' | 'received';
  messageType?: 'emotional' | 'logical';
  agentUsed?: 'therapist' | 'logical';
}

interface MessageProps {
  message: ChatMessage
  isLatest?: boolean
}

export function Message({ message, isLatest }: MessageProps) {
  const [copied, setCopied] = useState(false)
  const isUser = message.role === 'user'
  const isAssistant = message.role === 'assistant'

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const getAgentIcon = () => {
    if (message.agentUsed === 'therapist') {
      return <Heart className="h-4 w-4 text-pink-600" />
    }
    if (message.agentUsed === 'logical') {
      return <Brain className="h-4 w-4 text-blue-600" />
    }
    return null
  }

  const getAgentBadge = () => {
    if (!message.agentUsed) return null
    
    return (
      <div className={cn(
        "inline-flex items-center gap-1.5 px-2 py-1 rounded-full text-xs font-medium mb-2",
        message.agentUsed === 'therapist' 
          ? "bg-pink-100 text-pink-700" 
          : "bg-blue-100 text-blue-700"
      )}>
        {getAgentIcon()}
        <span>{message.agentUsed === 'therapist' ? 'Emotional' : 'Logical'} Mode</span>
      </div>
    )
  }

  const getStatusIcon = () => {
    switch (message.status) {
      case 'sending':
        return <Clock className="h-3 w-3 text-gray-400 animate-spin" />
      case 'sent':
      case 'received':
        return <Check className="h-3 w-3 text-green-500" />
      case 'error':
        return <AlertCircle className="h-3 w-3 text-red-500" />
      default:
        return null
    }
  }

  return (
    <div className={cn(
      "group flex gap-3 max-w-4xl mx-auto px-4 py-4 hover:bg-gray-50/50 transition-colors",
      isUser ? "flex-row-reverse" : "flex-row"
    )}>
      {/* Avatar */}
      <div className={cn(
        "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
        isUser 
          ? "bg-blue-600 text-white" 
          : message.agentUsed === 'therapist'
            ? "bg-pink-100 text-pink-600"
            : "bg-blue-100 text-blue-600"
      )}>
        {isUser ? (
          <User className="h-4 w-4" />
        ) : (
          getAgentIcon() || <Brain className="h-4 w-4" />
        )}
      </div>

      {/* Message Content */}
      <div className={cn(
        "flex-1 min-w-0",
        isUser ? "text-right" : "text-left"
      )}>
        {/* Agent Badge (only for assistant messages) */}
        {isAssistant && (
          <div className={cn(isUser ? "text-right" : "text-left")}>
            {getAgentBadge()}
          </div>
        )}

        {/* Message Bubble */}
        <div className={cn(
          "inline-block max-w-[80%] px-4 py-3 rounded-2xl shadow-sm",
          isUser
            ? "bg-blue-600 text-white ml-auto"
            : "bg-white text-gray-900 border border-gray-200"
        )}>
          <div className="prose prose-sm max-w-none">
            <p className={cn(
              "whitespace-pre-wrap break-words m-0",
              isUser ? "text-white" : "text-gray-900"
            )}>
              {message.content}
            </p>
          </div>
        </div>

        {/* Message Footer */}
        <div className={cn(
          "flex items-center gap-2 mt-1 text-xs text-gray-500",
          isUser ? "justify-end" : "justify-start"
        )}>
          <span>{formatTime(message.timestamp)}</span>
          {getStatusIcon()}
          
          {/* Action Buttons (show on hover) */}
          <div className="opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1 ml-2">
            <button
              onClick={handleCopy}
              className="p-1 rounded hover:bg-gray-200 transition-colors"
              title="Copy message"
            >
              {copied ? (
                <Check className="h-3 w-3 text-green-600" />
              ) : (
                <Copy className="h-3 w-3 text-gray-500" />
              )}
            </button>
            
            {isAssistant && (
              <button
                className="p-1 rounded hover:bg-gray-200 transition-colors"
                title="Regenerate response"
              >
                <RotateCcw className="h-3 w-3 text-gray-500" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}