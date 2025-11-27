"""
Verify Embeddings: Checks if embeddings were generated correctly.
"""

import json
import os

def verify_embeddings(file_path="data/embeddings/clios_embeddings.jsonl"):
    print(f"Checking embeddings in {file_path}...")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
        
    vectors = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            vectors.append(json.loads(line))
            
    if not vectors:
        print("No vectors found.")
        return
        
    print(f"Total vectors: {len(vectors)}")
    print(f"First vector ID: {vectors[0]['id']}")
    print(f"Embedding dimensions: {len(vectors[0]['values'])}")
    print(f"Metadata keys: {list(vectors[0]['metadata'].keys())}")
    
    print(f"\nSample vector record:")
    print(json.dumps(vectors[0], indent=2)[:500] + "...")
    
    if len(vectors[0]['values']) == 768:
        print(f"\nAll {len(vectors)} vectors ready for Pinecone upload!")
    else:
        print(f"\nWarning: Dimension mismatch. Expected 768, got {len(vectors[0]['values'])}")

if __name__ == "__main__":
    verify_embeddings()
