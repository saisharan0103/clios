"""
Configuration settings for the Clio Awards Chatbot.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "clios-index")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Validation
if not PINECONE_API_KEY:
    raise ValueError("Missing PINECONE_API_KEY in .env file")
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in .env file")

# Constants
EMBEDDING_MODEL = "models/text-embedding-004"
DIMENSION = 768
METRIC = "cosine"

# LLM Configuration
LLM_MODEL = "gemini-2.0-flash"
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 1024
