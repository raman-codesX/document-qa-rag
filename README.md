# Document Q&A with Citations

A RAG-based application for asking questions about documents and getting answers with references to the source content.

The project combines semantic search, keyword search, and reranking to retrieve relevant information before generating an answer.

## Features

- Supports PDF, DOCX, TXT, and Markdown files
- Document extraction and text chunking
- Semantic search with FAISS
- Keyword search with BM25
- Hybrid retrieval
- Cross-Encoder reranking
- Gemini for answer generation
- Source citations and retrieved passages
- Streamlit interface

## How It Works

```text
Document
   ↓
Text Extraction
   ↓
Chunking
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

The system first extracts and chunks the uploaded document. FAISS and BM25 are then used to find relevant chunks. The retrieved results are reranked using a Cross-Encoder before being passed to Gemini for answer generation.

Tech Stack-----
Python
Streamlit
PyMuPDF
python-docx
Sentence Transformers
FAISS
BM25
Cross-Encoder
Google Gemini API
Evaluation

As part of Task 2, the retrieval pipeline was evaluated using a separate 50-page document and 20 questions. Each question had a predefined expected source page.

Results
Metric	Result
Questions	20
Hit@3	100.00%
Hit@5	100.00%

The expected source page was retrieved within the top 3 results for all 20 questions. The same was true when considering the top 5 results.

Note: Hit@3 and Hit@5 measure retrieval performance. They do not represent the overall accuracy of the generated answers.

Evaluation files:

evaluation/
├── questions.json
└── evaluation.py
Project Structure
document-qa-rag/
├── app.py
├── main.py
├── README.md
├── .env.example
├── .gitignore
└── evaluation/
    ├── questions.json
    └── evaluation.py
Setup

Clone the repository:

git clone https://github.com/raman-codesX/document-qa-rag.git
cd document-qa-rag

Install the dependencies:

pip install -r requirements.txt

Create a .env file in the project directory:

GEMINI_API_KEY=your_api_key_here
Run

Start the application:

streamlit run app.py --server.fileWatcherType none

To run the retrieval evaluation:

python evaluation/evaluation.py
Limitations

The current evaluation focuses on retrieval performance. A separate evaluation of answer correctness and faithfulness would be needed to measure the quality of the generated responses.

Author

Raman

GitHub: https://github.com/raman-codesX
