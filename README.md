# Enterprise AI PDF Knowledge Assistant

A completely customized, production-grade, local RAG application built strictly upon **SOLID Principles** and **Clean Architecture**. This application features zero-telemetry local processing, a responsive custom CSS dashboard, and graceful error handling.

# Overview
Upload PDF documents, index them locally, and interact securely using Ollama (Llama 3) and ChromaDB. Engineered for resilience and scale.

# Features
- **Dashboard Metrics:** Real-time tracking of Indexed Chunks, LLM models, and Average Response Time.
- **Advanced Citations:** Every answer explicitly lists the Source File, Page Number, and a calculated Similarity Percentage.
- **PDF Highlight Preview:** Click citations to view exact extracted document text marked up and highlighted.
- **Premium Custom UI:** Rounded cards, modern typography (Inter font), smooth typing animations, and professional spacing. (Streamlit defaults completely removed).
- **Chat Actions:** Regenerate responses, Clear History, and Export Chat to Markdown or PDF.
- **Enterprise Resilience:** Graceful error handling, environment variables (`.env`), input validation, and distinct logging (`application.log`, `error.log`, `embedding.log`).

# Architecture
Implemented using strict Clean Architecture (Dependency Injection, DTOs, and isolated layers).

1. **Presentation:** Streamlit custom UI (`presentation/ui.py`).
2. **Core / Domain:** Interfaces, Models, and pure Python Use Cases (`core/`).
3. **Infrastructure:** Concrete classes interacting with LangChain, Chroma, and Ollama (`infrastructure/`).

# Technology Stack
- **Language:** Python 3.9+ (Strict Type Hints, PEP8)
- **Frontend:** Streamlit (Overridden with raw CSS/HTML)
- **Framework:** LangChain
- **Vector Database:** ChromaDB
- **LLM:** Ollama (Llama3)
- **Embeddings:** HuggingFace SentenceTransformers

# Installation & Configuration

1. Clone repository and setup environment:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt