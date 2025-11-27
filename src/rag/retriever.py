"""
Retriever: Handles the retrieval of relevant documents from the vector database.
"""

from typing import List, Dict, Any
from src.vector_db.pinecone_utils import search_vectors

def retrieve(query: str, filters: Dict[str, Any] = None, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve relevant documents from Pinecone based on the query and filters.
    
    Args:
        query: The user's search query
        filters: Optional dictionary of filters (year, category, etc.)
        top_k: Number of results to return
        
    Returns:
        List of relevant document dictionaries
    """
    try:
        results = search_vectors(query, top_k=top_k, filters=filters)
        return results
    except Exception as e:
        print(f"Error in retrieval: {e}")
        return []
