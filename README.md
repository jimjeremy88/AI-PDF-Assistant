# Enterprise AI PDF Knowledge Assistant

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-FD6F31?logo=chroma&logoColor=white)](https://www.trychroma.com/)
[![Ollama](https://img.shields.io/badge/Ollama-000000?logo=ollama&logoColor=white)](https://ollama.ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A customized, production-grade, local Retrieval-Augmented Generation (RAG) application built strictly upon **SOLID Principles** and **Clean Architecture**. This application features zero-telemetry local processing, a responsive custom CSS dashboard, and robust error handling. Upload PDF documents, index them locally, and interact securely using Ollama (Llama 3) and ChromaDB. Engineered for resilience and scale.

## Table of Contents
- [Features](#features)
- [Screenshots](#screenshots)
- [System Architecture](#system-architecture)
- [RAG Pipeline](#rag-pipeline)
- [Design Principles](#design-principles)
- [Security & Privacy](#security--privacy)
- [Performance](#performance)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation & Configuration](#installation--configuration)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Local PDF RAG:** Fully offline processing and inference using local vector databases and language models.
- **Advanced Citations & Highlight Preview:** Every answer explicitly lists the source file, page number, and similarity percentage. Click citations to view the exact extracted document text marked up and highlighted.
- **Dashboard Metrics:** Real-time tracking of indexed chunks, active LLM models, and average response times.
- **Premium Custom UI:** Rounded cards, modern typography, smooth typing animations, and professional spacing, completely overriding default Streamlit styling. Includes Dark/Light theme toggles.
- **Chat Actions:** Built-in functionality to regenerate responses, clear chat history, and export conversations to Markdown or PDF.
- **Enterprise Resilience:** Graceful error handling, robust input validation, environment variable management (`.env`), and distinct layer logging (`application.log`, `error.log`, `embedding.log`).

---

## Screenshots

| Dark Theme Dashboard | Light Theme Dashboard |
|:---:|:---:|
| ![Dashboard Dark](assets/dashboard-dark.png) | ![Dashboard Light](assets/dashboard-light.png) |

| Upload | Processing |
|:---:|:---:|
| ![Upload](assets/upload.png) | ![Processing](assets/processing.png) |

| Chat | Citation |
|:---:|:---:|
| ![Chat](assets/chat.png) | ![Citation](assets/citation.png) |

---

## System Architecture

The application is decoupled into distinct layers to isolate external frameworks from core business logic, adhering to Clean Architecture.

```mermaid
graph LR
    User([User]) --> UI[Streamlit UI]
    UI --> UC[Use Cases]
    UC --> Domain[Domain Models]
    UC --> Infra[Infrastructure]
    Infra --> ChromaDB[(ChromaDB)]
    Infra --> HF[SentenceTransformers]
    Infra --> Ollama[[Ollama / Llama3]]
