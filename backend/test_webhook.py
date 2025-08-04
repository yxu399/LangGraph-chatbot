import requests
import json

import hmac
import hashlib
import time
import base64
from app.core.config import settings

def create_webhook_signature(payload_str: str, secret_b64: str) -> str:
    """Create a webhook signature like Clerk does (base64-encoded)"""
    timestamp = str(int(time.time()))
    signed_payload = f"{timestamp}.{payload_str}"
    
    # Decode the base64 secret to get the actual secret bytes
    secret_bytes = base64.b64decode(secret_b64)
    
    signature = hmac.new(
        secret_bytes,
        signed_payload.encode(),
        hashlib.sha256
    ).digest()
    # Don't strip padding - svix needs complete base64
    signature_b64url = base64.urlsafe_b64encode(signature).decode()
    return timestamp, signature_b64url

def test_webhook():
    """Test the Clerk webhook endpoint"""
    
    # Sample Clerk user.created webhook payload
    webhook_payload = {
        "type": "user.created",
        "object": "event",
        "data": {
            "id": "user_test_12345",
            "email_addresses": [
                {
                    "email_address": "webhook-test@example.com",
                    "verification": {
                        "status": "verified"
                    }
                }
            ],
            "first_name": "Test",
            "last_name": "User",
            "created_at": int(time.time() * 1000),
            "updated_at": int(time.time() * 1000)
        }
    }
    
    payload_str = json.dumps(webhook_payload, separators=(',', ':'))
    
    # Create signature (if you have webhook secret)
    webhook_secret = settings.clerk_webhook_secret
    if webhook_secret and webhook_secret != "your_clerk_webhook_secret_here":
        # Extract the base64 part from the webhook secret
        if webhook_secret.startswith("whsec_"):
            secret_key = webhook_secret[6:]  # Remove "whsec_" prefix
        else:
            secret_key = webhook_secret
            
        timestamp, signature_b64 = create_webhook_signature(payload_str, secret_key)
        headers = {
            "Content-Type": "application/json",
            "svix-id": "msg_test_12345",
            "svix-timestamp": timestamp,
            "svix-signature": f"v1,{signature_b64}"
        }
    else:
        print("⚠️ No webhook secret configured, testing without signature verification")
        headers = {
            "Content-Type": "application/json"
        }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/auth/webhook",
            data=payload_str,
            headers=headers
        )
        
        print(f"Webhook test: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook endpoint is working!")
        else:
            print("❌ Webhook endpoint failed")
            
    except Exception as e:
        print(f"❌ Webhook test error: {e}")

if __name__ == "__main__":
    test_webhook()
