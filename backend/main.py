from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid
import json
import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory to the path to import your existing main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your existing LangGraph system
try:
    from main import graph
    LANGGRAPH_AVAILABLE = True
    print("✅ Successfully imported LangGraph system from main.py")
except ImportError as e:
    print(f"❌ Could not import LangGraph system: {e}")
    print("⚠️  Falling back to mock responses")
    LANGGRAPH_AVAILABLE = False

from pydantic import BaseModel
from typing import Literal

# Models (keeping them inline for simplicity)
MessageRole = Literal["user", "assistant", "system"]
MessageType = Literal["emotional", "logical"]
AgentType = Literal["therapist", "logical"]
MessageStatus = Literal["sending", "sent", "error", "received"]

class MessageRequest(BaseModel):
    content: str
    conversation_id: Optional[str] = None

class MessageResponse(BaseModel):
    id: str
    role: MessageRole
    content: str
    timestamp: datetime
    status: MessageStatus
    message_type: Optional[MessageType] = None
    agent_used: Optional[AgentType] = None
    confidence: Optional[float] = None

class ChatResponse(BaseModel):
    user_message: MessageResponse
    ai_message: MessageResponse
    conversation_id: str

class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"

class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int
    last_message: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: datetime
    langgraph_status: str

# Simple in-memory storage for development
# TODO: Replace with your PostgreSQL database
conversations_db = {}
messages_db = {}

# LangGraph Service
class LangGraphService:
    def __init__(self):
        self.available = LANGGRAPH_AVAILABLE
        
    def process_message(self, user_message: str, conversation_history: list = None) -> tuple[MessageResponse, MessageResponse]:
        """Process a user message through your LangGraph system"""
        
        # Create user message response
        user_msg = MessageResponse(
            id=str(uuid.uuid4()),
            role="user",
            content=user_message,
            timestamp=datetime.now(),
            status="sent"
        )
        
        if self.available:
            try:
                # Use your actual LangGraph system
                ai_response = self._invoke_langgraph(user_message, conversation_history)
                
                ai_msg = MessageResponse(
                    id=str(uuid.uuid4()),
                    role="assistant",
                    content=ai_response["content"],
                    timestamp=datetime.now(),
                    status="received",
                    message_type=ai_response["message_type"],
                    agent_used=ai_response["agent_used"],
                    confidence=ai_response.get("confidence", 90)
                )
                
                return user_msg, ai_msg
                
            except Exception as e:
                print(f"❌ Error invoking LangGraph: {e}")
                return user_msg, self._get_mock_response()
        else:
            return user_msg, self._get_mock_response()
    
    def _invoke_langgraph(self, user_message: str, conversation_history: list = None) -> Dict[str, Any]:
        """Invoke your actual LangGraph system"""
        
        # Prepare messages for your LangGraph system
        messages = []
        
        if conversation_history:
            for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Add the new user message
        messages.append({
            "role": "user", 
            "content": user_message
        })
        
        # Create state for your LangGraph system
        state = {
            "messages": messages,
            "message_type": None
        }
        
        print(f"🤖 Invoking LangGraph with: {user_message}")
        
        # Invoke your LangGraph system
        result = graph.invoke(state)
        
        print(f"📝 LangGraph result: {result}")
        
        # Extract the AI response
        if result.get("messages") and len(result["messages"]) > 0:
            last_message = result["messages"][-1]
            message_type = result.get("message_type", "logical")
            agent_used = "therapist" if message_type == "emotional" else "logical"
            
            return {
                "content": last_message.get("content", "I apologize, but I couldn't generate a proper response."),
                "message_type": message_type,
                "agent_used": agent_used,
                "confidence": 95
            }
        else:
            raise Exception("No response generated from LangGraph")
    
    def _get_mock_response(self) -> MessageResponse:
        """Mock response for development"""
        import random
        
        mock_responses = [
            {
                "content": "🔧 [Mock Mode] I understand you're reaching out, and I want you to know that I'm here to support you. The real LangGraph system will provide more personalized responses.",
                "message_type": "emotional",
                "agent_used": "therapist"
            },
            {
                "content": "🔧 [Mock Mode] Based on your query, I can provide structured information. The real LangGraph system will give you more detailed technical analysis.",
                "message_type": "logical", 
                "agent_used": "logical"
            }
        ]
        
        mock = random.choice(mock_responses)
        
        return MessageResponse(
            id=str(uuid.uuid4()),
            role="assistant",
            content=mock['content'],
            timestamp=datetime.now(),
            status="received",
            message_type=mock["message_type"],
            agent_used=mock["agent_used"],
            confidence=75
        )
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the LangGraph system is working"""
        if self.available:
            try:
                # Test with a simple message
                test_state = {
                    "messages": [{"role": "user", "content": "Hello"}],
                    "message_type": None
                }
                
                result = graph.invoke(test_state)
                
                return {
                    "status": "healthy",
                    "langgraph_available": True,
                    "message": "LangGraph system is operational"
                }
            except Exception as e:
                return {
                    "status": "error",
                    "langgraph_available": False,
                    "message": f"LangGraph system error: {str(e)}"
                }
        else:
            return {
                "status": "mock",
                "langgraph_available": False,
                "message": "Running in mock mode - LangGraph not available"
            }

# Initialize FastAPI app
app = FastAPI(
    title="LangGraph Chat API",
    description="Backend API for LangGraph intelligent chat application",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
langgraph_service = LangGraphService()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass  # Connection might be closed

manager = ConnectionManager()

# API Endpoints
@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Check API and LangGraph system health"""
    langgraph_health = langgraph_service.health_check()
    
    return HealthResponse(
        status="healthy" if langgraph_health["status"] != "error" else "degraded",
        message=f"API is running. {langgraph_health['message']}",
        timestamp=datetime.now(),
        langgraph_status=langgraph_health["status"]
    )

@app.get("/api/conversations", response_model=List[ConversationResponse])
async def get_conversations():
    """Get all conversations"""
    conversations = []
    for conv_id, conv_data in conversations_db.items():
        conv_messages = messages_db.get(conv_id, [])
        last_message = conv_messages[-1].content if conv_messages else None
        
        conversations.append(ConversationResponse(
            id=conv_id,
            title=conv_data["title"],
            created_at=conv_data["created_at"],
            updated_at=conv_data["updated_at"],
            message_count=len(conv_messages),
            last_message=last_message
        ))
    
    return sorted(conversations, key=lambda x: x.updated_at, reverse=True)

@app.post("/api/conversations", response_model=ConversationResponse)
async def create_conversation(conversation: ConversationCreate):
    """Create a new conversation"""
    conversation_id = str(uuid.uuid4())
    now = datetime.now()
    
    conversations_db[conversation_id] = {
        "title": conversation.title,
        "created_at": now,
        "updated_at": now
    }
    messages_db[conversation_id] = []
    
    return ConversationResponse(
        id=conversation_id,
        title=conversation.title,
        created_at=now,
        updated_at=now,
        message_count=0
    )

@app.post("/api/conversations/{conversation_id}/messages", response_model=ChatResponse)
async def send_message(conversation_id: str, message_request: MessageRequest):
    """Send a message and get AI response"""
    
    # Check if conversation exists, create if it doesn't
    if conversation_id not in conversations_db:
        conversations_db[conversation_id] = {
            "title": "New Conversation",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        messages_db[conversation_id] = []
    
    try:
        # Get conversation history
        conversation_history = messages_db.get(conversation_id, [])
        
        # Process message through LangGraph
        user_msg, ai_msg = langgraph_service.process_message(
            message_request.content, 
            conversation_history
        )
        
        # Save messages
        messages_db[conversation_id].extend([user_msg, ai_msg])
        
        # Update conversation timestamp
        conversations_db[conversation_id]["updated_at"] = datetime.now()
        
        # Update title if this is the first message
        if len(messages_db[conversation_id]) == 2:  # First user + AI message
            title = message_request.content[:50] + ("..." if len(message_request.content) > 50 else "")
            conversations_db[conversation_id]["title"] = title
        
        # Broadcast to WebSocket connections
        await manager.broadcast(json.dumps({
            "type": "message",
            "conversation_id": conversation_id,
            "user_message": user_msg.model_dump(mode='json'),
            "ai_message": ai_msg.model_dump(mode='json')
        }, default=str))
        
        return ChatResponse(
            user_message=user_msg,
            ai_message=ai_msg,
            conversation_id=conversation_id
        )
        
    except Exception as e:
        print(f"❌ Error processing message: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    print("🚀 Starting LangGraph Chat API...")
    print(f"📊 Database URL: {os.getenv('DATABASE_URL', 'In-memory storage')}")
    
    # Test LangGraph integration
    health = langgraph_service.health_check()
    if health["langgraph_available"]:
        print("✅ LangGraph system connected and ready")
    else:
        print("⚠️  LangGraph system not available - running in mock mode")
        print(f"   Reason: {health['message']}")
    
    print("🌐 API server ready at http://localhost:8000")
    print("📖 API docs available at http://localhost:8000/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )