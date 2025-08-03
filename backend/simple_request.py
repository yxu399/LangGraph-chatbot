import requests
import json

def simple_chat_test():
    url = "http://localhost:8000/api/chat/send"
    payload = {
        "message": "Hello",
        "conversation_id": None
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code != 200:
            print("❌ Request failed")
        else:
            print("✅ Request succeeded")
            
    except Exception as e:
        print(f"❌ Request error: {e}")

if __name__ == "__main__":
    simple_chat_test()


