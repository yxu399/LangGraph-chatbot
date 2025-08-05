import { SignIn, SignUp, useUser } from '@clerk/clerk-react'
import { useState } from 'react'
import { MessageCircle, Brain, Heart, Zap, Shield, Users, Sparkles } from 'lucide-react'

export function AuthPage() {
  const [isSignUp, setIsSignUp] = useState(false)
  const { isLoaded } = useUser()

  if (!isLoaded) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex">
      {/* Left side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 xl:w-2/3 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-800"></div>
        <div className="absolute inset-0 bg-black opacity-10"></div>
        
        <div className="relative z-10 flex flex-col justify-center px-12 xl:px-20 text-white">
          <div className="flex items-center gap-3 mb-8">
            <div className="bg-white bg-opacity-20 p-3 rounded-2xl backdrop-blur-sm">
              <MessageCircle className="h-8 w-8" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">LangGraph Chat</h1>
              <p className="text-blue-100">Intelligent AI Assistant</p>
            </div>
          </div>

          <div className="space-y-6 mb-12">
            <h2 className="text-4xl xl:text-5xl font-bold leading-tight">
              The Future of
              <br />
              <span className="bg-gradient-to-r from-yellow-400 to-pink-400 bg-clip-text text-transparent">
                Intelligent Chat
              </span>
            </h2>
            <p className="text-xl text-blue-100 leading-relaxed">
              Experience AI that understands context and emotion, 
              automatically routing your conversations to specialized agents 
              for the most relevant and helpful responses.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-6">
            <div className="flex items-center gap-4">
              <div className="bg-white bg-opacity-20 p-3 rounded-xl backdrop-blur-sm">
                <Brain className="h-6 w-6" />
              </div>
              <div>
                <h3 className="font-semibold text-lg">Smart Logical Reasoning</h3>
                <p className="text-blue-100">Get precise, analytical answers for technical questions</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="bg-white bg-opacity-20 p-3 rounded-xl backdrop-blur-sm">
                <Heart className="h-6 w-6" />
              </div>
              <div>
                <h3 className="font-semibold text-lg">Emotional Intelligence</h3>
                <p className="text-blue-100">Receive empathetic support for personal matters</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="bg-white bg-opacity-20 p-3 rounded-xl backdrop-blur-sm">
                <Zap className="h-6 w-6" />
              </div>
              <div>
                <h3 className="font-semibold text-lg">Automatic Routing</h3>
                <p className="text-blue-100">AI determines the best response approach instantly</p>
              </div>
            </div>
          </div>

          <div className="mt-12 flex items-center gap-8 text-sm text-blue-200">
            <div className="flex items-center gap-2">
              <Shield className="h-4 w-4" />
              <span>Secure & Private</span>
            </div>
            <div className="flex items-center gap-2">
              <Users className="h-4 w-4" />
              <span>1000+ Users</span>
            </div>
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4" />
              <span>Advanced AI</span>
            </div>
          </div>
        </div>
      </div>

      {/* Right side - Authentication */}
      <div className="w-full lg:w-1/2 xl:w-1/3 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <div className="text-center mb-8">
              <div className="flex justify-center mb-4 lg:hidden">
                <div className="bg-blue-600 p-3 rounded-2xl">
                  <MessageCircle className="h-8 w-8 text-white" />
                </div>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                {isSignUp ? 'Create your account' : 'Welcome back'}
              </h2>
              <p className="text-gray-600">
                {isSignUp 
                  ? 'Start your intelligent chat experience' 
                  : 'Sign in to continue your conversations'
                }
              </p>
            </div>

            <div className="flex flex-col items-center">
              {isSignUp ? (
                <SignUp 
                  appearance={{
                    elements: {
                      formButtonPrimary: 'bg-blue-600 hover:bg-blue-700 text-sm',
                      card: 'shadow-none',
                    }
                  }}
                />
              ) : (
                <SignIn 
                  appearance={{
                    elements: {
                      formButtonPrimary: 'bg-blue-600 hover:bg-blue-700 text-sm',
                      card: 'shadow-none',
                    }
                  }}
                />
              )}
            </div>

            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                {isSignUp ? 'Already have an account?' : "Don't have an account?"}{' '}
                <button
                  onClick={() => setIsSignUp(!isSignUp)}
                  className="text-blue-600 hover:text-blue-700 font-medium"
                >
                  {isSignUp ? 'Sign in' : 'Sign up'}
                </button>
              </p>
            </div>
          </div>

          <div className="mt-8 text-center text-xs text-gray-500">
            <p>By continuing, you agree to our Terms of Service and Privacy Policy</p>
          </div>
        </div>
      </div>
    </div>
  )
}