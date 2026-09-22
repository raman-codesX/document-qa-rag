# Document Q&A with Citations

A Retrieval-Augmented Generation (RAG) application that allows users to ask questions about documents and receive answers with traceable source citations.

## Features

- PDF, DOCX, TXT and Markdown support
- Automatic document extraction and chunking
- FAISS semantic search
- BM25 keyword search
- Hybrid retrieval
- Cross-Encoder reranking
- Gemini-based answer generation
- Source citations and retrieved passages
- Streamlit interface

## Architecture

```text
Document
   ↓
Extraction & Chunking
   ↓
FAISS + BM25
   ↓
Hybrid Retrieval
   ↓
Cross-Encoder Reranking
   ↓
Gemini
   ↓
Answer + Citations
Tech Stack
Python
Streamlit
PyMuPDF
Sentence Transformers
FAISS
BM25
Cross-Encoder
Google Gemini API
Task 2 — RAG Evaluation

The retrieval system was evaluated using a separate 50-page evaluation document containing 20 questions with predefined expected source pages.

Evaluation Results
Metric	Result
Questions	20
Hit@3	100.00%
Hit@5	100.00%

Hit@3 measures whether the expected source page appears in the top 3 retrieved results.

Hit@5 measures whether the expected source page appears in the top 5 retrieved results.

The system retrieved the expected source page within the top 3 and top 5 results for all 20 evaluation questions.

Note: These metrics evaluate retrieval performance and do not represent overall answer accuracy.

Project Structure
document-qa-rag/
│
├── app.py
├── main.py
├── README.md
├── .env.example
├── .gitignore
│
└── evaluation/
    ├── questions.json
    └── evaluation.py
Setup

Clone the repository:

git clone https://github.com/raman-codesX/document-qa-rag.git
cd document-qa-rag

Install dependencies:

pip install -r requirements.txt

Create a .env file:

GEMINI_API_KEY=your_api_key_here
Run

Start the application:

streamlit run app.py --server.fileWatcherType none

Run the retrieval evaluation:

python evaluation/evaluation.py
Author

Raman

GitHub: https://github.com/raman-codesX
