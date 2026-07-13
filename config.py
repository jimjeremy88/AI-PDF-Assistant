import os
import logging
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

# Define the base directory first so it can be used below
_BASE = os.path.dirname(os.path.abspath(__file__))

@dataclass(frozen=True)
class AppConfig:
    """Immutable enterprise configuration object."""
    BASE_DIR: str = _BASE
    DB_DIR: str = os.path.join(_BASE, "embeddings")
    DOCS_DIR: str = os.path.join(_BASE, "documents")
    LOGS_DIR: str = os.path.join(_BASE, "logs")
    
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 200))
    TOP_K: int = int(os.getenv("TOP_K_RESULTS", 3))
    TEMP: float = float(os.getenv("TEMPERATURE", 0.2))

    default_system_prompt: str = (
        "You are a highly intelligent enterprise AI. "
        "Use ONLY the following context to answer the question. "
        "If the answer is not in the context, state that you do not know.\n\n"
        "Context:\n{context}"
    )

    def __post_init__(self):
        os.makedirs(self.DB_DIR, exist_ok=True)
        os.makedirs(self.DOCS_DIR, exist_ok=True)
        os.makedirs(self.LOGS_DIR, exist_ok=True)

CONFIG = AppConfig()