# tools.py
# This file contains the "actions" our agent can take.
# Think of tools as the agent's hands — the system prompt is its brain,
# but tools are how it actually DOES things in the real world.

import os
from langchain_community.tools.tavily_search import TavilySearchResults

def get_search_tool():
    """
    Creates and returns a Tavily search tool.
    
    Tavily is a search engine built specifically for AI agents —
    unlike Google, it returns clean, structured results that LLMs
    can easily read and reason over.
    """
    search_tool = TavilySearchResults(
        max_results=5,          # fetch top 5 results per search
        search_depth="advanced", # deep search for better medical info
        include_answer=True,     # include a direct answer if available
        include_raw_content=False, # skip raw HTML — we want clean text
        include_images=False,    # no images needed
    )
    return search_tool


def check_emergency_keywords(symptoms: str) -> bool:
    """
    Safety check — scans user input for emergency-level keywords.
    
    This is a simple but critical feature:
    if someone types "chest pain" or "can't breathe",
    we immediately flag it BEFORE the agent even searches.
    
    This is responsible AI design — safety checks should be
    the FIRST thing that runs, not an afterthought.
    """
    emergency_keywords = [
        "chest pain", "can't breathe", "cannot breathe",
        "difficulty breathing", "unconscious", "not breathing",
        "heart attack", "stroke", "severe bleeding",
        "overdose", "suicide", "seizure", "anaphylaxis",
        "allergic reaction", "losing consciousness", "collapse"
    ]
    
    symptoms_lower = symptoms.lower()
    
    for keyword in emergency_keywords:
        if keyword in symptoms_lower:
            return True  # emergency detected
    
    return False  # no emergency keywords found


EMERGENCY_MESSAGE = """
🚨 EMERGENCY ALERT 🚨

The symptoms you described may require IMMEDIATE medical attention.

Please:
1. Call emergency services immediately (112 in Germany / 911 in US)
2. Do NOT wait for an online response
3. If possible, have someone stay with you

This is not the time for an AI assistant — please seek help now.
"""