"""
RAG (Retrieval-Augmented Generation) Pipeline for Clio Awards Chatbot.

This package provides a complete RAG implementation including:
- Query processing and filter extraction
- Vector retrieval from Pinecone
- Result reranking
- Context building
- Response generation
"""

from .rag_pipeline import query

__all__ = ['query']
