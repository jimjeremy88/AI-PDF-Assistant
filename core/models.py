from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class DocumentChunk:
    """Entity representing a piece of text with metadata and similarity score."""
    content: str
    metadata: Dict[str, Any]
    score: float = 0.0

@dataclass
class ChatResponse:
    """Entity representing the AI's response."""
    answer: str
    sources: List[DocumentChunk]
    timestamp: str
    generation_time: float