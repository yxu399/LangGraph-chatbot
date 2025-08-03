import os
from dotenv import load_dotenv
load_dotenv()

# Test the exact same logic as the API endpoint
def test_chat_endpoint_logic():
    try:
        from app.database import SessionLocal
        from app.services.chat_service import ChatService
        from app.chat.agents import process_message, AGENT_TYPE_MAPPING
        from app.models import MessageRole, AgentType
        
        print("Testing exact API endpoint logic...")
        
        # Simulate the API endpoint logic
        user_id = 1  # Test user ID
        message_content = "Can you explain machine learning?"
        conversation_id = None
        
        db = SessionLocal()
        service = ChatService(db)
        
        print(f"1. User ID: {user_id}")
        print(f"2. Message: {message_content}")
        
        # Get or create conversation (same as API)
        if conversation_id:
            conversation = service.get_conversation(conversation_id, user_id)
            print(f"3. Found existing conversation: {conversation}")
        else:
            # Create new conversation
            conversation = service.create_conversation(user_id)
            print(f"3. Created new conversation: {conversation.id}")
        
        # Add user message to database (same as API)
        user_message = service.add_message(
            conversation.id,
            message_content,
            MessageRole.USER
        )
        print(f"4. Added user message: {user_message.id}")
        
        # Get conversation history for context (same as API)
        messages = service.get_conversation_messages(conversation.id)
        print(f"5. Retrieved {len(messages)} messages for context")
        
        # Convert to format expected by LangGraph (same as API)
        conversation_history = []
        for msg in messages:
            conversation_history.append({
                "role": msg.role.value,
                "content": msg.content
            })
        print(f"6. Converted to LangGraph format: {len(conversation_history)} messages")
        
        # Process through LangGraph (same as API)
        response_content, agent_type_str = process_message(conversation_history)
        print(f"7. LangGraph response: {agent_type_str}")
        print(f"8. Response content: {response_content[:100]}...")
        
        agent_type = AGENT_TYPE_MAPPING.get(agent_type_str, AgentType.LOGICAL)
        print(f"9. Mapped agent type: {agent_type}")
        
        # Add AI response to database (same as API)
        ai_message = service.add_message(
            conversation.id,
            response_content,
            MessageRole.ASSISTANT,
            agent_type
        )
        print(f"10. Added AI message: {ai_message.id}")
        
        # Auto-generate title if needed (same as API)
        if not conversation.title and len(messages) == 1:
            title = service.auto_generate_title(conversation)
            conversation.title = title
            db.commit()
            print(f"11. Generated title: {title}")
        
        print("✅ All API endpoint logic works!")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ API endpoint logic error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_chat_endpoint_logic()


