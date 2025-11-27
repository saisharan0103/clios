"""
Chat Handler: Wrapper for RAG pipeline to be used by the UI.
"""

from typing import Dict
from src.rag import query

def chat(user_query: str) -> Dict:
    """
    Process a user query and return the response.
    
    Args:
        user_query: The user's question
        
    Returns:
        Dictionary containing 'answer', 'sources', 'confidence', etc.
    """
    try:
        # Call the RAG pipeline
        # We enable filters (regex) by default as it's free and helpful
        response = query(user_query, enable_filters=True)
        return response
        
    except Exception as e:
        print(f"Error in chat handler: {e}")
        return {
            "answer": "I encountered an unexpected error. Please try again.",
            "sources": [],
            "confidence": "low",
            "has_answer": False,
            "error": str(e)
        }
