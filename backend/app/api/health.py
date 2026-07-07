from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    message: str
    version: str | None = None

@router.get("/health", response_model=HealthResponse)
async def health_check() -> Dict[str, Any]:
    """
    Check if the API is running correctly.
    """
    # In the future, this can be expanded to check DB connections, etc.
    return {
        "status": "healthy",
        "message": "AI Study Pal backend is running",
        "version": "0.1.0"
    }
