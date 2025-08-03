from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.chat_service import ChatService
from app.core.config import settings
import json
import hmac
import hashlib
from svix.webhooks import Webhook

router = APIRouter()


@router.post("/webhook")
async def clerk_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Clerk webhooks for user management"""
    try:
        # Get headers and body
        headers = dict(request.headers)
        body = await request.body()
        
        # Verify webhook signature
        webhook = Webhook(settings.clerk_webhook_secret)
        payload = webhook.verify(body, headers)
        
        event_type = payload.get("type")
        user_data = payload.get("data", {})
        
        service = ChatService(db)
        
        if event_type == "user.created":
            # Create user in our database
            clerk_user_id = user_data.get("id")
            email = user_data.get("email_addresses", [{}])[0].get("email_address")
            
            if clerk_user_id and email:
                user = service.get_or_create_user(clerk_user_id, email)
                print(f"User created: {user.email}")
            
        elif event_type == "user.updated":
            # Update user information
            clerk_user_id = user_data.get("id")
            email = user_data.get("email_addresses", [{}])[0].get("email_address")
            
            if clerk_user_id and email:
                user = service.get_or_create_user(clerk_user_id, email)
                print(f"User updated: {user.email}")
        
        return {"success": True}
        
    except Exception as e:
        print(f"Webhook error: {e}")
        raise HTTPException(status_code=400, detail="Webhook processing failed")


@router.get("/me") 
async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    """Get current user information (placeholder for now)"""
    # TODO: Implement JWT verification
    # For now, return a test user
    service = ChatService(db)
    user = service.get_or_create_user("test_user_123", "test@example.com")
    
    return {
        "id": user.id,
        "clerk_user_id": user.clerk_user_id,
        "email": user.email,
        "created_at": user.created_at
    }