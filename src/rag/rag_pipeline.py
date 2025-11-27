"""
RAG Pipeline: Orchestrates the entire retrieval and generation process.
"""

import time
from typing import Dict, Optional
from .query_processor import extract_filters
from .retriever import retrieve
from .context_builder import build_context
from .response_generator import generate_response

def query(user_query: str, enable_filters: bool = True) -> Dict:
    """
    Execute the full RAG pipeline for a user query.
    
    Args:
        user_query: The user's question
        enable_filters: Whether to use regex-based filtering
        
    Returns:
        Dictionary containing answer, sources, and metadata
    """
    start_time = time.time()
    
    # 1. Query Processing (Filter Extraction)
    # This is a regex-based operation (0 API calls)
    filters = {}
    if enable_filters:
        filters = extract_filters(user_query)
    
    # 2. Retrieval (Pinecone Search)
    # This involves 1 API call for embedding generation
    # The embedding function has a built-in 4s delay for rate limiting
    retrieval_results = retrieve(user_query, filters=filters)
    
    # 3. Context Building
    # Format the results for display
    context_data = build_context(retrieval_results)
    
    # 4. Response Generation
    # Direct formatting of results (0 API calls)
    response = generate_response(user_query, context_data['context_text'], retrieval_results)
    
    processing_time = round(time.time() - start_time, 2)
    
    # Add metadata to response
    response['processing_time'] = processing_time
    response['filters_used'] = filters
    response['sources'] = retrieval_results
    
    return response
