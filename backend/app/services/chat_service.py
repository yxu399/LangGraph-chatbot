from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models import User, Conversation, Message, MessageRole, AgentType
from typing import List, Optional


class ChatService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_user(self, clerk_user_id: str, email: str) -> User:
        """Get existing user or create new one"""
        user = self.db.query(User).filter(User.clerk_user_id == clerk_user_id).first()
        if not user:
            user = User(clerk_user_id=clerk_user_id, email=email)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        return user

    def create_conversation(self, user_id: int, title: Optional[str] = None) -> Conversation:
        """Create a new conversation"""
        from sqlalchemy import func
        conversation = Conversation(
            user_id=user_id, 
            title=title,
            updated_at=func.now()  # Explicitly set updated_at
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def get_conversation(self, conversation_id: int, user_id: int) -> Optional[Conversation]:
        """Get conversation with messages, ensuring user owns it"""
        return self.db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ).first()

    def get_user_conversations(self, user_id: int) -> List[Conversation]:
        """Get all conversations for a user"""
        return self.db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(desc(Conversation.updated_at)).all()

    def add_message(
        self, 
        conversation_id: int, 
        content: str, 
        role: MessageRole, 
        agent_type: Optional[AgentType] = None
    ) -> Message:
        """Add a message to a conversation"""
        message = Message(
            conversation_id=conversation_id,
            content=content,
            role=role,
            agent_type=agent_type
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_conversation_messages(self, conversation_id: int) -> List[Message]:
        """Get all messages in a conversation"""
        return self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()

    def auto_generate_title(self, conversation: Conversation) -> str:
        """Auto-generate conversation title from first few messages"""
        messages = self.get_conversation_messages(conversation.id)
        if messages:
            first_user_message = next(
                (msg for msg in messages if msg.role == MessageRole.USER), 
                None
            )
            if first_user_message:
                # Take first 50 characters of first user message
                title = first_user_message.content[:50]
                if len(first_user_message.content) > 50:
                    title += "..."
                return title
        return "New Conversation"