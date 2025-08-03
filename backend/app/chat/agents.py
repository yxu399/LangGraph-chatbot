from typing import Annotated, Literal, List, Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from app.core.config import settings
from app.models import AgentType

# Initialize LLM with your API key
llm = init_chat_model(
    "anthropic:claude-3-5-sonnet-latest",
    api_key=settings.anthropic_api_key
)


class MessageClassifier(BaseModel):
    message_type: Literal["emotional", "logical", "study", "creative", "planning"] = Field(
        ...,
        description="""Classify the user message:
        - emotional: therapy, feelings, mental health, personal support, anxiety, depression
        - logical: analysis, reasoning, data, problem-solving, factual questions
        - study: learning, explanations, homework, tutoring, "explain this", "help me understand"
        - creative: writing, art, brainstorming, imagination, stories, creative projects
        - planning: scheduling, goals, time management, organization, "help me plan"
        """
    )


class State(TypedDict):
    messages: Annotated[list, add_messages]
    message_type: str | None


def classify_message(state: State):
    """Classify the user's message to route to appropriate agent"""
    last_message = state["messages"][-1]
    classifier_llm = llm.with_structured_output(MessageClassifier)

    result = classifier_llm.invoke([
        {
            "role": "system",
            "content": """Classify the user message based on their primary intent and need."""
        },
        {"role": "user", "content": last_message.content}
    ])
    return {"message_type": result.message_type}


def router(state: State):
    """Route to the appropriate agent based on classification"""
    message_type = state.get("message_type", "logical")
    return {"next": message_type}


def therapist_agent(state: State):
    """Handles emotional support and mental health conversations"""
    conversation_messages = state["messages"]

    messages = [
        {"role": "system",
         "content": """You are a compassionate therapist and emotional support specialist. 
         Focus on the emotional aspects of the user's message. Show empathy, validate their feelings, 
         and help them process their emotions. Ask thoughtful questions to help them explore their 
         feelings more deeply. Provide gentle guidance and coping strategies when appropriate.
         Avoid giving medical advice - suggest professional help for serious concerns."""
         }
    ] + conversation_messages
    
    reply = llm.invoke(messages)
    return {"messages": [reply]}


def logical_agent(state: State):
    """Handles analytical reasoning and problem-solving"""
    conversation_messages = state["messages"]

    messages = [
        {"role": "system",
         "content": """You are a logical analysis expert. Focus on facts, data, and rational reasoning.
         Provide clear, structured answers based on logic and evidence. Break down complex problems 
         into manageable parts. Be direct, methodical, and thorough in your analysis.
         Use examples and step-by-step reasoning when helpful."""
         }
    ] + conversation_messages
    
    reply = llm.invoke(messages)
    return {"messages": [reply]}


def study_buddy_agent(state: State):
    """Handles learning, explanations, and educational support"""
    conversation_messages = state["messages"]

    messages = [
        {"role": "system",
         "content": """You are an expert tutor and study buddy who makes complex topics simple and engaging.
         
         Your approach:
         - Break down concepts into digestible, easy-to-understand parts
         - Use analogies, examples, and real-world connections
         - Ask questions to check understanding and encourage active learning
         - Adapt your explanation level to match the user's background
         - Provide study tips, memory techniques, and learning strategies
         - Be encouraging and patient, celebrating progress
         - Suggest practice problems or follow-up questions when appropriate
         
         Make learning enjoyable and build the user's confidence."""
         }
    ] + conversation_messages
    
    reply = llm.invoke(messages)
    return {"messages": [reply]}


def creative_agent(state: State):
    """Handles creative writing, brainstorming, and artistic projects"""
    conversation_messages = state["messages"]

    messages = [
        {"role": "system",
         "content": """You are a creative writing partner, brainstorming expert, and artistic collaborator.
         
         Your specialties:
         - Generate original ideas, stories, and creative content
         - Help overcome creative blocks and writer's block
         - Brainstorm innovative solutions and out-of-the-box thinking
         - Provide feedback on creative work with constructive suggestions
         - Explore different creative techniques and styles
         - Inspire imagination and artistic expression
         - Collaborate on creative projects as an enthusiastic partner
         
         Be imaginative, inspiring, and supportive. Encourage experimentation and creative risk-taking.
         Ask engaging questions that spark new ideas."""
         }
    ] + conversation_messages
    
    reply = llm.invoke(messages)
    return {"messages": [reply]}


def planning_agent(state: State):
    """Handles goal setting, scheduling, and productivity planning"""
    conversation_messages = state["messages"]

    messages = [
        {"role": "system",
         "content": """You are a productivity coach and planning expert who helps people achieve their goals.
         
         Your expertise includes:
         - Breaking down large goals into actionable, manageable steps
         - Creating realistic timelines and schedules
         - Suggesting effective time management and productivity techniques
         - Helping prioritize tasks and identify what matters most
         - Providing accountability and motivation strategies
         - Designing systems and habits for long-term success
         - Troubleshooting planning challenges and obstacles
         
         Be practical, structured, and motivating. Focus on creating concrete, achievable plans.
         Ask clarifying questions to understand their specific situation and constraints."""
         }
    ] + conversation_messages
    
    reply = llm.invoke(messages)
    return {"messages": [reply]}


# Build the conversation graph
def create_conversation_graph():
    """Create and return the LangGraph conversation flow"""
    graph_builder = StateGraph(State)

    # Add all agent nodes
    graph_builder.add_node("classifier", classify_message)
    graph_builder.add_node("router", router)
    graph_builder.add_node("emotional", therapist_agent)
    graph_builder.add_node("logical", logical_agent)
    graph_builder.add_node("study", study_buddy_agent)
    graph_builder.add_node("creative", creative_agent)
    graph_builder.add_node("planning", planning_agent)

    # Set up the flow
    graph_builder.add_edge(START, "classifier")
    graph_builder.add_edge("classifier", "router")

    # Router directs to appropriate agent
    graph_builder.add_conditional_edges(
        "router",
        lambda state: state.get("next"),
        {
            "emotional": "emotional",
            "logical": "logical", 
            "study": "study",
            "creative": "creative",
            "planning": "planning"
        }
    )

    # All agents lead to END
    graph_builder.add_edge("emotional", END)
    graph_builder.add_edge("logical", END)
    graph_builder.add_edge("study", END)
    graph_builder.add_edge("creative", END)
    graph_builder.add_edge("planning", END)

    return graph_builder.compile()


# Global graph instance
conversation_graph = create_conversation_graph()


def process_message(messages: List[Dict[str, str]]) -> tuple[str, str]:
    """
    Process a conversation through the LangGraph system
    
    Args:
        messages: List of message dicts with 'role' and 'content'
    
    Returns:
        tuple: (response_content, agent_type)
    """
    try:
        # Convert to LangChain message format
        langchain_messages = []
        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))

        # Create state for LangGraph
        state = {
            "messages": langchain_messages,
            "message_type": None
        }

        # Process through the graph
        result_state = conversation_graph.invoke(state)
        
        # Extract response and agent type
        if result_state.get("messages") and len(result_state["messages"]) > 0:
            last_response = result_state["messages"][-1]
            agent_type = result_state.get("message_type", "logical")
            
            return last_response.content, agent_type
        else:
            return "I'm sorry, I couldn't process that message.", "logical"
            
    except Exception as e:
        print(f"Error processing message: {e}")
        return "I'm sorry, something went wrong. Please try again.", "logical"


# Agent type mapping for database storage
AGENT_TYPE_MAPPING = {
    "emotional": AgentType.EMOTIONAL,
    "logical": AgentType.LOGICAL,
    "study": AgentType.STUDY,
    "creative": AgentType.CREATIVE,
    "planning": AgentType.PLANNING
}