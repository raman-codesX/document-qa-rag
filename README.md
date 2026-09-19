# Document Q&A with Citations

A RAG-based document question-answering system that answers questions from uploaded documents and provides source citations for traceability.

## Features

- PDF, DOCX, TXT and Markdown support
- FAISS semantic search
- BM25 keyword search
- Hybrid retrieval
- Cross-Encoder reranking
- Gemini-based answers
- Source citations
- Streamlit UI

## Tech Stack

Python · Streamlit · FAISS · BM25 · Sentence Transformers · Cross-Encoder · Gemini

## Architecture

```text
Document
   ↓
Extraction → Chunking
   ↓
FAISS + BM25
   ↓
Reranking
   ↓
Gemini
   ↓
Answer + Citations
Run
pip install -r requirements.txt
streamlit run app.py --server.fileWatcherType none

Create a .env file:

GEMINI_API_KEY=your_api_key_here
Author

Raman
GitHub: https://github.com/raman-codesX
