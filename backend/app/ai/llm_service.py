import logging
import requests
from backend.app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger("ai_study_pal")

class LLMService:
    """
    Service layer for Language Model generation.
    Connects to the Hugging Face text-generation API.
    """

    @classmethod
    def _get_api_url(cls, model: str) -> str:
        return f"https://api-inference.huggingface.co/models/{model}"

    @classmethod
    def _get_headers(cls) -> dict:
        if not settings.HF_API_KEY:
            return {}
        return {"Authorization": f"Bearer {settings.HF_API_KEY}"}

    @classmethod
    def generate(cls, prompt: str, max_new_tokens: int = 150, temperature: float = 0.7) -> str:
        """
        Generate text using the configured LLM model via HF API.
        """
        try:
            response = requests.post(
                cls._get_api_url(settings.LLM_MODEL),
                headers=cls._get_headers(),
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": max_new_tokens,
                        "temperature": temperature,
                        "return_full_text": False
                    },
                    "options": {"wait_for_model": True}
                },
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                return result[0]["generated_text"].strip()
            return str(result)
        except Exception as e:
            logger.error(f"LLM Generation Error: {e}")
            return "I apologize, but I am currently offline or unable to reach my language model."

    @classmethod
    def summarize(cls, text: str) -> str:
        """
        Summarize text using a dedicated summarization model.
        """
        try:
            response = requests.post(
                cls._get_api_url(settings.SUMMARIZATION_MODEL),
                headers=cls._get_headers(),
                json={
                    "inputs": text,
                    "options": {"wait_for_model": True}
                },
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            if isinstance(result, list) and len(result) > 0 and "summary_text" in result[0]:
                return result[0]["summary_text"].strip()
            return str(result)
        except Exception as e:
            logger.error(f"Summarization Error: {e}")
            return "Summarization unavailable at the moment."
