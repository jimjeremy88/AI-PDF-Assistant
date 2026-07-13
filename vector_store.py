import os
import logging
from typing import List, Tuple
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from config import CONFIG
from database import DatabaseManager

logger = logging.getLogger("App")

class AdvancedRAGPipeline:
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db = db_manager
        try:
            self._embeddings = HuggingFaceEmbeddings(
                model_name=CONFIG.EMBEDDING_MODEL,
                model_kwargs={"device": "cpu"}
            )
        except Exception as e:
            logger.warning(f"Network drop encountered. Engaging offline asset isolation: {e}")
            os.environ["HF_HUB_OFFLINE"] = "1"
            os.environ["TRANSFORMERS_OFFLINE"] = "1"
            self._embeddings = HuggingFaceEmbeddings(model_name=CONFIG.EMBEDDING_MODEL)
            
        self._vector_store = Chroma(
            persist_directory=CONFIG.DB_DIR, 
            embedding_function=self._embeddings
        )

    def process_pdf(self, file_path: str, filename: str, file_size_mb: float) -> int:
        try:
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=CONFIG.CHUNK_SIZE, 
                chunk_overlap=CONFIG.CHUNK_OVERLAP,
                separators=["\n\n", "\n", "(?<=\\. )", " ", ""]
            )
            chunks = splitter.split_documents(docs)
            for i, chunk in enumerate(chunks):
                chunk.metadata.update({"chunk_id": i, "source_file": filename})
            self._vector_store.add_documents(chunks)
            self.db.add_document(filename, file_size_mb, len(chunks))
            return len(chunks)
        except Exception as e:
            logger.error(f"Failed pipeline processing execution for {filename}", exc_info=True)
            raise RuntimeError(f"Indexing failed: {str(e)}")

    def search_similar(self, query: str, top_k: int, threshold: float = 0.0) -> List[Tuple[Document, float]]:
        try:
            results = self._vector_store.similarity_search_with_score(query, k=top_k)
            valid_results = []
            for doc, score in results:
                similarity_pct = max(0.0, 100.0 - (score * 50))
                if similarity_pct >= threshold:
                    valid_results.append((doc, round(similarity_pct, 2)))
            return valid_results
        except Exception as e:
            logger.error("Vector search failure mapping context blocks", exc_info=True)
            return []

    def get_total_chunks(self) -> int:
        try: return self._vector_store._collection.count()
        except: return 0