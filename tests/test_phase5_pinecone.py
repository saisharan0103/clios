"""
Verify Phase 5: Checks Pinecone connection and index status.
"""

import os
from pinecone import Pinecone
from dotenv import load_dotenv

def verify_pinecone():
    print("Phase 5 Verification\n")
    
    # Load env vars
    load_dotenv()
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    print("\n1. Environment Variables:")
    print(f"   PINECONE_API_KEY: {'Set' if api_key else 'Missing'}")
    print(f"   PINECONE_INDEX_NAME: {index_name if index_name else 'Missing'}")
    print(f"   GOOGLE_API_KEY: {'Set' if google_key else 'Missing'}")
    
    if not (api_key and index_name):
        print("\nMissing required environment variables.")
        return
        
    try:
        print("\n2. Pinecone Connection:")
        pc = Pinecone(api_key=api_key)
        indexes = pc.list_indexes()
        index_names = [i.name for i in indexes]
        
        if index_name in index_names:
            print(f"   Connected to index: {index_name}")
        else:
            print(f"   Index '{index_name}' not found.")
            return
            
        index = pc.Index(index_name)
        stats = index.describe_index_stats()
        
        print("\n3. Index Statistics:")
        print(f"   Total Vectors: {stats.total_vector_count}")
        print(f"   Dimension: {stats.dimension}")
        
        if stats.total_vector_count > 0:
            print("\nVerification Successful! Pinecone is ready.")
        else:
            print("\nWarning: Index is empty.")
            
    except Exception as e:
        print(f"\nError connecting to Pinecone: {e}")

if __name__ == "__main__":
    verify_pinecone()
