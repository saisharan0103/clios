# Clio Awards Chatbot

A production-ready RAG (Retrieval-Augmented Generation) chatbot that answers questions about Clio Awards using Pinecone vector search and Google Gemini AI.

## Overview

This chatbot provides intelligent answers about Clio Awards winners, jury members, and events by combining:
- **Vector Search** (Pinecone) for semantic retrieval
- **LLM** (Google Gemini) for embeddings
- **Streamlit** for the user interface
- **Optimized "One Call" Architecture** to avoid API rate limits

## Project Structure

```
clios-chatbot/
├── data/                          # Data files
│   ├── raw/                       # Raw scraped HTML files
│   ├── cleaned/                   # Cleaned JSON data
│   └── chunks/                    # Chunked data ready for embedding
├── src/                           # Source code
│   ├── preprocessing/             # Data preprocessing modules
│   │   ├── clean_raw.py          # Clean raw HTML data
│   │   └── chunk_data.py         # Chunk cleaned data
│   ├── scraping/                  # Web scraping
│   │   └── local_crawler.py      # Crawl Clio Awards website
│   ├── vector_db/                 # Pinecone integration
│   │   ├── pinecone_utils.py     # Pinecone utility functions
│   │   ├── create_pinecone_index.py  # Create Pinecone index
│   │   ├── generate_embeddings.py    # Generate embeddings
│   │   ├── upload_to_pinecone.py     # Upload vectors to Pinecone
│   │   └── test_pinecone_search.py   # Test Pinecone search
│   └── rag/                       # RAG pipeline
│       ├── config.py              # Configuration settings
│       ├── query_processor.py    # Extract filters from queries (regex)
│       ├── retriever.py          # Retrieve from Pinecone
│       ├── context_builder.py    # Build context from results
│       ├── response_generator.py # Format response
│       ├── rag_pipeline.py       # Main pipeline orchestrator
│       └── chat_handler.py       # UI wrapper
├── ui/                            # Streamlit UI
│   └── app.py                    # Main Streamlit application
├── tests/                         # Test suite
│   ├── test_rag_integration.py   # Integration tests
│   ├── test_embeddings.py        # Embedding verification
│   ├── test_phase5_pinecone.py   # Pinecone tests
│   └── test_rag_single.py        # Single query test
├── scripts/                       # Utility scripts
│   ├── check_stats.py            # Check data statistics
│   └── list_gemini_models.py     # List available Gemini models
├── .env                          # Environment variables (not in repo)
├── .gitignore                    # Git ignore file
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Pinecone account (free tier)
- Google Gemini API key (free tier)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd clios-chatbot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv virtualenv
   virtualenv\Scripts\activate  # Windows
   # or
   source virtualenv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_INDEX_NAME=clios-index
   GOOGLE_API_KEY=your_google_api_key
   ```

### Running Locally

**Start the Streamlit UI:**
```bash
streamlit run ui/app.py
```

The app will open at `http://localhost:8501`

## Architecture

### RAG Pipeline Flow

```
User Query
    ↓
1. Query Processor (Regex Filter Extraction)
    ↓
2. Retriever (Pinecone Vector Search) ← 1 API Call (Embedding)
    ↓
3. Context Builder (Format Results)
    ↓
4. Response Generator (Format Answer)
    ↓
Final Answer with Sources
```

### Key Design Decisions

1. **"One Call" Architecture**: Only 1 API call per query (embedding) to avoid rate limits
2. **Regex Filtering**: Extract filters (year, category) without LLM calls
3. **Direct Response Formatting**: Return formatted search results instead of LLM-generated answers
4. **4-Second Rate Limiting**: Mandatory delay before embedding to stay under 15 RPM limit

### Technology Stack

- **Backend**: Python 3.8+
- **Vector Database**: Pinecone (Serverless)
- **Embeddings**: Google Gemini (`text-embedding-004`)
- **UI**: Streamlit
- **Data Processing**: Custom preprocessing pipeline

## API Usage & Costs

### Google Gemini API (Free Tier)
- **Embedding Model**: `text-embedding-004`
- **Rate Limit**: 15 requests per minute
- **Daily Limit**: ~1,500 requests
- **Cost**: Free

### Pinecone (Free Tier)
- **Index**: Serverless (us-east-1)
- **Vectors**: 464 documents
- **Dimensions**: 768
- **Cost**: Free

## Testing

### Run All Tests
```bash
# Integration tests
python tests/test_rag_integration.py

# Single query test
python tests/test_rag_single.py

# Pinecone verification
python tests/test_phase5_pinecone.py

# Embeddings verification
python tests/test_embeddings.py
```

### Test Coverage
- Query processing (filter extraction)
- Vector retrieval
- Context building
- Response formatting
- End-to-end pipeline
- Out-of-domain handling

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for AWS deployment instructions.

## Troubleshooting

### Common Issues

**1. "ImportError: cannot import name 'genai'"**
- Solution: Install `google-genai` package
  ```bash
  pip install google-genai
  ```

**2. "Exception: pinecone-client renamed to pinecone"**
- Solution: Uninstall old package and install new one
  ```bash
  pip uninstall pinecone-client -y
  pip install pinecone
  ```

**3. "429 RESOURCE_EXHAUSTED" errors**
- Solution: The 4-second delay should prevent this. If it persists, wait for quota reset.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License

## Contact

For questions or issues, please open a GitHub issue.
