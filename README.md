# RAG-Powered Document Assistant - Data Structures & Algorithms

A complete Retrieval-Augmented Generation (RAG) web application: ask questions about **Data Structures & Algorithms** (Stacks, Queues, Binary Trees, BSTs, Huffman Coding, Sorting Algorithms) and receive grounded, cited answers powered by ChromaDB vector search, FastAPI backend, and local Ollama LLM (`llama3.2`).

## Overview

- **Domain:** Data Structures & Algorithms (Unit I: Stacks & Queues; Unit III: Trees & Huffman Coding; Unit IV: Sorting Algorithms).
- **Track:** Core Track (Text-based Document RAG Assistant with grounded source citations).
- **Pipeline:** Raw source documents (`dsa_unit1_stacks_queues.txt`, `dsa_unit3_trees_huffman.txt`, `dsa_unit4_sorting_algorithms.txt`) → Character chunking with overlap → Dense vector embeddings (`all-MiniLM-L6-v2`) → ChromaDB vector store → Similarity retrieval (`top_k=4`) → Ollama LLM / Context-grounded synthesis → Grounded response with citations via FastAPI & Streamlit UI.

## Architecture

```
┌─────────────────┐      HTTP POST      ┌──────────────────┐      Similarity      ┌───────────────────┐
│   Streamlit     │ ───────────────────▶│     FastAPI      │ ───────────────────▶ │     ChromaDB      │
│   Frontend      │      /query         │     Backend      │       Search         │   Vector Store    │
│  (Port 8501)    │ ◀────────────────── │   (Port 8000)    │                      └───────────────────┘
└─────────────────┘      JSON Resp      └────────┬─────────┘                                │
                                                 │                                          │
                                                 ▼                                          ▼
                                        ┌──────────────────┐                       ┌───────────────────┐
                                        │    Ollama LLM    │                       │  Grounded Prompt  │
                                        │   (llama3.2)     │                       │  + Citations      │
                                        └──────────────────┘                       └───────────────────┘
```

## Tech Stack

- **Notebook:** Jupyter, pandas, sentence-transformers, chromadb
- **Backend:** FastAPI, Pydantic, pydantic-settings, ChromaDB, Ollama Python Client, pytest
- **Frontend:** Streamlit, requests, python-dotenv
- **LLM:** Local Ollama (`llama3.2`) with context-grounded fallback synthesizer
- **Vector Store:** ChromaDB (persisted to `backend/data/vector_store/`)

## Project Structure

```
rag-assistant-project/
├── data/
│   └── raw/                       # Source documents (dsa_unit1_stacks_queues.txt, dsa_unit3_trees_huffman.txt, dsa_unit4_sorting_algorithms.txt)
├── notebooks/
│   └── rag_pipeline.ipynb         # Data preparation, chunking, embeddings, retrieval, evaluation report
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI entry point, CORS middleware, lifespan loader
│   │   ├── api/routes/query.py    # GET /health, POST /query routes
│   │   ├── core/config.py         # App settings loaded via pydantic-settings
│   │   ├── schemas/query.py       # Pydantic schemas (QueryRequest, QueryResponse)
│   │   ├── services/
│   │   │   ├── retrieval.py       # Vector store loader & similarity search
│   │   │   └── generation.py      # Grounded prompt builder & Ollama LLM integration
│   │   └── utils/logging_config.py
│   ├── data/vector_store/         # Persisted ChromaDB collection & config.json
│   ├── tests/test_query.py        # Pytest suite with TestClient
│   ├── requirements.txt
│   ├── .env
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── app.py                     # Streamlit chat interface with sidebar status
│   ├── api_client.py              # Backend API wrapper
│   ├── .env                       # API_BASE_URL=http://localhost:8000
│   ├── .env.example
│   └── requirements.txt
├── .gitignore
└── README.md
```

## Setup & Running Instructions

### 1. Rebuild Vector Store

```bash
python run_pipeline_notebook.py
```

### 2. Run FastAPI Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 3. Run Streamlit Frontend

```bash
cd frontend
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

## API Reference

### `POST /query`

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How does a Stack work and what is LIFO?"}'
```

**Response:**
```json
{
  "answer": "A Stack is an abstract linear data type in which items are inserted and deleted at only one end, called the top of the stack...",
  "sources": [
    "dsa_unit1_stacks_queues.txt"
  ]
}
```
