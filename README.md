<img width="2879" height="1560" alt="Screenshot 2026-07-10 011753" src="https://github.com/user-attachments/assets/87ca7407-766a-4fab-ae85-52a4885ad403" />
<img width="2879" height="1592" alt="Screenshot 2026-07-10 013450" src="https://github.com/user-attachments/assets/3eaf9192-5411-46ea-988b-ef31cf80d3b0" />
<img width="2879" height="1623" alt="Screenshot 2026-07-10 013043" src="https://github.com/user-attachments/assets/40240f29-5e74-4873-a2af-2d48b6a94d15" />
<img width="2879" height="1622" alt="Screenshot 2026-07-10 012707" src="https://github.com/user-attachments/assets/7a7ec0fa-30f3-4491-87e5-2b9d6d86d292" />
<img width="2879" height="1616" alt="Screenshot 2026-07-10 012503" src="https://github.com/user-attachments/assets/5ee200de-58cb-496d-aad6-1a1395adaeef" />
<img width="2879" height="1563" alt="Screenshot 2026-07-10 011834" src="https://github.com/user-attachments/assets/ebf677a7-314f-4853-8890-d0a88ff0d933" />
# Enterprise AI PDF Knowledge Assistant

A completely customized, production-grade, local RAG application built strictly upon **SOLID Principles** and **Clean Architecture**. This application features zero-telemetry local processing, a responsive custom CSS dashboard, and graceful error handling.

---

## Overview

Upload PDF documents, index them locally, and interact securely using Ollama (Llama 3) and ChromaDB. Engineered for resilience and scale.

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

## Installation & Configuration

### 1. Clone repository and setup environment:

```bash
# Clone repositori (Sesuaikan dengan URL GitHub Anda)
git clone [https://github.com/jimjeremy88/nama-repositori.git](https://github.com/jimjeremy88/nama-repositori.git)
cd nama-repositori

# Membuat dan mengaktifkan virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
