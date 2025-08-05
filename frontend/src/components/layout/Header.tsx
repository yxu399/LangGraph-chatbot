import { MessageCircle, Menu, Settings, LogOut } from 'lucide-react'
import { useUser, useClerk } from '@clerk/clerk-react'
import { cn } from '@/lib/utils'

interface HeaderProps {
  onToggleSidebar: () => void
  isSidebarOpen: boolean
}

export function Header({ onToggleSidebar, isSidebarOpen }: HeaderProps) {
  const { user } = useUser()
  const { signOut } = useClerk()

  return (
    <header className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
      {/* Left side - Logo and menu toggle */}
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleSidebar}
          className="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <Menu className="h-5 w-5" />
        </button>
        
        <div className="flex items-center gap-2">
          <div className="bg-blue-600 p-2 rounded-lg">
            <MessageCircle className="h-5 w-5 text-white" />
          </div>
          <div className="hidden sm:block">
            <h1 className="font-semibold text-gray-900">LangGraph Chat</h1>
            <p className="text-xs text-gray-500">Intelligent AI Assistant</p>
          </div>
        </div>
      </div>

      {/* Right side - User menu */}
      <div className="flex items-center gap-2">
        <button className="p-2 rounded-lg hover:bg-gray-100 transition-colors">
          <Settings className="h-5 w-5 text-gray-600" />
        </button>
        
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-100 transition-colors">
            {user?.imageUrl ? (
              <img 
                src={user.imageUrl} 
                alt={user.firstName || 'User'} 
                className="h-6 w-6 rounded-full"
              />
            ) : (
              <div className="bg-blue-100 p-1.5 rounded-full">
                <span className="text-xs font-medium text-blue-600">
                  {user?.firstName?.[0] || user?.emailAddresses[0]?.emailAddress[0] || 'U'}
                </span>
              </div>
            )}
            <span className="hidden sm:block text-sm font-medium text-gray-700">
              {user?.firstName || user?.emailAddresses[0]?.emailAddress.split('@')[0] || 'User'}
            </span>
          </button>
          
          <button 
            onClick={() => signOut()}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            title="Sign out"
          >
            <LogOut className="h-4 w-4 text-gray-600" />
          </button>
        </div>
      </div>
    </header>
  )
}