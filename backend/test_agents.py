from app.chat.agents import process_message, AGENT_TYPE_MAPPING

def test_agents():
    """Test all agents with sample messages"""
    test_cases = [
        {
            "name": "Study Buddy",
            "messages": [{"role": "user", "content": "Can you explain how machine learning works?"}],
            "expected_agent": "study"
        },
        {
            "name": "Creative Agent", 
            "messages": [{"role": "user", "content": "Help me write a story about AI"}],
            "expected_agent": "creative"
        },
        {
            "name": "Planning Agent",
            "messages": [{"role": "user", "content": "Help me plan my study schedule"}],
            "expected_agent": "planning"
        },
        {
            "name": "Therapist Agent",
            "messages": [{"role": "user", "content": "I'm feeling anxious about job interviews"}],
            "expected_agent": "emotional"
        },
        {
            "name": "Logical Agent",
            "messages": [{"role": "user", "content": "What are the pros and cons of remote work?"}],
            "expected_agent": "logical"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n=== Testing {test_case['name']} ===")
        print(f"Input: {test_case['messages'][0]['content']}")
        
        try:
            response, agent_type = process_message(test_case['messages'])
            db_agent_type = AGENT_TYPE_MAPPING.get(agent_type)
            
            print(f"Agent: {agent_type} ({db_agent_type})")
            print(f"Response: {response[:100]}...")
            
            if agent_type == test_case['expected_agent']:
                print("✅ Correct agent selected")
            else:
                print(f"❌ Expected {test_case['expected_agent']}, got {agent_type}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_agents()

