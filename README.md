# AI PDF Knowledge Assistant

A local, privacy-first Retrieval-Augmented Generation (RAG) application for querying enterprise PDF documents. Built on Clean Architecture and SOLID principles, it runs entirely on local infrastructure using Ollama and ChromaDB — no document content ever leaves the machine.

---

## Features

### AI & RAG
- **Local LLM inference** via Ollama (Llama 3) — no external API calls.
- **Semantic search** over document chunks using HuggingFace SentenceTransformers embeddings.
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
| ![Initial state — dark theme](docs/screenshot-dark-initial.png) <br> Initial dashboard state (dark theme) with a PDF uploaded and indexed | ![Chat with citations](docs/screenshot-chat.png) <br> Conversational Q&A over an indexed document, including a follow-up query |
| ![Upload panel — dark theme](docs/screenshot-upload-dark.png) <br> Upload panel before indexing (dark theme) | ![Upload panel — light theme](docs/screenshot-upload-light.png) <br> Same panel in light theme |
| ![Backend infrastructure call](docs/screenshot-backend-call.png) <br> Backend infrastructure invocation during a query | ![Session with chat history](docs/screenshot-session.png) <br> Active session with indexed chunks and chat history controls |

> Screenshot files are referenced from a `docs/` folder for illustration. Replace the paths above with the actual location of your image assets in the repository.

---

## Architecture

The application follows **Clean Architecture**: dependencies point inward, business logic is isolated from frameworks, and infrastructure details (the vector store, the LLM provider) are implementation details that can be swapped without touching core logic.

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

**Presentation layer** (`presentation/`) — Renders the custom Streamlit UI, handles user input, and displays results, metrics, and citations. Contains no business logic.

**Core / domain layer** (`core/`) — Defines interfaces, models, and use cases (e.g. "index a document," "answer a query"). Pure Python, framework-agnostic, and independently testable.

**Infrastructure layer** (`infrastructure/`) — Concrete implementations of the core interfaces: LangChain-based document loaders and splitters, the ChromaDB vector store client, and the Ollama LLM client.

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

1. **Upload PDF** — The user uploads one or more PDF files through the sidebar.
2. **Extract Text** — Text is extracted from the PDF using `pypdf`.
3. **Split Documents** — Extracted text is chunked using LangChain text splitters to produce retrieval-sized segments.
4. **Generate Embeddings** — Each chunk is embedded using a HuggingFace SentenceTransformers model.
5. **Store in ChromaDB** — Embeddings and their source metadata are persisted to a local ChromaDB collection.
6. **Similarity Search** — At query time, the user's question is embedded and the Top-K most similar chunks are retrieved.
7. **LLM Response** — Retrieved chunks are passed as context to the local Ollama (Llama 3) model, which generates a grounded answer.
8. **Citations** — The response is returned alongside the source chunks it was generated from.

---

## Project Structure

```
AI-PDF-Assistant/
├── app.py                 # Streamlit application entry point
├── config.py               # Application configuration
├── database.py             # Persistence layer (enterprise.db)
├── vector_store.py         # ChromaDB vector store integration
├── core/                   # Domain layer: interfaces, models, use cases
├── infrastructure/         # Concrete implementations (LangChain, ChromaDB, Ollama)
├── presentation/           # Streamlit UI (custom CSS/HTML dashboard)
├── settings/               # User/application settings management
├── utils/                  # Shared helper utilities
├── assets/                 # Static assets (styles, images, fonts)
├── documents/              # Uploaded source PDF documents
├── embeddings/             # Local embedding artifacts
├── chat_history/           # Persisted chat sessions
├── logs/                   # application.log, error.log, embedding.log
├── enterprise.db           # Local database file
├── Dockerfile              # Container build definition
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (not committed)
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
| langchain-community / langchain-core | LangChain core and community integrations |
| langchain-text-splitters | Document chunking |
| langchain-huggingface | HuggingFace embedding integration |
| langchain-ollama | Ollama LLM integration |
| ChromaDB | Local vector database for embedding storage and similarity search |
| sentence-transformers | Embedding model backend |
| pypdf | PDF text extraction |
| python-dotenv | Environment variable management |
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

1. **Clone the repository**

```bash
git clone https://github.com/<your-username>/AI-PDF-Assistant.git
cd AI-PDF-Assistant
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
.\venv\Scripts\activate      # Windows
source venv/bin/activate     # macOS / Linux
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root with any required configuration values (e.g. model names, log paths).

5. **Run the application**

```bash
streamlit run app.py
```

---

## Usage

1. **Upload PDFs** — Use the "Upload PDFs" panel in the sidebar to add one or more documents.
2. **Process Documents** — Click **Process PDFs** to extract, chunk, embed, and index the documents into ChromaDB.
3. **Ask Questions** — Enter a question in the chat input. The assistant retrieves the most relevant chunks and generates an answer using the local LLM.
4. **Review Citations** — Each response is grounded in the retrieved source chunks, allowing the answer to be traced back to the original document content.

---

## Design Principles

- **SOLID** — Each component has a single, well-defined responsibility; interfaces are used so that infrastructure implementations can be extended or replaced without modifying dependent code.
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

## License

This project is licensed under the [MIT License](LICENSE).
