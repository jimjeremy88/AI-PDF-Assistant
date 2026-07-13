import time
import logging
from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser

from core.interfaces import IDocumentLoader, IVectorStore, ILLMProvider
from core.models import ChatResponse, DocumentChunk

logger = logging.getLogger("App")

class RAGUseCase:
    """Orchestrates RAG logic using pure LCEL, completely bypassing legacy chains."""
    def __init__(
        self, 
        loader: IDocumentLoader, 
        vector_store: IVectorStore, 
        llm_provider: ILLMProvider
    ) -> None:
        self._loader = loader
        self._vector_store = vector_store
        self._llm_provider = llm_provider

    def process_new_documents(self, file_paths: List[str]) -> int:
        """Processes documents and returns total chunks indexed."""
        try:
            self._vector_store.clear_database()
            chunks = self._loader.load_and_split(file_paths)
            if chunks:
                return self._vector_store.store_documents(chunks)
            return 0
        except Exception as e:
            logger.error(f"Document processing failed: {str(e)}", exc_info=True)
            raise ValueError(f"Failed to process documents: {str(e)}")

    def generate_response(
        self, 
        question: str, 
        chat_history: List[BaseMessage], 
        temperature: float, 
        top_k: int, 
        system_prompt: str
    ) -> ChatResponse:
        """Generates AI response using pure LangChain Expression Language (LCEL)."""
        start_time = time.time()
        try:
            llm = self._llm_provider.get_model(temperature)
            
            # 1. Direct Search to get scores and context
            source_chunks = self._vector_store.search_similar(question, top_k)
            context_text = "\n\n".join([chunk.content for chunk in source_chunks])

            # 2. Pure Core Prompt (No broken chains required)
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ])
            
            # 3. Pure LCEL Pipeline
            chain = prompt | llm | StrOutputParser()
            
            answer = chain.invoke({
                "context": context_text,
                "input": question,
                "chat_history": chat_history
            })

            generation_time = round(time.time() - start_time, 2)
            timestamp = time.strftime("%I:%M %p")
            
            logger.info(f"Generated response in {generation_time}s")
            return ChatResponse(
                answer=answer, 
                sources=source_chunks, 
                timestamp=timestamp, 
                generation_time=generation_time
            )
            
        except Exception as e:
            logger.error(f"Generation failed: {str(e)}", exc_info=True)
            raise RuntimeError("The AI encountered an error generating a response. Check logs.")
            
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Fetch metrics for the UI Dashboard."""
        return {
            "chunks_indexed": self._vector_store.get_document_count()
        }