"""
Pinecone Utils: Handles vector database interactions and embedding generation.
"""

import os
import time
from typing import List, Dict, Any
from pinecone import Pinecone
from google import genai
from google.genai import types
from src.rag.config import PINECONE_API_KEY, PINECONE_INDEX_NAME, GOOGLE_API_KEY

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# Initialize Gemini
client = genai.Client(api_key=GOOGLE_API_KEY)
EMBEDDING_MODEL = "models/text-embedding-004"

def embed_query(query_text: str) -> List[float]:
    """
    Generate embedding for a query using Gemini.
    Includes strict rate limiting (4s delay) to stay under 15 RPM.
    
    Args:
        query_text: The text to embed
        
    Returns:
        List of floats representing the embedding
    """
    # Enforce rate limit: 15 RPM = 1 request every 4 seconds
    # We sleep BEFORE the call to be safe
    time.sleep(4)
    
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query_text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY"  # Use QUERY for search queries
        )
    )
    
    return response.embeddings[0].values

def search_vectors(query_text: str, top_k: int = 5, filters: Dict = None) -> List[Dict]:
    """
    Search Pinecone index for similar vectors.
    
    Args:
        query_text: The user's query
        top_k: Number of results to return
        filters: Metadata filters (year, category, etc.)
        
    Returns:
        List of matches with metadata
    """
    # Generate embedding
    query_embedding = embed_query(query_text)
    
    # Prepare filters for Pinecone
    pinecone_filter = {}
    if filters:
        for key, value in filters.items():
            if value:
                pinecone_filter[key] = value
                
    # Execute search
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter=pinecone_filter if pinecone_filter else None
    )
    
    # Format results
    matches = []
    for match in results.matches:
        matches.append({
            'id': match.id,
            'score': match.score,
            'title': match.metadata.get('title', 'Untitled'),
            'url': match.metadata.get('url', '#'),
            'content': match.metadata.get('content', ''),
            'excerpt': match.metadata.get('content', '')[:300] + "...",
            'year': int(match.metadata.get('year', 0)) if match.metadata.get('year') else None,
            'category': match.metadata.get('category'),
            'page_type': match.metadata.get('page_type')
        })
        
    return matches
