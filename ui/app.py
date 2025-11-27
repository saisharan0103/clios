import streamlit as st
import time
import sys
import os

# Add project root to path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.rag.chat_handler import chat

# Page Config
st.set_page_config(
    page_title="Clio Awards Chatbot",
    page_icon="📋",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #f0f2f6;
    }
    .source-box {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
        margin-top: 5px;
        font-size: 0.9em;
    }
    .metadata-tag {
        display: inline-block;
        background-color: #e1e4e8;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        margin-right: 5px;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("Clio Awards Assistant")
st.markdown("Ask me about Clio Awards winners, jury members, and events.")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_processing_time" not in st.session_state:
    st.session_state.last_processing_time = None

if "last_filters" not in st.session_state:
    st.session_state.last_filters = {}

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This chatbot uses **RAG (Retrieval-Augmented Generation)** to answer questions about the Clio Awards.
    
    **Data Source:**
    - Clio Awards Website (Winners, Jury, Events)
    - Pinecone Vector Database
    
    **Tech Stack:**
    - Google Gemini (Embeddings)
    - Pinecone (Vector Search)
    - Streamlit (UI)
    """)
    
    st.divider()
    
    st.subheader("Performance")
    if st.session_state.last_processing_time:
        st.metric("Processing Time", f"{st.session_state.last_processing_time}s")
    else:
        st.info("Ask a question to see stats.")
        
    if st.session_state.last_filters:
        st.subheader("Filters Applied")
        st.json(st.session_state.last_filters)

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # If there are sources in the message metadata, show them
        if "sources" in message and message["sources"]:
            with st.expander("📚 View Sources"):
                for i, source in enumerate(message["sources"], 1):
                    st.markdown(f"**{i}. [{source['title']}]({source.get('url', '#')})**")
                    
                    # Metadata tags
                    meta = []
                    if source.get('year'): meta.append(f"Year: {source['year']}")
                    if source.get('category'): meta.append(f"Category: {source['category']}")
                    if source.get('page_type'): meta.append(f"Type: {source['page_type']}")
                    
                    if meta:
                        st.markdown(f"<div style='margin-bottom:5px'>{' '.join([f'<span class=metadata-tag>{m}</span>' for m in meta])}</div>", unsafe_allow_html=True)
                    
                    st.markdown(f"_{source.get('excerpt', '')[:200]}..._")
                    st.divider()

# Chat Input
if prompt := st.chat_input("Ex: Who won Clio Sports 2025?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Searching Clio database..."):
            # Call Chat Handler
            response = chat(prompt)
            
            # Update Session State Stats
            st.session_state.last_processing_time = response.get("processing_time", 0)
            st.session_state.last_filters = response.get("filters_used", {})
            
            # Display Answer
            st.markdown(response["answer"])
            
            # Display Sources
            sources = response.get("sources", [])
            if sources:
                with st.expander("📚 View Sources"):
                    for i, source in enumerate(sources, 1):
                        st.markdown(f"**{i}. [{source['title']}]({source.get('url', '#')})**")
                        
                        meta = []
                        if source.get('year'): meta.append(f"Year: {source['year']}")
                        if source.get('category'): meta.append(f"Category: {source['category']}")
                        if source.get('page_type'): meta.append(f"Type: {source['page_type']}")
                        
                        if meta:
                            st.markdown(f"<div style='margin-bottom:5px'>{' '.join([f'<span class=metadata-tag>{m}</span>' for m in meta])}</div>", unsafe_allow_html=True)
                        
                        st.markdown(f"_{source.get('excerpt', '')[:200]}..._")
                        if i < len(sources):
                            st.divider()
            
            # Add assistant message to history (with sources for persistence)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response["answer"],
                "sources": sources
            })
            
            # Force rerun to update sidebar stats immediately
            st.rerun()
