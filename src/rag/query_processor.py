"""
Query Processor: Handles query analysis and filter extraction using Regex.
"""

import re
from typing import Dict, Any

def extract_filters(query: str) -> Dict[str, Any]:
    """
    Extract filters (year, category, page_type) from the query using regex.
    
    Args:
        query: The user's search query
        
    Returns:
        Dictionary of filters
    """
    filters = {}
    query_lower = query.lower()
    
    # 1. Extract Year (4 digits, 1990-2029)
    year_match = re.search(r'\b(199\d|20[0-2]\d)\b', query)
    if year_match:
        filters['year'] = int(year_match.group(0))
        
    # 2. Extract Category (Keyword matching)
    categories = {
        'clio sports': 'Clio Sports',
        'clio health': 'Clio Health',
        'clio music': 'Clio Music',
        'clio entertainment': 'Clio Entertainment',
        'clio cannabis': 'Clio Cannabis',
        'grand clio': 'Grand Clio',
        'gold': 'Gold',
        'silver': 'Silver',
        'bronze': 'Bronze'
    }
    
    for key, value in categories.items():
        if key in query_lower:
            filters['category'] = value
            break  # Take the first match
            
    # 3. Extract Page Type
    if 'jury' in query_lower or 'juror' in query_lower or 'judge' in query_lower:
        filters['page_type'] = 'jury'
    elif 'winner' in query_lower or 'won' in query_lower or 'award' in query_lower:
        filters['page_type'] = 'winners'
    elif 'event' in query_lower:
        filters['page_type'] = 'events'
        
    return filters
