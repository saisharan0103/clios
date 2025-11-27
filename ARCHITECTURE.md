# System Architecture

## High-Level Overview

The Clio Awards Chatbot is built using a Retrieval-Augmented Generation (RAG) architecture optimized for API rate limits.

```
┌─────────────┐
│   User UI   │ (Streamlit)
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│         RAG Pipeline                     │
│  ┌────────────────────────────────────┐ │
│  │ 1. Query Processor (Regex)         │ │
│  │    - Extract year filter           │ │
│  │    - Extract category filter       │ │
│  │    - Extract page type filter      │ │
│  └────────────────────────────────────┘ │
│                  │                       │
│                  ▼                       │
│  ┌────────────────────────────────────┐ │
│  │ 2. Retriever                       │ │
│  │    - Generate query embedding      │ │ ← 1 API Call (Gemini)
│  │    - Search Pinecone (with filters)│ │
│  │    - Return top-k results          │ │
│  └────────────────────────────────────┘ │
│                  │                       │
│                  ▼                       │
│  ┌────────────────────────────────────┐ │
│  │ 3. Context Builder                 │ │
│  │    - Format search results         │ │
│  │    - Build sources list            │ │
│  └────────────────────────────────────┘ │
│                  │                       │
│                  ▼                       │
│  ┌────────────────────────────────────┐ │
│  │ 4. Response Generator              │ │
│  │    - Format final answer           │ │
│  │    - Add metadata                  │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
                  │
                  ▼
          ┌──────────────┐
          │ Final Answer │
          │ + Sources    │
          └──────────────┘
```

## Data Flow

### 1. Data Ingestion Pipeline

```
Raw HTML (Scraped)
    ↓
Clean & Extract (clean_raw.py)
    ↓
Chunk Documents (chunk_data.py)
    ↓
Generate Embeddings (generate_embeddings.py)
    ↓
Upload to Pinecone (upload_to_pinecone.py)
```

### 2. Query Processing Pipeline

```
User Query: "Who won Clio Sports 2025?"
    ↓
Regex Extraction: {year: 2025, category: "Clio Sports"}
    ↓
Embedding Generation: [0.123, 0.456, ..., 0.789] (768 dims)
    ↓
Pinecone Search: Top 3 results with filters
    ↓
Context Building: Formatted text with sources
    ↓
Response Formatting: "Top Result: ..."
```

## Component Details

### Query Processor (`query_processor.py`)
- **Purpose**: Extract structured filters from natural language
- **Method**: Regular expressions (no LLM)
- **Filters**:
  - Year: 4-digit pattern (1999-2025)
  - Category: Keyword matching (Clio Sports, Clio Health, etc.)
  - Page Type: Heuristic matching (winners, jury, events)

### Retriever (`retriever.py`)
- **Purpose**: Fetch relevant documents from Pinecone
- **Process**:
  1. Generate query embedding (Gemini API)
  2. Apply 4-second rate limit delay
  3. Search Pinecone with filters
  4. Filter by similarity threshold (0.7)
  5. Rerank by score

### Context Builder (`context_builder.py`)
- **Purpose**: Format results for response generation
- **Output Format**:
  ```
  [Source 1] (Relevance: 0.87)
  URL: https://clios.com/sports/
  Type: winners | Year: 2025 | Category: Clio Sports
  Content: ...
  ```

### Response Generator (`response_generator.py`)
- **Purpose**: Create final user-facing answer
- **Method**: Direct formatting (no LLM)
- **Output**:
  - Top result with metadata
  - Related results list
  - Confidence score

## Rate Limiting Strategy

### Problem
- Gemini Free Tier: 15 requests per minute
- Original pipeline: 3 API calls per query (filter + embed + response)
- Result: Frequent 429 errors

### Solution: "One Call" Architecture
- **Filter Extraction**: Regex (0 API calls)
- **Embedding**: Gemini (1 API call with 4s delay)
- **Response**: Formatting (0 API calls)

### Implementation
```python
def embed_query(query_text: str):
    time.sleep(4)  # Enforce 15 RPM limit
    return client.models.embed_content(...)
```

## Database Schema

### Pinecone Index
- **Name**: `clios-index`
- **Dimension**: 768
- **Metric**: Cosine similarity
- **Vectors**: 464 documents

### Vector Metadata
```json
{
  "chunk_id": "clios_0001_0",
  "url": "https://clios.com/sports/",
  "page_type": "winners",
  "year": 2025,
  "category": "Clio Sports",
  "title": "Clio Sports Winners",
  "content": "...",
  "content_length": 1234,
  "chunk_index": 0,
  "total_chunks": 3
}
```

## Performance Characteristics

- **Query Latency**: ~4-5 seconds (due to rate limiting)
- **Accuracy**: High (direct retrieval from curated data)
- **Scalability**: Limited by free tier quotas
- **Reliability**: 100% (no LLM hallucinations)

## Security Considerations

- API keys stored in `.env` (not in repo)
- No user data persistence
- Read-only Pinecone access
- HTTPS for all API calls

## Future Enhancements

1. **Caching**: Cache embeddings for common queries
2. **Reranking**: Add LLM-based reranking when quota allows
3. **Streaming**: Stream responses for better UX
4. **Analytics**: Track query patterns and performance
