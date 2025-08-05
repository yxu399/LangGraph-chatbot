import { useUser } from '@clerk/clerk-react'
import { Layout } from '@/components/layout/Layout'
import { ChatPlaceholder } from '@/components/chat/ChatPlaceholder'
import { AuthPage } from '@/components/auth/AuthPage'

function App() {
  const { isSignedIn, isLoaded } = useUser()

  // Show loading spinner while Clerk loads
  if (!isLoaded) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  // Show auth page if user is not signed in
  if (!isSignedIn) {
    return <AuthPage />
  }

  // Show main app if user is signed in
  return (
    <Layout>
      <ChatPlaceholder />
    </Layout>
  )
}

export default App