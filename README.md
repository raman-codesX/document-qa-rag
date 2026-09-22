# Document Q&A with Citations

A Retrieval-Augmented Generation (RAG) based document question-answering system that allows users to ask questions about their documents and receive answers with traceable source citations.

The system retrieves relevant information from documents before generating an answer, making the responses more transparent and easier to verify.

---

## Features

- PDF document support
- DOCX document support
- TXT document support
- Markdown document support
- Automatic document extraction
- Text chunking
- FAISS semantic search
- BM25 keyword search
- Hybrid retrieval
- Cross-Encoder reranking
- Gemini-based answer generation
- Source citations
- Retrieved passage display
- Streamlit user interface

---

## Architecture

```text
Document
   ↓
Document Extraction
   ↓
Text Chunking
   ↓
 ┌───────────────────────┐
 │                       │
FAISS                  BM25
 │                       │
 └──────────┬────────────┘
            ↓
     Hybrid Retrieval
            ↓
    Cross-Encoder Reranking
            ↓
      Top Relevant Chunks
            ↓
          Gemini
            ↓
    Answer + Citations
How It Works
1. Document Extraction

The system accepts multiple document formats:

PDF
DOCX
TXT
MD

The document content is extracted and converted into a common format containing:

text
source
location

For example:

{
    "text" : "...",
    "source" : "inspection_report.pdf",
    "location" : "page 1"
}
2. Text Chunking

Large documents are divided into smaller chunks so that relevant information can be retrieved efficiently.

The current configuration uses:

Chunk Size    : 500
Chunk Overlap : 50

Each chunk also stores its source and location.

3. FAISS Semantic Search

The system uses:

all-MiniLM-L6-v2

to convert text into vector embeddings.

FAISS is then used to find semantically similar document chunks for a user's question.

4. BM25 Keyword Search

BM25 provides keyword-based retrieval.

This helps when the query contains important terms that should match directly with the document.

5. Hybrid Retrieval

The system combines candidates retrieved by:

FAISS + BM25

This provides both:

Semantic matching
Keyword matching

The combined results are then passed to the reranking stage.

6. Cross-Encoder Reranking

A Cross-Encoder is used to compare the question with the retrieved chunks and rank them based on relevance.

Model:

cross-encoder/ms-marco-MiniLM-L-6-v2

The most relevant chunks are selected as the final context.

7. Answer Generation

The selected context is provided to Gemini along with the user's question.

The model generates an answer using the retrieved document information.

8. Citations

The system also identifies supporting evidence from the retrieved content.

The final response displays the source document and location so that the user can trace the answer back to the original document.

Task 2 — RAG Evaluation Suite

The second task evaluates the retrieval performance of the RAG system.

Instead of only testing the system manually, a separate evaluation dataset was created to measure whether the correct source page is retrieved for a given question.

Evaluation Dataset

The evaluation uses a 50-page document containing different AI and RAG concepts.

Document       : rag_evaluation_50_pages.pdf
Pages          : 50
Questions      : 20

Each evaluation question has a predefined expected source page.

Example:

Question:
What is FAISS used for?

Expected Source:
rag_evaluation_50_pages.pdf
page 25
Evaluation Process

For every question:

Question
   ↓
Query Embedding
   ↓
FAISS Search
   +
BM25 Search
   ↓
Hybrid Retrieval
   ↓
Cross-Encoder Reranking
   ↓
Top Results
   ↓
Compare With Expected Source

The evaluation checks whether the expected source page appears in the retrieved results.

Evaluation Metrics
Hit@3

Hit@3 checks whether the expected source appears within the top 3 retrieved results.

Hit@3 =
Questions where expected source is in top 3
--------------------------------------------
Total Questions
Hit@5

Hit@5 checks whether the expected source appears within the top 5 retrieved results.

Hit@5 =
Questions where expected source is in top 5
--------------------------------------------
Total Questions
Evaluation Results

The RAG system was evaluated using 20 questions.

Metric	Result
Total Questions	20
Hit@3 Hits	20
Hit@3 Misses	0
Hit@3	100.00%
Hit@5 Hits	20
Hit@5 Misses	0
Hit@5	100.00%
Interpretation

The system achieved:

Hit@3 = 100.00%
Hit@5 = 100.00%

This means that for all 20 evaluation questions, the expected source page was retrieved within the top 3 and top 5 results.

This result measures retrieval performance.

It does not mean that the generated answers are 100% accurate.

Evaluation Files
evaluation/
├── questions.json
└── evaluation.py
questions.json

Contains:

Evaluation questions
Expected answers
Expected source document
Expected source location
evaluation.py

Runs the retrieval evaluation and calculates:

Hit@3
Hit@5
Running the Evaluation

From the project root:

python evaluation/evaluation.py

Example output:

==============================

Total Questions : 20

Hit@3 Hits      : 20
Hit@3 Misses    : 0
Hit@3           : 100.00%

Hit@5 Hits      : 20
Hit@5 Misses    : 0
Hit@5           : 100.00%

==============================
Evaluation Limitation

The current evaluation focuses on retrieval performance.

Answer correctness and faithfulness require a separate evaluation of the generated responses.

A Gemini-based answer evaluation was tested, but the evaluation could not be completed across the full dataset because of API quota limitations.

Therefore, the final reported evaluation results are based only on the completed retrieval evaluation.

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
Tech Stack
Python
Streamlit
PyMuPDF
python-docx
LangChain Text Splitters
Sentence Transformers
FAISS
BM25
Cross-Encoder
Google Gemini API
Installation

Clone the repository:

git clone https://github.com/raman-codesX/document-qa-rag.git

Go to the project directory:

cd document-qa-rag

Install dependencies:

pip install -r requirements.txt
Environment Variables

Create a .env file:

GEMINI_API_KEY=your_api_key_here

Do not commit the .env file to GitHub.

Run the Application

Start the Streamlit application:

streamlit run app.py --server.fileWatcherType none

The application will open in the browser.

Example Workflow
Upload Document
      ↓
Extract Text
      ↓
Create Chunks
      ↓
Build FAISS + BM25
      ↓
Ask Question
      ↓
Retrieve Relevant Chunks
      ↓
Rerank Results
      ↓
Generate Answer
      ↓
Show Answer + Citations
Future Improvements
Automated answer correctness evaluation
Faithfulness evaluation
Better citation extraction
Retrieval score visualization
Response caching
Query rewriting
Support for larger document collections
Evaluation dashboard
Author

Raman

GitHub:

https://github.com/raman-codesX
