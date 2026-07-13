# Enterprise AI PDF Knowledge Assistant

A completely customized, production-grade, local RAG application built strictly upon **SOLID Principles** and **Clean Architecture**. This application features zero-telemetry local processing, a responsive custom CSS dashboard, and graceful error handling.

---

## Overview

Upload PDF documents, index them locally, and interact securely using Ollama (Llama 3) and ChromaDB. Engineered for resilience and scale.

---

## Screenshots

**Dashboard — Dark Mode**
<img width="2879" height="1560" alt="Dashboard dark mode" src="https://github.com/user-attachments/assets/87ca7407-766a-4fab-ae85-52a4885ad403" />

**Dashboard — Light Mode**
<img width="2879" height="1563" alt="Dashboard light mode" src="https://github.com/user-attachments/assets/ebf677a7-314f-4853-8890-d0a88ff0d933" />

**PDF Upload & Indexing**
<img width="2879" height="1592" alt="PDF upload" src="https://github.com/user-attachments/assets/3eaf9192-5411-46ea-988b-ef31cf80d3b0" />

**RAG Pipeline Processing**
<img width="2879" height="1622" alt="RAG pipeline running" src="https://github.com/user-attachments/assets/7a7ec0fa-30f3-4491-87e5-2b9d6d86d292" />

**Indexing Verified**
<img width="2879" height="1616" alt="Indexing verified" src="https://github.com/user-attachments/assets/5ee200de-58cb-496d-aad6-1a1395adaeef" />

**Chat in Action**
<img width="2879" height="1623" alt="Chat response with citations" src="https://github.com/user-attachments/assets/40240f29-5e74-4873-a2af-2d48b6a94d15" />

---

## Features

* **Dashboard Metrics:** Real-time tracking of Indexed Chunks, LLM models, and Average Response Time.
* **Advanced Citations:** Every answer explicitly lists the Source File, Page Number, and a calculated Similarity Percentage.
* **PDF Highlight Preview:** Click citations to view exact extracted document text marked up and highlighted.
* **Premium Custom UI:** Rounded cards, modern typography (Inter font), smooth typing animations, and professional spacing. (Streamlit defaults completely removed).
* **Chat Actions:** Regenerate responses, Clear History, and Export Chat to Markdown or PDF.
* **Enterprise Resilience:** Graceful error handling, environment variables (`.env`), input validation, and distinct logging (`application.log`, `error.log`, `embedding.log`).

---

## Architecture

Implemented using strict Clean Architecture (Dependency Injection, DTOs, and isolated layers).

1. **Presentation:** Streamlit custom UI (`presentation/ui.py`).
2. **Core / Domain:** Interfaces, Models, and pure Python Use Cases (`core/`).
3. **Infrastructure:** Concrete classes interacting with LangChain, Chroma, and Ollama (`infrastructure/`).

---

## Technology Stack

* **Language:** Python 3.9+ (Strict Type Hints, PEP8)
* **Frontend:** Streamlit (Overridden with raw CSS/HTML)
* **Framework:** LangChain
* **Vector Database:** ChromaDB
* **LLM:** Ollama (Llama3)
* **Embeddings:** HuggingFace SentenceTransformers

---

## Prerequisites

> Requires [Ollama](https://ollama.com) installed locally with the `llama3` model pulled before running:
> ```bash
> ollama pull llama3
> ```

---

## Installation & Configuration

### 1. Clone repository and setup environment:

```bash
git clone https://github.com/jimjeremy88/AI-PDF-Assistant.git
cd AI-PDF-Assistant

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the application:

```bash
streamlit run app.py
```
