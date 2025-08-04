import requests
import json
import time

def test_webhook_without_signature():
    """Test the Clerk webhook endpoint without signature verification"""
    
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
    
    # Test without signature headers
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/auth/webhook",
            data=payload_str,
            headers=headers
        )
        
        print(f"Webhook test (no signature): {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook endpoint is working without signature!")
        else:
            print("❌ Webhook endpoint failed even without signature")
            
    except Exception as e:
        print(f"❌ Webhook test error: {e}")

if __name__ == "__main__":
    test_webhook_without_signature()
