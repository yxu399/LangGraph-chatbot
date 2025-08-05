import { Plus, Brain, Heart, Search, MoreHorizontal } from 'lucide-react'
import { cn } from '@/lib/utils'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

// Mock conversation data for testing
const mockConversations = [
  {
    id: '1',
    title: 'How do I manage stress at work?',
    lastMessage: 'Let me help you with some strategies...',
    type: 'emotional' as const,
    updatedAt: new Date(),
  },
  {
    id: '2', 
    title: 'Explain quantum computing',
    lastMessage: 'Quantum computing uses quantum mechanics...',
    type: 'logical' as const,
    updatedAt: new Date(Date.now() - 86400000), // Yesterday
  },
  {
    id: '3',
    title: 'Career advice for developers',
    lastMessage: 'Focus on building a strong portfolio...',
    type: 'logical' as const,
    updatedAt: new Date(Date.now() - 172800000), // 2 days ago
  }
]

export function Sidebar({ isOpen, onClose }: SidebarProps) {
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <aside className={cn(
        "fixed lg:static inset-y-0 left-0 z-50 w-80 bg-white border-r border-gray-200 transform transition-transform duration-200 ease-in-out",
        isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
      )}>
        <div className="flex flex-col h-full">
          {/* New chat button */}
          <div className="p-4">
            <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg font-medium transition-colors flex items-center justify-center gap-2">
              <Plus className="h-4 w-4" />
              New Chat
            </button>
          </div>

          {/* Search */}
          <div className="px-4 pb-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search conversations..."
                className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Conversations list */}
          <div className="flex-1 overflow-y-auto">
            <div className="px-4">
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
                Recent Conversations
              </h3>
              
              <div className="space-y-1">
                {mockConversations.map((conversation) => (
                  <div
                    key={conversation.id}
                    className="w-full text-left p-3 rounded-lg hover:bg-gray-50 transition-colors group cursor-pointer"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex items-start gap-3 flex-1 min-w-0">
                        <div className={cn(
                          "flex-shrink-0 p-1.5 rounded-full",
                          conversation.type === 'emotional' 
                            ? "bg-pink-100 text-pink-600" 
                            : "bg-blue-100 text-blue-600"
                        )}>
                          {conversation.type === 'emotional' ? (
                            <Heart className="h-3 w-3" />
                          ) : (
                            <Brain className="h-3 w-3" />
                          )}
                        </div>
                        
                        <div className="flex-1 min-w-0">
                          <h4 className="text-sm font-medium text-gray-900 truncate">
                            {conversation.title}
                          </h4>
                          <p className="text-xs text-gray-500 truncate mt-0.5">
                            {conversation.lastMessage}
                          </p>
                        </div>
                      </div>
                      
                      <div className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-gray-100 transition-all">
                        <MoreHorizontal className="h-3 w-3 text-gray-400" />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="p-4 border-t border-gray-200">
            <div className="text-xs text-gray-500 text-center">
              <p>Built with LangGraph</p>
              <p className="mt-1">Intelligent AI Routing</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}