"""
Single Query Test: Quick verification of the RAG pipeline.
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.rag import query

def verify_single_query():
    print("Verifying Single Query...\n")
    
    q = "Who won Clio Sports 2025?"
    print(f"Query: {q}")
    
    try:
        response = query(q)
        print(f"\nAnswer:\n{response['answer']}")
        
        if response['has_answer']:
            print("\nVerification Successful!")
        else:
            print("\nVerification Failed: No answer found.")
            
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    verify_single_query()
