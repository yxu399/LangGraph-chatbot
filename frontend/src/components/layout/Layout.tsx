import { useState } from 'react'
import { Header } from './Header'
import { Sidebar } from './Sidebar'

interface LayoutProps {
  children: React.ReactNode
}

export function Layout({ children }: LayoutProps) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen)
  const closeSidebar = () => setIsSidebarOpen(false)

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <Header 
        onToggleSidebar={toggleSidebar}
        isSidebarOpen={isSidebarOpen}
      />
      
      <div className="flex-1 flex overflow-hidden">
        <Sidebar 
          isOpen={isSidebarOpen}
          onClose={closeSidebar}
        />
        
        <main className="flex-1 flex flex-col overflow-hidden">
          {children}
        </main>
      </div>
    </div>
  )
}