from typing import List
import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.interfaces import IDocumentLoader
from core.models import DocumentChunk
from config import CONFIG

logger = logging.getLogger("App")

class PyPDFDocumentLoader(IDocumentLoader):
    def __init__(self) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CONFIG.chunk_size,
            chunk_overlap=CONFIG.chunk_overlap
        )

    def load_and_split(self, file_paths: List[str]) -> List[DocumentChunk]:
        documents = []
        for path in file_paths:
            try:
                loader = PyPDFLoader(path)
                documents.extend(loader.load())
            except Exception as e:
                logger.error(f"Failed to load {path}: {str(e)}")
                
        chunks = self.splitter.split_documents(documents)
        return [
            DocumentChunk(content=chunk.page_content, metadata=chunk.metadata) 
            for chunk in chunks
        ]