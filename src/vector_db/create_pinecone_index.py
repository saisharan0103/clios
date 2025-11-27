"""
Create Pinecone Index: Initializes the Pinecone index with correct settings.
"""

import os
import time
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "clios-index")

if not PINECONE_API_KEY:
    raise ValueError("Missing PINECONE_API_KEY in .env file")

pc = Pinecone(api_key=PINECONE_API_KEY)

# Index Config
DIMENSION = 768  # For text-embedding-004
METRIC = "cosine"

def create_index():
    print(f"Checking if index '{PINECONE_INDEX_NAME}' exists...")
    
    existing_indexes = [i.name for i in pc.list_indexes()]
    
    if PINECONE_INDEX_NAME not in existing_indexes:
        print(f"Creating index '{PINECONE_INDEX_NAME}'...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=DIMENSION,
            metric=METRIC,
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print("Waiting for index to be ready...")
        time.sleep(10)
    else:
        print(f"Index '{PINECONE_INDEX_NAME}' already exists.")
        
    index = pc.Index(PINECONE_INDEX_NAME)
    stats = index.describe_index_stats()
    
    print("Index Statistics:")
    print(f"   Status: Ready")
    print(f"   Dimension: {DIMENSION}")
    print(f"   Metric: {METRIC}")
    print(f"   Total Vectors: {stats.total_vector_count}")
    print("\nPinecone index is ready for vector upload!")

if __name__ == "__main__":
    create_index()
