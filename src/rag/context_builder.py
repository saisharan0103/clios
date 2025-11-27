"""
Context Builder: Formats retrieved documents into a context string for the response generator.
"""

from typing import List, Dict, Any

def build_context(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Format retrieval results into a context string.
    
    Args:
        results: List of retrieved documents
        
    Returns:
        Dictionary containing the formatted context string and metadata
    """
    context_parts = []
    
    for i, res in enumerate(results, 1):
        # Format each result
        part = f"[Result {i}]\n"
        part += f"Title: {res.get('title', 'Untitled')}\n"
        
        # Add metadata
        meta = []
        if res.get('year'):
            meta.append(f"Year: {res['year']}")
        if res.get('category'):
            meta.append(f"Category: {res['category']}")
        if res.get('page_type'):
            meta.append(f"Type: {res['page_type']}")
            
        if meta:
            part += f"Metadata: {' | '.join(meta)}\n"
            
        part += f"Content: {res.get('excerpt', res.get('content', ''))}\n"
        context_parts.append(part)
        
    context_text = "\n\n".join(context_parts)
    
    return {
        "context_text": context_text,
        "source_count": len(results)
    }
