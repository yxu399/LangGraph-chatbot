import requests
import json

BASE_URL = "http://localhost:8000"

def test_agent(message, expected_agent):
    """Test a specific agent with a message"""
    payload = {
        "message": message,
        "conversation_id": None
    }
    
    response = requests.post(f"{BASE_URL}/api/chat/send", json=payload)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Message: '{message[:30]}...'")
        print(f"   Agent: {data['agent_type']}")
        print(f"   Response: {data['message'][:80]}...")
        return data['agent_type']
    else:
        print(f"❌ Failed: {response.text}")
        return None

def test_all_agents():
    """Test all 5 agent types"""
    test_cases = [
        ("Can you explain quantum physics?", "study"),
        ("Help me write a creative story", "creative"), 
        ("I need to plan my weekly schedule", "planning"),
        ("I'm feeling stressed about work", "emotional"),
        ("What are the pros and cons of AI?", "logical")
    ]
    
    print("Testing all agent types...\n")
    
    for message, expected in test_cases:
        agent_type = test_agent(message, expected)
        print()

if __name__ == "__main__":
    test_all_agents()


