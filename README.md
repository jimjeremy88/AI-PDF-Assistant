<div align="center">

# AI PDF Knowledge Assistant

**A local, privacy-first Retrieval-Augmented Generation (RAG) application for querying enterprise PDF documents.**

Built on Clean Architecture and SOLID Principles, it runs entirely on local infrastructure using Ollama and ChromaDB — no document content ever leaves the machine.

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG%20Orchestration-1C3C3C)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-6A5ACD)](https://www.trychroma.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Llama%203-000000?logo=ollama&logoColor=white)](https://ollama.com/)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20Architecture-blue)](#architecture)
[![Status](https://img.shields.io/badge/Status-Active-success)](#)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)

</div>

---

## Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Architecture](#architecture)
- [RAG Pipeline](#rag-pipeline)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Design Principles](#design-principles)
- [Enterprise Features](#enterprise-features)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [Security](#security)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [License](#license)

---

## Features

### AI & RAG
- **Local LLM inference** via Ollama (Llama 3) — no external API calls.
- **Semantic search** over document chunks using SentenceTransformers embeddings.
- **Vector storage and retrieval** powered by ChromaDB.
- **Configurable retrieval** — adjustable Top-K results and LLM temperature at query time.
- **Source-grounded answers** with citations tied back to the original document.

### User Experience
- **Custom Streamlit dashboard** with a fully overridden CSS/HTML presentation layer (default Streamlit styling removed).
- **Live indexing metrics** — indexed chunk count and total query count displayed in real time.
- **Dark and light themes**, switchable from the settings panel.
- **Multi-file PDF upload** with per-file size display and drag-and-drop support.
- **Conversational follow-ups** — the assistant retains context across a chat session (e.g. "more details" on a prior answer).
- **Chat management** — clear chat history and start a new session at any point.

### Enterprise Features
- **Local-first processing** — documents, embeddings, and chat history never leave the host machine.
- **Environment-based configuration** via `.env` and `config.py`.
- **Structured logging** — distinct log streams for application, error, and embedding events.
- **Persistent storage** — indexed data and enterprise records persisted via `database.py` and `enterprise.db`.
- **Graceful error handling** throughout the ingestion and query pipeline.

### Architecture
- **Clean Architecture** with strict separation between presentation, domain, and infrastructure layers.
- **Dependency Injection** — infrastructure implementations are injected into core use cases rather than imported directly.
- **Framework-isolated core** — business logic in `core/` has no dependency on Streamlit, LangChain, or ChromaDB internals.

---

## Screenshots

| | |
|---|---|
| <img width="800" alt="Initial dashboard state" src="https://github.com/user-attachments/assets/12d5a8ed-ecd5-40b3-84db-1b22216e8c9d" /> <br> **Initial dashboard state** — a PDF uploaded and indexed, ready for questions | <img width="800" alt="Conversational Q&A with citations" src="https://github.com/user-attachments/assets/d617e5a9-120d-4d0d-8ac6-e4281a040a4c" /> <br> **Conversational Q&A** — a follow-up query answered using retained chat context |
| <img width="800" alt="Upload panel, dark theme" src="https://github.com/user-attachments/assets/cdc0b102-fd69-45c8-a65b-861c0138704c" /> <br> **Upload panel (dark theme)** — before document indexing | <img width="800" alt="Upload panel, light theme" src="https://github.com/user-attachments/assets/cdbb8ef0-c6ce-40af-b643-57649708d147" /> <br> **Upload panel (light theme)** — the same view with the light theme applied |
| <img width="800" alt="Backend infrastructure call in progress" src="https://github.com/user-attachments/assets/b52d0e69-06c8-418f-b393-3dafdf9e7ba6" /> <br> **Backend infrastructure call** — retrieval and inference in progress during a query | <img width="800" alt="Active session with chat history controls" src="https://github.com/user-attachments/assets/63fc988c-0d2a-4193-bb09-13514fae3554" /> <br> **Active session** — indexed chunk count alongside chat history controls |

---

## Architecture

The application follows **Clean Architecture**: dependencies point inward, business logic is isolated from frameworks, and infrastructure details — the vector store, the LLM provider — are treated as replaceable implementation details rather than core assumptions.

```
                          User
                           │
                           ▼
                    Streamlit UI
                  (presentation/)
                           │
                           ▼
                  Application Layer
                      (core/)
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
         Embedding                 LLM Service
        (infrastructure/)         (infrastructure/)
              │                         │
              ▼                         ▼
          ChromaDB                   Ollama
```

| Layer | Location | Responsibility |
|---|---|---|
| **Presentation** | `presentation/` | Renders the custom Streamlit UI, handles user input, and displays results, metrics, and citations. Contains no business logic. |
| **Core / Domain** | `core/` | Defines interfaces, models, and use cases (e.g. "index a document," "answer a query"). Pure Python, framework-agnostic, and independently testable. |
| **Infrastructure** | `infrastructure/` | Concrete implementations of the core interfaces: LangChain-based document loaders and splitters, the ChromaDB vector store client, and the Ollama LLM client. |

This separation means the embedding model, vector database, or LLM provider can be replaced by implementing the corresponding interface in `infrastructure/`, without modifying `core/` or `presentation/`.

---

## RAG Pipeline

```
   Upload PDF
        │
        ▼
   Extract Text
        │
        ▼
  Split Documents
        │
        ▼
Generate Embeddings
        │
        ▼
 Store in ChromaDB
        │
        ▼
 Similarity Search
        │
        ▼
   LLM Response
        │
        ▼
    Citations
```

| Step | Description |
|---|---|
| **1. Upload PDF** | The user uploads one or more PDF files through the sidebar. |
| **2. Extract Text** | Text is extracted from the PDF using `pypdf`. |
| **3. Split Documents** | Extracted text is chunked using LangChain text splitters into retrieval-sized segments. |
| **4. Generate Embeddings** | Each chunk is embedded using a SentenceTransformers model. |
| **5. Store in ChromaDB** | Embeddings and their source metadata are persisted to a local ChromaDB collection. |
| **6. Similarity Search** | At query time, the user's question is embedded and the Top-K most similar chunks are retrieved. |
| **7. LLM Response** | Retrieved chunks are passed as context to the local Ollama (Llama 3) model, which generates a grounded answer. |
| **8. Citations** | The response is returned alongside the source chunks it was generated from. |

---

## Project Structure

```
AI-PDF-Assistant/
├── app.py               # Streamlit application entry point
├── config.py             # Application configuration
├── database.py           # Persistence layer (enterprise.db)
├── vector_store.py       # ChromaDB vector store integration
├── core/                 # Domain layer: interfaces, models, use cases
├── infrastructure/       # Concrete implementations (LangChain, ChromaDB, Ollama)
├── presentation/         # Streamlit UI (custom CSS/HTML dashboard)
├── settings/             # User/application settings management
├── utils/                # Shared helper utilities
├── assets/               # Static assets (styles, images, fonts)
├── documents/            # Uploaded source PDF documents
├── embeddings/            # Local embedding artifacts
├── chat_history/          # Persisted chat sessions
├── logs/                  # application.log, error.log, embedding.log
├── enterprise.db          # Local database file
├── Dockerfile             # Container build definition
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (not committed)
```

| Folder / File | Responsibility |
|---|---|
| `app.py` | Bootstraps and runs the Streamlit application. |
| `config.py` | Centralized application configuration and environment loading. |
| `database.py` | Data access layer for persisted application state. |
| `vector_store.py` | Wrapper around the ChromaDB client used for indexing and retrieval. |
| `core/` | Framework-agnostic interfaces, domain models, and use cases. |
| `infrastructure/` | Adapters implementing core interfaces using LangChain, ChromaDB, and Ollama. |
| `presentation/` | Streamlit UI components and custom styling. |
| `settings/` | Application and user-configurable settings. |
| `utils/` | Shared, cross-cutting helper functions. |
| `assets/` | Static files used by the UI (CSS, fonts, images). |
| `documents/` | Storage location for uploaded PDF files. |
| `embeddings/` | Local storage for generated embedding data. |
| `chat_history/` | Saved conversation sessions. |
| `logs/` | Structured application, error, and embedding logs. |

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.9+ | Core application language |
| Streamlit | Web UI framework |
| LangChain | Document loading, text splitting, and RAG orchestration |
| `langchain-community` / `langchain-core` | LangChain core and community integrations |
| `langchain-text-splitters` | Document chunking |
| `langchain-huggingface` | SentenceTransformers embedding integration |
| `langchain-ollama` | Ollama LLM integration |
| ChromaDB | Local vector database for embedding storage and similarity search |
| SentenceTransformers | Embedding model backend |
| `pypdf` | PDF text extraction |
| `python-dotenv` | Environment variable management |
| Ollama (Llama 3) | Local large language model inference |

---

## Prerequisites

- Python 3.9 or later
- [Ollama](https://ollama.com/) installed and running locally
- The `llama3` model pulled in Ollama:

```bash
ollama pull llama3
```

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/AI-PDF-Assistant.git
cd AI-PDF-Assistant
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
.\venv\Scripts\activate      # Windows
source venv/bin/activate     # macOS / Linux
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root with any required configuration values (e.g. model names, log paths).

**5. Run the application**

```bash
streamlit run app.py
```

---

## Quick Start

For readers who want the shortest path from clone to a working assistant:

```bash
git clone https://github.com/<your-username>/AI-PDF-Assistant.git
cd AI-PDF-Assistant
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
ollama pull llama3
streamlit run app.py
```

Then open the local Streamlit URL, upload a PDF, click **Process PDFs**, and start asking questions.

---

## Usage

1. **Upload PDFs** — Use the "Upload PDFs" panel in the sidebar to add one or more documents.
2. **Process Documents** — Click **Process PDFs** to extract, chunk, embed, and index the documents into ChromaDB.
3. **Ask Questions** — Enter a question in the chat input. The assistant retrieves the most relevant chunks and generates an answer using the local LLM.
4. **Review Citations** — Each response is grounded in the retrieved source chunks, allowing the answer to be traced back to the original document content.

---

## Design Principles

- **SOLID Principles** — Each component has a single, well-defined responsibility; interfaces are used so that infrastructure implementations can be extended or replaced without modifying dependent code.
- **Clean Architecture** — Business logic in `core/` has no knowledge of Streamlit, LangChain, or ChromaDB; all framework-specific code lives in `infrastructure/` and `presentation/`.
- **Dependency Injection** — Core use cases depend on abstractions defined in `core/`, with concrete implementations supplied from `infrastructure/` at runtime.
- **Separation of Concerns** — UI rendering, business logic, and data access are kept in distinct layers, which keeps each layer independently testable and maintainable.

---

## Enterprise Features

- **Local-first processing** — All document ingestion, embedding, and inference happen on-device; no data is sent to third-party APIs.
- **Privacy** — Uploaded documents, embeddings, and chat history remain within the local file system and database.
- **Error handling** — Ingestion and query operations fail gracefully with informative feedback rather than uncaught exceptions.
- **Logging** — Application, error, and embedding events are logged separately for easier diagnosis.
- **Modular architecture** — Clean separation between layers allows individual components to be modified or replaced in isolation.
- **Extensibility** — New embedding models, vector stores, or LLM providers can be added by implementing the corresponding interface in `infrastructure/`.

---

## Troubleshooting

| Issue | Likely Cause | Resolution |
|---|---|---|
| `ConnectionError` when asking a question | Ollama is not running | Start Ollama and confirm `llama3` is available via `ollama list` |
| Model not found | The `llama3` model was not pulled | Run `ollama pull llama3` |
| Slow first response | Model is loading into memory on first call | Subsequent queries will be faster once the model is warm |
| PDF upload fails silently | Unsupported or corrupted PDF | Verify the file opens correctly in a standard PDF viewer before uploading |
| No citations returned | Documents have not been processed yet | Click **Process PDFs** after uploading, before asking questions |
| Dependency install errors | Python version mismatch | Confirm Python 3.9+ is active in the virtual environment |

> If an issue is not listed here, check `logs/application.log` and `logs/error.log` for details.

---

## Future Improvements

The following are planned enhancements and are **not currently implemented**:

- Hybrid search combining BM25 and vector similarity
- Cross-encoder re-ranking of retrieved chunks
- Streaming LLM responses
- Support for multiple document collections
- Finalized Docker-based deployment
- User authentication
- REST API for programmatic access
- Persistent conversation memory across sessions

---

## Security

- All processing runs locally; no document content, embeddings, or chat data is transmitted to external services.
- Configuration secrets are managed via `.env` and are excluded from version control.
- If you discover a security issue, please open a private report or contact the maintainer directly rather than filing a public issue.

---

## Contributing

Contributions are welcome. To propose a change:

1. Fork the repository and create a feature branch.
2. Follow the existing Clean Architecture boundaries — keep `core/` framework-agnostic.
3. Ensure new infrastructure integrations implement the corresponding interface in `core/`.
4. Open a pull request with a clear description of the change and its motivation.

---

## Acknowledgements

- [LangChain](https://www.langchain.com/) for RAG orchestration primitives.
- [ChromaDB](https://www.trychroma.com/) for local vector storage.
- [Ollama](https://ollama.com/) for local LLM inference.
- [Streamlit](https://streamlit.io/) for the application UI framework.
- [SentenceTransformers](https://www.sbert.net/) for embedding generation.

---

## License

This project is licensed under the [MIT License](LICENSE).
