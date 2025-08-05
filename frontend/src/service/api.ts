const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Type definitions matching backend
export interface MessageRequest {
  content: string;
  conversation_id?: string;
}

export interface MessageResponse {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  status: 'sending' | 'sent' | 'error' | 'received';
  message_type?: 'emotional' | 'logical';
  agent_used?: 'therapist' | 'logical';
  confidence?: number;
}

export interface ChatResponse {
  user_message: MessageResponse;
  ai_message: MessageResponse;
  conversation_id: string;
}

export interface ConversationResponse {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
  last_message?: string;
}

export interface HealthResponse {
  status: string;
  message: string;
  timestamp: string;
  langgraph_status: string;
}

class ApiService {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      console.log(`🌐 API Request: ${options.method || 'GET'} ${url}`);
      
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error(`❌ API Error: ${response.status} ${errorText}`);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }
      
      const data = await response.json();
      console.log(`✅ API Response:`, data);
      
      return data;
    } catch (error) {
      console.error('❌ API request failed:', error);
      throw error;
    }
  }

  // Health check
  async healthCheck(): Promise<HealthResponse> {
    return this.request<HealthResponse>('/api/health');
  }

  // Conversations
  async getConversations(): Promise<ConversationResponse[]> {
    return this.request<ConversationResponse[]>('/api/conversations');
  }

  async createConversation(title?: string): Promise<ConversationResponse> {
    return this.request<ConversationResponse>('/api/conversations', {
      method: 'POST',
      body: JSON.stringify({ title: title || 'New Conversation' }),
    });
  }

  // Messages
  async sendMessage(
    conversationId: string,
    content: string
  ): Promise<ChatResponse> {
    return this.request<ChatResponse>(`/api/conversations/${conversationId}/messages`, {
      method: 'POST',
      body: JSON.stringify({ content }),
    });
  }
}

export const apiService = new ApiService();

// Test connection function
export async function testConnection(): Promise<boolean> {
  try {
    const health = await apiService.healthCheck();
    console.log('🏥 Backend Health:', health);
    return health.status === 'healthy' || health.status === 'degraded';
  } catch (error) {
    console.error('❌ Backend connection failed:', error);
    return false;
  }
}