from abc import ABC, abstractmethod
from typing import List
from core.models import DocumentChunk
from langchain_core.language_models.chat_models import BaseChatModel

class IDocumentLoader(ABC):
    @abstractmethod
    def load_and_split(self, file_paths: List[str]) -> List[DocumentChunk]: pass

class IVectorStore(ABC):
    @abstractmethod
    def store_documents(self, documents: List[DocumentChunk]) -> int: pass

    @abstractmethod
    def search_similar(self, query: str, top_k: int) -> List[DocumentChunk]: pass

    @abstractmethod
    def clear_database(self) -> None: pass
    
    @abstractmethod
    def get_document_count(self) -> int: pass

class ILLMProvider(ABC):
    @abstractmethod
    def get_model(self, temperature: float) -> BaseChatModel: pass