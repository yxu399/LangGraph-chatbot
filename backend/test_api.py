import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code}")
    print(f"Response: {response.json()}")

def test_chat():
    """Test chat endpoint"""
    payload = {
        "message": "Can you explain how photosynthesis works?",
        "conversation_id": None
    }
    
    response = requests.post(f"{BASE_URL}/api/chat/send", json=payload)
    print(f"\nChat test: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Agent: {data['agent_type']}")
        print(f"Response: {data['message'][:100]}...")
        print(f"Conversation ID: {data['conversation_id']}")
        return data['conversation_id']
    else:
        print(f"Error: {response.text}")
        return None

def test_get_conversations():
    """Test get conversations endpoint"""
    response = requests.get(f"{BASE_URL}/api/chat/conversations")
    print(f"\nConversations test: {response.status_code}")
    if response.status_code == 200:
        conversations = response.json()
        print(f"Found {len(conversations)} conversations")
        for conv in conversations:
            print(f"- {conv['title']} ({conv['message_count']} messages)")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    print("Testing AI Chat Platform API...")
    test_health()
    conversation_id = test_chat()
    test_get_conversations()
    
    if conversation_id:
        print(f"\n✅ Successfully created conversation {conversation_id}")
    else:
        print("\n❌ Failed to create conversation")