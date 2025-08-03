from app.database import SessionLocal
from app.services.chat_service import ChatService

def debug_conversations():
    """Debug the get conversations functionality"""
    try:
        db = SessionLocal()
        service = ChatService(db)
        
        # Test with user_id = 1 (same as our test user)
        user_id = 1
        print(f"Getting conversations for user_id: {user_id}")
        
        conversations = service.get_user_conversations(user_id)
        print(f"Found {len(conversations)} conversations")
        
        for conv in conversations:
            print(f"- ID: {conv.id}, Title: {conv.title}, Messages: {len(conv.messages)}")
            
        # Test the response model conversion (same logic as API)
        from app.chat.schemas import ConversationResponse
        
        result = []
        for conv in conversations:
            response = ConversationResponse(
                id=conv.id,
                title=conv.title,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                message_count=len(conv.messages)
            )
            result.append(response)
            print(f"✅ Converted conversation {conv.id} to response model")
        
        print(f"✅ Successfully converted {len(result)} conversations")
        db.close()
        
    except Exception as e:
        print(f"❌ Debug error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_conversations()
