from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.chat_service import ChatService
from app.chat.schemas import (
    ChatRequest, ChatResponse, ConversationCreate, 
    ConversationResponse, ConversationDetail, ChatMessage
)
from app.chat.agents import process_message, AGENT_TYPE_MAPPING
from app.models import MessageRole, AgentType, User
from app.core.auth import get_current_user_id, get_current_user  # Updated imports
import json

router = APIRouter()


@router.post("/send", response_model=ChatResponse)
async def send_message(
    chat_request: ChatRequest,
    user_id: int = Depends(get_current_user_id),  # Now uses real auth
    db: Session = Depends(get_db)
):
    """Send a message and get AI response"""
    try:
        service = ChatService(db)
        
        # Get or create conversation
        if chat_request.conversation_id:
            conversation = service.get_conversation(chat_request.conversation_id, user_id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Create new conversation
            conversation = service.create_conversation(user_id)
        
        # Add user message to database
        user_message = service.add_message(
            conversation.id,
            chat_request.message,
            MessageRole.USER
        )
        
        # Get conversation history for context
        messages = service.get_conversation_messages(conversation.id)
        
        # Convert to format expected by LangGraph
        conversation_history = []
        for msg in messages:
            conversation_history.append({
                "role": msg.role.value,
                "content": msg.content
            })
        
        # Process through LangGraph
        response_content, agent_type_str = process_message(conversation_history)
        agent_type = AGENT_TYPE_MAPPING.get(agent_type_str, AgentType.LOGICAL)
        
        # Add AI response to database
        ai_message = service.add_message(
            conversation.id,
            response_content,
            MessageRole.ASSISTANT,
            agent_type
        )
        
        # Auto-generate title if this is the first exchange
        if not conversation.title and len(messages) == 1:
            title = service.auto_generate_title(conversation)
            conversation.title = title
            db.commit()
        
        return ChatResponse(
            message=response_content,
            agent_type=agent_type,
            conversation_id=conversation.id,
            message_id=ai_message.id
        )
        
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process message")


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    user_id: int = Depends(get_current_user_id),  # Now uses real auth
    db: Session = Depends(get_db)
):
    """Get all conversations for the current user"""
    try:
        service = ChatService(db)
        conversations = service.get_user_conversations(user_id)
        
        result = []
        for conv in conversations:
            result.append(ConversationResponse(
                id=conv.id,
                title=conv.title,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                message_count=len(conv.messages)
            ))
        
        return result
        
    except Exception as e:
        print(f"Get conversations error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get conversations")


@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(
    conversation_id: int,
    user_id: int = Depends(get_current_user_id),  # Now uses real auth
    db: Session = Depends(get_db)
):
    """Get a specific conversation with all messages"""
    try:
        service = ChatService(db)
        
        conversation = service.get_conversation(conversation_id, user_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Convert messages to schema format
        messages = []
        for msg in conversation.messages:
            messages.append(ChatMessage(
                content=msg.content,
                role=msg.role,
                agent_type=msg.agent_type,
                created_at=msg.created_at
            ))
        
        return ConversationDetail(
            id=conversation.id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=messages
        )
        
    except Exception as e:
        print(f"Get conversation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get conversation")


@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    conversation_data: ConversationCreate,
    user_id: int = Depends(get_current_user_id),  # Now uses real auth
    db: Session = Depends(get_db)
):
    """Create a new conversation"""
    try:
        service = ChatService(db)
        conversation = service.create_conversation(user_id, conversation_data.title)
        
        return ConversationResponse(
            id=conversation.id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            message_count=0
        )
        
    except Exception as e:
        print(f"Create conversation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create conversation")


# WebSocket endpoint (unchanged for now)
@router.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: int):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            response = {
                "type": "message",
                "content": f"Echo: {message_data.get('message', '')}",
                "agent_type": "logical"
            }
            
            await websocket.send_text(json.dumps(response))
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for conversation {conversation_id}")