import { MessageCircle, Brain, Heart, Zap } from 'lucide-react'

export function ChatPlaceholder() {
  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-md text-center space-y-6">
        <div className="flex justify-center">
          <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-4 rounded-2xl">
            <MessageCircle className="h-12 w-12 text-white" />
          </div>
        </div>
        
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Welcome to LangGraph Chat
          </h2>
          <p className="text-gray-600">
            Start a conversation and let our intelligent AI routing system 
            determine the best response approach for you.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-4">
          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <div className="flex items-center gap-3 mb-2">
              <div className="bg-blue-100 p-2 rounded-lg">
                <Brain className="h-4 w-4 text-blue-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Logical Mode</h3>
            </div>
            <p className="text-sm text-gray-600">
              Get factual, analytical responses for technical questions and problem-solving.
            </p>
          </div>

          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <div className="flex items-center gap-3 mb-2">
              <div className="bg-pink-100 p-2 rounded-lg">
                <Heart className="h-4 w-4 text-pink-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Emotional Mode</h3>
            </div>
            <p className="text-sm text-gray-600">
              Receive empathetic, supportive responses for personal and emotional topics.
            </p>
          </div>

          <div className="bg-white rounded-lg p-4 border border-gray-200">
            <div className="flex items-center gap-3 mb-2">
              <div className="bg-yellow-100 p-2 rounded-lg">
                <Zap className="h-4 w-4 text-yellow-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Smart Routing</h3>
            </div>
            <p className="text-sm text-gray-600">
              Our AI automatically detects your needs and routes to the appropriate agent.
            </p>
          </div>
        </div>

        <button className="bg-blue-600 hover:bg-blue-700 text-white py-3 px-6 rounded-lg font-medium transition-colors">
          Start Your First Chat
        </button>
      </div>
    </div>
  )
}