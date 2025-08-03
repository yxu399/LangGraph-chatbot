import os
from dotenv import load_dotenv
load_dotenv()

# Test LangGraph agents directly
try:
    from app.chat.agents import process_message
    
    print("Testing LangGraph agents...")
    
    # Simple test message
    messages = [{"role": "user", "content": "Hello, can you help me?"}]
    
    response, agent_type = process_message(messages)
    print(f"✅ Agent response: {agent_type}")
    print(f"✅ Response content: {response[:100]}...")
    
except Exception as e:
    print(f"❌ LangGraph error: {e}")
    import traceback
    traceback.print_exc()

# Test database operations
try:
    from app.database import SessionLocal
    from app.services.chat_service import ChatService
    from app.models import MessageRole
    
    print("\nTesting database operations...")
    
    db = SessionLocal()
    service = ChatService(db)
    
    # Test user creation
    user = service.get_or_create_user("debug_user", "debug@test.com")
    print(f"✅ User: {user.email}")
    
    # Test conversation creation
    conversation = service.create_conversation(user.id, "Debug Chat")
    print(f"✅ Conversation: {conversation.id}")
    
    # Test message creation
    message = service.add_message(conversation.id, "Test message", MessageRole.USER)
    print(f"✅ Message: {message.id}")
    
    db.close()
    
except Exception as e:
    print(f"❌ Database service error: {e}")
    import traceback
    traceback.print_exc()