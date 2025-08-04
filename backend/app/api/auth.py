from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.chat_service import ChatService
from app.core.config import settings
from app.core.auth import get_current_user
from app.models import User
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
        
        # Check if signature headers are present
        has_signature_headers = (
            "svix-id" in headers and 
            "svix-timestamp" in headers and 
            "svix-signature" in headers
        )
        
        if has_signature_headers:
            # Try to verify webhook signature
            try:
                webhook = Webhook(settings.clerk_webhook_secret)
                payload = webhook.verify(body, headers)
                print("✅ Webhook signature verified")
            except Exception as verify_error:
                print(f"⚠️ Signature verification failed: {verify_error}")
                print("⚠️ Falling back to parsing without verification")
                payload = json.loads(body.decode())
        else:
            # No signature headers - parse JSON directly (for testing)
            print("⚠️ No signature headers found, parsing without verification")
            payload = json.loads(body.decode())
        
        event_type = payload.get("type")
        user_data = payload.get("data", {})
        
        service = ChatService(db)
        
        if event_type == "user.created":
            # Create user in our database
            clerk_user_id = user_data.get("id")
            email_addresses = user_data.get("email_addresses", [])
            email = email_addresses[0].get("email_address") if email_addresses else None
            
            if clerk_user_id and email:
                user = service.get_or_create_user(clerk_user_id, email)
                print(f"✅ User created via webhook: {user.email}")
            
        elif event_type == "user.updated":
            # Update user information
            clerk_user_id = user_data.get("id")
            email_addresses = user_data.get("email_addresses", [])
            email = email_addresses[0].get("email_address") if email_addresses else None
            
            if clerk_user_id and email:
                user = service.get_or_create_user(clerk_user_id, email)
                print(f"✅ User updated via webhook: {user.email}")
        
        elif event_type == "user.deleted":
            # Handle user deletion (optional)
            clerk_user_id = user_data.get("id")
            print(f"⚠️ User deleted: {clerk_user_id} (implement cleanup if needed)")
        
        return {"success": True, "event": event_type}
        
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        raise HTTPException(status_code=400, detail=f"Webhook processing failed: {str(e)}")


@router.get("/me") 
async def get_current_user_info(user: User = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": user.id,
        "clerk_user_id": user.clerk_user_id,
        "email": user.email,
        "created_at": user.created_at,
        "conversation_count": len(user.conversations)
    }


@router.get("/test")
async def test_auth():
    """Test endpoint to verify auth is working"""
    return {"message": "Auth system is working!", "timestamp": "2025-08-03"}
