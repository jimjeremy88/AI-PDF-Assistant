import os
import shutil
import logging
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from core.interfaces import IVectorStore
from core.models import DocumentChunk
from config import CONFIG

embed_logger = logging.getLogger("embedding")

class ChromaVectorStore(IVectorStore):
    def __init__(self) -> None:
        self.persist_directory = CONFIG.vector_db_dir
        self.embeddings = HuggingFaceEmbeddings(
            model_name=CONFIG.embedding_model,
            model_kwargs={'device': 'cpu'}
        )
        self._store = None

    def _get_or_create_store(self) -> Chroma:
        if self._store is None:
            self._store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        return self._store

    def store_documents(self, documents: List[DocumentChunk]) -> int:
        langchain_docs = [
            Document(page_content=doc.content, metadata=doc.metadata) 
            for doc in documents
        ]
        store = self._get_or_create_store()
        store.add_documents(langchain_docs)
        embed_logger.info(f"Indexed {len(langchain_docs)} chunks into ChromaDB.")
        return len(langchain_docs)

    def search_similar(self, query: str, top_k: int) -> List[DocumentChunk]:
        store = self._get_or_create_store()
        # Returns tuple of (Document, score) -> L2 distance, lower is better
        results = store.similarity_search_with_score(query, k=top_k)
        
        chunks = []
        for doc, score in results:
            # Convert L2 distance to an approximate percentage similarity for UI
            similarity = max(0.0, 100.0 - (score * 50))
            chunks.append(DocumentChunk(
                content=doc.page_content, 
                metadata=doc.metadata,
                score=round(similarity, 2)
            ))
        return chunks

    def clear_database(self) -> None:
        self._store = None
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
            os.makedirs(self.persist_directory, exist_ok=True)
            embed_logger.info("Vector database cleared.")

    def get_document_count(self) -> int:
        try:
            store = self._get_or_create_store()
            return store._collection.count()
        except Exception:
            return 0