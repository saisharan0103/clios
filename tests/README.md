# Test Suite

This directory contains all test files for the Clio Awards Chatbot.

## Test Files

### `test_rag_integration.py`
End-to-end integration tests for the RAG pipeline.

**Tests:**
1. Specific fact retrieval
2. Filtered search (jury members)
3. Out-of-domain query handling

**Usage:**
```bash
python tests/test_rag_integration.py
```

### `test_rag_single.py`
Single query test for quick verification.

**Usage:**
```bash
python tests/test_rag_single.py
```

### `test_phase5_pinecone.py`
Pinecone integration verification.

**Tests:**
- Environment variables
- Pinecone connection
- Index statistics
- Vector search functionality

**Usage:**
```bash
python tests/test_phase5_pinecone.py
```

### `test_embeddings.py`
Embedding generation verification.

**Tests:**
- Vector count
- Embedding dimensions
- Metadata structure

**Usage:**
```bash
python tests/test_embeddings.py
```

## Running All Tests

```bash
# Run all tests sequentially
python tests/test_rag_integration.py
python tests/test_rag_single.py
python tests/test_phase5_pinecone.py
python tests/test_embeddings.py
```

## Test Coverage

- Query processing (filter extraction)
- Vector retrieval from Pinecone
- Context building
- Response formatting
- End-to-end pipeline
- Error handling

## Notes

- Tests require valid API keys in `.env`
- Some tests may hit rate limits (wait 60s between runs)
- All tests should pass before deployment
