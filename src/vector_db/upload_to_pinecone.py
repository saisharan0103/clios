"""
Upload to Pinecone: Uploads generated embeddings to the Pinecone index.
"""

import json
import os
import time
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "clios-index")

if not PINECONE_API_KEY:
    raise ValueError("Missing PINECONE_API_KEY in .env file")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

def upload_vectors(input_file="data/embeddings/clios_embeddings.jsonl", batch_size=100):
    print(f"Uploading vectors from {input_file} to index '{PINECONE_INDEX_NAME}'...")
    
    vectors = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            vectors.append(json.loads(line))
            
    print(f"Loaded {len(vectors)} vectors.")
    
    # Batch upload
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        try:
            index.upsert(vectors=batch)
            print(f"Uploaded batch {i // batch_size + 1}/{(len(vectors) + batch_size - 1) // batch_size}")
            time.sleep(1)  # Rate limit protection
        except Exception as e:
            print(f"Error uploading batch starting at {i}: {e}")
            
    print("Upload complete!")

if __name__ == "__main__":
    upload_vectors()
