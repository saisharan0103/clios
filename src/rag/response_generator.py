"""
Response Generator: Uses Google Gemini LLM to generate natural conversational answers.
"""

from typing import Dict, List, Any
import google.generativeai as genai
from .config import GOOGLE_API_KEY, LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS

# Configure Google Gemini
genai.configure(api_key=GOOGLE_API_KEY)

def generate_response(query: str, context: str, sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate a natural conversational answer using Google Gemini LLM.
    
    Args:
        query: The user's question
        context: The formatted context string from retrieved documents
        sources: List of source documents
        
    Returns:
        Dictionary containing the LLM-generated answer
    """
    if not sources:
        return {
            "answer": "I couldn't find any relevant information in the database about that topic.",
            "confidence": "low",
            "has_answer": False
        }
    
    # Build the prompt for the LLM
    prompt = f"""You are a helpful assistant for the Clio Awards. Answer the user's question based on the provided context from the Clio Awards database.

User Question: {query}

Context from Clio Awards Database:
{context}

Instructions:
- Provide a clear, conversational answer based on the context above
- If the context contains specific information (winners, categories, years, jury members), include those details
- Be concise but informative
- If the context doesn't fully answer the question, acknowledge what information is available
- Do not make up information not present in the context
- Use a friendly, professional tone

Answer:"""

    try:
        # Call Google Gemini LLM
        model = genai.GenerativeModel(LLM_MODEL)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=LLM_TEMPERATURE,
                max_output_tokens=LLM_MAX_TOKENS,
            )
        )
        
        answer = response.text.strip()
        
        return {
            "answer": answer,
            "confidence": "high",
            "has_answer": True
        }
        
    except Exception as e:
        print(f"Error generating LLM response: {e}")
        
        # Fallback to direct formatting if LLM fails
        top_result = sources[0]
        fallback_answer = f"Based on the search results:\n\n"
        fallback_answer += f"**{top_result['title']}**\n"
        
        if top_result.get('category'):
            fallback_answer += f"Category: {top_result['category']}\n"
        if top_result.get('year'):
            fallback_answer += f"Year: {top_result['year']}\n"
            
        fallback_answer += f"\n{top_result.get('excerpt', top_result.get('content', '')[:300])}"
        
        return {
            "answer": fallback_answer,
            "confidence": "medium",
            "has_answer": True,
            "error": str(e)
        }
