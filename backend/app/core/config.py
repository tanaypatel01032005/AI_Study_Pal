from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables or .env file.
    Provides a central place for configuration management.
    """
    PROJECT_NAME: str = "AI Study Pal 2.0"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your_secret_key_here"  # Default for development
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Database
    DATABASE_URL: str = "sqlite:///./ai_study_pal.db"
    
    # LLM Settings
    LLM_PROVIDER: str = "huggingface"
    LLM_MODEL: str = "google/flan-t5-base"
    SUMMARIZATION_MODEL: str = "facebook/bart-large-cnn"
    OPENAI_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    HF_API_KEY: str | None = None
    
    # RAG Settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K_RETRIEVAL: int = 3
    SIMILARITY_THRESHOLD: float = 0.75
    MAX_CONTEXT_LENGTH: int = 2048
    UPLOAD_SIZE_LIMIT_MB: int = 10

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    """Return application settings, cached for performance."""
    return Settings()
