# agent.py
# This is the BRAIN of our application.
# It connects everything together:
# prompts + tools + LLM = a working AI agent
#
# LangGraph works by building a "graph" of steps.
# Think of it like a flowchart — each node is a step,
# and edges are the paths between steps.

import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated
import operator

from tools import get_search_tool, check_emergency_keywords, EMERGENCY_MESSAGE
from prompts import SYSTEM_PROMPT, SEARCH_PROMPT

# ─────────────────────────────────────────
# STEP 1: Define the Agent's State
# ─────────────────────────────────────────
# State is like the agent's "memory" for one conversation.
# Every step in the graph can read and update this state.
# Think of it as a shared notebook all steps can write to.

class AgentState(TypedDict):
    symptoms: str                          # what the user typed
    messages: Annotated[list, operator.add] # conversation history
    search_results: str                    # what Tavily found
    final_response: str                    # what we show the user
    is_emergency: bool                     # emergency flag


# ─────────────────────────────────────────
# STEP 2: Initialize the LLM
# ─────────────────────────────────────────
# This creates our connection to Groq's free LLM.
# We use llama-3.3-70b — a powerful open source model.
# temperature=0.3 means responses are mostly factual,
# not too creative (0 = robotic, 1 = very creative)

def get_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile",
        temperature=0.3,
    )


# ─────────────────────────────────────────
# STEP 3: Define the Graph Nodes
# ─────────────────────────────────────────
# Each function below is one NODE in our graph —
# one step in the agent's thinking process.

def emergency_check_node(state: AgentState) -> AgentState:
    """
    Node 1: Safety first.
    Runs BEFORE anything else.
    If emergency keywords found → set flag and stop.
    """
    is_emergency = check_emergency_keywords(state["symptoms"])
    
    if is_emergency:
        return {
            **state,
            "is_emergency": True,
            "final_response": EMERGENCY_MESSAGE
        }
    
    return {**state, "is_emergency": False}


def search_node(state: AgentState) -> AgentState:
    """
    Node 2: Search the web.
    Uses Tavily to find real medical information.
    Only runs if NOT an emergency.
    """
    search_tool = get_search_tool()
    
    # Format our search query using the SEARCH_PROMPT template
    query = SEARCH_PROMPT.format(symptoms=state["symptoms"])
    
    # Run the search
    results = search_tool.invoke(query)
    
    # results is a list of dicts — extract just the text content
    search_text = "\n\n".join([
        f"Source: {r.get('url', 'Unknown')}\n{r.get('content', '')}"
        for r in results
    ])
    
    return {**state, "search_results": search_text}


def analyze_node(state: AgentState) -> AgentState:
    """
    Node 3: Analyze and respond.
    Sends symptoms + search results to the LLM.
    LLM reads everything and writes a structured response.
    """
    llm = get_llm()
    
    # Build the message with symptoms + what we found
    user_message = f"""
    User symptoms: {state["symptoms"]}
    
    Research findings:
    {state["search_results"]}
    
    Please analyze these findings and provide a helpful, 
    structured response following your guidelines.
    """
    
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_message)
    ]
    
    response = llm.invoke(messages)
    
    return {**state, "final_response": response.content}


# ─────────────────────────────────────────
# STEP 4: Build the Graph
# ─────────────────────────────────────────
# Now we connect all nodes together like a flowchart.
# This is what makes it a LangGraph agent!

def should_continue(state: AgentState) -> str:
    """
    This is a CONDITIONAL EDGE —
    it decides which path the graph takes next.
    
    If emergency → go straight to END
    If not → go to search_node
    """
    if state["is_emergency"]:
        return "end"
    return "search"


def build_agent():
    # Create the graph
    graph = StateGraph(AgentState)
    
    # Add all our nodes
    graph.add_node("emergency_check", emergency_check_node)
    graph.add_node("search", search_node)
    graph.add_node("analyze", analyze_node)
    
    # Set starting point
    graph.set_entry_point("emergency_check")
    
    # Add conditional edge after emergency check
    graph.add_conditional_edges(
        "emergency_check",
        should_continue,
        {
            "end": END,
            "search": "search"
        }
    )
    
    # After search → always go to analyze
    graph.add_edge("search", "analyze")
    
    # After analyze → done
    graph.add_edge("analyze", END)
    
    # Compile and return
    return graph.compile()


# ─────────────────────────────────────────
# STEP 5: Main function to run the agent
# ─────────────────────────────────────────

def run_agent(symptoms: str) -> str:
    """
    This is the function our app.py will call.
    Takes symptoms as input, returns final response.
    """
    agent = build_agent()
    
    initial_state = {
        "symptoms": symptoms,
        "messages": [],
        "search_results": "",
        "final_response": "",
        "is_emergency": False
    }
    
    result = agent.invoke(initial_state)
    return result["final_response"]