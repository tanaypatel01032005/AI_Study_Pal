import logging
import requests
from typing import List
from backend.app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger("ai_study_pal")

class EmbeddingService:
    """
    Service responsible for generating text embeddings via Hugging Face Inference API.
    Gracefully falls back to mock embeddings if the API is unreachable (e.g. offline/sandbox).
    """
    
    @classmethod
    def _get_api_url(cls) -> str:
        return f"https://api-inference.huggingface.co/pipeline/feature-extraction/{settings.EMBEDDING_MODEL}"

    @classmethod
    def _get_headers(cls) -> dict:
        if not settings.HF_API_KEY:
            return {}
        return {"Authorization": f"Bearer {settings.HF_API_KEY}"}

    @classmethod
    def generate_embedding(cls, text: str) -> List[float]:
        try:
            response = requests.post(
                cls._get_api_url(),
                headers=cls._get_headers(),
                json={"inputs": text, "options": {"wait_for_model": True}},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.warning("Returning mock embedding due to API/Network failure")
            return [0.0] * 384

    @classmethod
    def generate_embeddings(cls, texts: List[str]) -> List[List[float]]:
        try:
            response = requests.post(
                cls._get_api_url(),
                headers=cls._get_headers(),
                json={"inputs": texts, "options": {"wait_for_model": True}},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.warning("Returning mock embeddings due to API/Network failure")
            return [[0.0] * 384 for _ in texts]
