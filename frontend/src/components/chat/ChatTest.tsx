import { useState } from 'react'
import { MessageList } from './MessageList'
import { MessageInput } from './MessageInput'
import { generateId } from '@/lib/utils'

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

// Mock messages for testing
const mockMessages: ChatMessage[] = [
  {
    id: generateId(),
    role: 'user',
    content: 'Hello! I\'m feeling a bit stressed about work lately. Can you help me?',
    timestamp: new Date(Date.now() - 300000), // 5 minutes ago
    status: 'sent'
  },
  {
    id: generateId(),
    role: 'assistant',
    content: 'I understand that work stress can be really overwhelming. It\'s completely normal to feel this way, and I\'m here to help you work through it. Can you tell me what specific aspects of work are causing you the most stress right now?',
    timestamp: new Date(Date.now() - 240000), // 4 minutes ago
    status: 'received',
    messageType: 'emotional',
    agentUsed: 'therapist'
  },
  {
    id: generateId(),
    role: 'user',
    content: 'Thanks for understanding. It\'s mainly the tight deadlines and feeling like I\'m always behind. Also, how does machine learning actually work?',
    timestamp: new Date(Date.now() - 180000), // 3 minutes ago
    status: 'sent'
  },
  {
    id: generateId(),
    role: 'assistant',
    content: 'Machine learning works by training algorithms on data to recognize patterns and make predictions. The process involves feeding large amounts of data to mathematical models, which then learn to identify relationships and make decisions based on new, unseen data. There are three main types: supervised learning (with labeled data), unsupervised learning (finding hidden patterns), and reinforcement learning (learning through trial and error).',
    timestamp: new Date(Date.now() - 120000), // 2 minutes ago
    status: 'received',
    messageType: 'logical',
    agentUsed: 'logical'
  },
  {
    id: generateId(),
    role: 'user',
    content: 'That\'s really interesting! But going back to my stress - do you have any practical tips?',
    timestamp: new Date(Date.now() - 60000), // 1 minute ago
    status: 'sent'
  }
]

export function ChatTest() {
  const [messages, setMessages] = useState<ChatMessage[]>(mockMessages)
  const [isTyping, setIsTyping] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [typingAgent, setTypingAgent] = useState<'therapist' | 'logical'>('therapist')

  const toggleTyping = () => {
    setIsTyping(!isTyping)
    setTypingAgent(isTyping ? 'therapist' : (Math.random() > 0.5 ? 'therapist' : 'logical'))
  }

  const handleSendMessage = (content: string) => {
    // Add user message immediately
    const userMessage: ChatMessage = {
      id: generateId(),
      role: 'user',
      content,
      timestamp: new Date(),
      status: 'sent'
    }
    
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)
    setIsTyping(true)

    // Simulate AI response delay
    setTimeout(() => {
      const agentType = Math.random() > 0.5 ? 'therapist' : 'logical'
      const responses = {
        therapist: [
          "I hear you, and I want you to know that what you're feeling is completely valid. Let's work through this together.",
          "It sounds like you're going through a challenging time. I'm here to support you through this.",
          "Your feelings matter, and it's okay to feel overwhelmed sometimes. Let's explore this further."
        ],
        logical: [
          "Based on your query, I can provide a systematic analysis of the situation.",
          "Let me break this down logically and provide you with structured information.",
          "Here's a factual approach to addressing your question systematically."
        ]
      }

      const aiMessage: ChatMessage = {
        id: generateId(),
        role: 'assistant',
        content: responses[agentType][Math.floor(Math.random() * responses[agentType].length)],
        timestamp: new Date(),
        status: 'received',
        messageType: agentType === 'therapist' ? 'emotional' : 'logical',
        agentUsed: agentType
      }

      setMessages(prev => [...prev, aiMessage])
      setIsLoading(false)
      setIsTyping(false)
    }, 2000 + Math.random() * 2000) // 2-4 second delay
  }

  const addMessage = (content: string, role: 'user' | 'assistant') => {
    const newMessage: ChatMessage = {
      id: generateId(),
      role,
      content,
      timestamp: new Date(),
      status: role === 'user' ? 'sent' : 'received',
      ...(role === 'assistant' && {
        messageType: Math.random() > 0.5 ? 'emotional' : 'logical',
        agentUsed: Math.random() > 0.5 ? 'therapist' : 'logical'
      })
    }
    setMessages(prev => [...prev, newMessage])
  }

  return (
    <div className="flex-1 flex flex-col bg-white">
      {/* Test Controls */}
      <div className="bg-gray-100 p-4 border-b">
        <div className="flex gap-2 flex-wrap">
          <button
            onClick={toggleTyping}
            className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700"
          >
            {isTyping ? 'Stop Typing' : 'Show Typing'}
          </button>
          <button
            onClick={() => addMessage('This is a test user message', 'user')}
            className="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700"
          >
            Add User Message
          </button>
          <button
            onClick={() => addMessage('This is a test assistant response with some helpful information.', 'assistant')}
            className="px-3 py-1 bg-purple-600 text-white rounded text-sm hover:bg-purple-700"
          >
            Add AI Message
          </button>
          <button
            onClick={() => setMessages([])}
            className="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700"
          >
            Clear Messages
          </button>
        </div>
      </div>

      {/* Message List */}
      <MessageList 
        messages={messages} 
        isTyping={isTyping}
        typingAgent={typingAgent}
      />

      {/* Message Input */}
      <MessageInput 
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
        disabled={isLoading}
      />
    </div>
  )
}