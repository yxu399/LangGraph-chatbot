import requests
import json

BASE_URL = "http://localhost:8000"

def test_authenticated_chat():
    """Test chat functionality with authentication (development mode)"""
    
    print("Testing authenticated chat flow...\n")
    
    # Test 1: Get current user
    response = requests.get(f"{BASE_URL}/api/auth/me")
    print(f"1. Get current user: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"   User: {user_data['email']} (ID: {user_data['id']})")
    else:
        print(f"   Error: {response.text}")
        return
    
    # Test 2: Send a chat message
    chat_payload = {
        "message": "Can you help me plan my day?",
        "conversation_id": None
    }
    
    response = requests.post(f"{BASE_URL}/api/chat/send", json=chat_payload)
    print(f"\n2. Send chat message: {response.status_code}")
    if response.status_code == 200:
        chat_data = response.json()
        print(f"   Agent: {chat_data['agent_type']}")
        print(f"   Response: {chat_data['message'][:80]}...")
        conversation_id = chat_data['conversation_id']
    else:
        print(f"   Error: {response.text}")
        return
    
    # Test 3: Get conversations list
    response = requests.get(f"{BASE_URL}/api/chat/conversations")
    print(f"\n3. Get conversations: {response.status_code}")
    if response.status_code == 200:
        conversations = response.json()
        print(f"   Found {len(conversations)} conversations")
        for conv in conversations[:3]:  # Show first 3
            print(f"   - {conv['title']} ({conv['message_count']} messages)")
    else:
        print(f"   Error: {response.text}")
    
    # Test 4: Get specific conversation
    if 'conversation_id' in locals():
        response = requests.get(f"{BASE_URL}/api/chat/conversations/{conversation_id}")
        print(f"\n4. Get conversation details: {response.status_code}")
        if response.status_code == 200:
            conv_data = response.json()
            print(f"   Conversation: {conv_data['title']}")
            print(f"   Messages: {len(conv_data['messages'])}")
        else:
            print(f"   Error: {response.text}")
    
    print("\n✅ Authentication flow test complete!")

if __name__ == "__main__":
    test_authenticated_chat()


