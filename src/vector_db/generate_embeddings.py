"""
Generate Embeddings: Creates vector embeddings for chunked data using Gemini.
"""

import json
import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in .env file")

client = genai.Client(api_key=GOOGLE_API_KEY)
EMBEDDING_MODEL = "models/text-embedding-004"

def generate_embeddings(input_file="data/chunks/clios_chunks.jsonl", output_file="data/embeddings/clios_embeddings.jsonl"):
    print("Starting embedding generation...")
    
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
        
    chunks = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            chunks.append(json.loads(line))
            
    print(f"Loaded {len(chunks)} chunks.")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, chunk in enumerate(chunks):
            try:
                # Rate limiting: 15 RPM = 1 request every 4 seconds
                time.sleep(4)
                
                response = client.models.embed_content(
                    model=EMBEDDING_MODEL,
                    contents=chunk['content'],
                    config=types.EmbedContentConfig(
                        task_type="RETRIEVAL_DOCUMENT"
                    )
                )
                
                embedding = response.embeddings[0].values
                
                record = {
                    "id": chunk['chunk_id'],
                    "values": embedding,
                    "metadata": {
                        "text": chunk['content'],
                        "url": chunk['url'],
                        "title": chunk['title'],
                        "year": chunk['year'],
                        "category": chunk['category'],
                        "page_type": chunk['page_type']
                    }
                }
                
                f.write(json.dumps(record) + "\n")
                
                if (i + 1) % 10 == 0:
                    print(f"Processed {i + 1}/{len(chunks)} chunks...")
                    
            except Exception as e:
                print(f"Error processing chunk {i}: {e}")
                
    print("Embedding generation complete!")

if __name__ == "__main__":
    generate_embeddings()
