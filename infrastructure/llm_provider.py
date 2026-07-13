from langchain_ollama import ChatOllama
from langchain_core.language_models.chat_models import BaseChatModel
from core.interfaces import ILLMProvider
from config import CONFIG

class OllamaProvider(ILLMProvider):
    def get_model(self, temperature: float) -> BaseChatModel:
        return ChatOllama(
            model=CONFIG.llm_model,
            temperature=temperature
        )