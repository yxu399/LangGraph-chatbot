export type MessageType = 'emotional' | 'logical';

export type MessageRole = 'user' | 'assistant' | 'system';

export type MessageStatus = 'sending' | 'sent' | 'error' | 'received';

export type AgentType = 'therapist' | 'logical';

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: Date;
  status?: MessageStatus;
  messageType?: MessageType;
  agentUsed?: AgentType;
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
  lastMessage?: Message;
}

export interface ChatState {
  conversations: Conversation[];
  currentConversationId: string | null;
  isTyping: boolean;
  typingAgent?: AgentType;
  isConnected: boolean;
  error: string | null;
}