import requests

BASE_URL = "http://localhost:8000"

def test_all_agents_authenticated():
    """Test all agent types with authentication"""
    
    test_cases = [
        ("Can you explain quantum mechanics?", "study"),
        ("Help me write a creative story about space", "creative"),
        ("I need to organize my weekly schedule", "planning"),
        ("I'm feeling overwhelmed with work", "emotional"),
        ("What are the advantages and disadvantages of remote work?", "logical")
    ]
    
    print("Testing all agents with authentication...\n")
    
    for i, (message, expected_agent) in enumerate(test_cases, 1):
        payload = {
            "message": message,
            "conversation_id": None
        }
        
        response = requests.post(f"{BASE_URL}/api/chat/send", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"{i}. ✅ Message: '{message[:40]}...'")
            print(f"   Agent: {data['agent_type']} (Expected: {expected_agent})")
            print(f"   Response: {data['message'][:60]}...\n")
        else:
            print(f"{i}. ❌ Failed: {response.status_code} - {response.text}\n")

if __name__ == "__main__":
    test_all_agents_authenticated()


