from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from backend.app.database.session import get_db
from backend.app.ai.insight_service import InsightService

router = APIRouter()

class InsightResponse(BaseModel):
    id: int
    created_at: datetime
    strong_concepts: Optional[str]
    weak_concepts: Optional[str]
    recommendations: Optional[str]
    
    class Config:
        from_attributes = True

@router.post("/generate", response_model=InsightResponse, summary="Generate new learning insights")
def generate_insights(db: Session = Depends(get_db)):
    service = InsightService(db)
    try:
        insight = service.generate_insights()
        return insight
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/latest", response_model=InsightResponse, summary="Get the latest learning insights")
def get_latest_insight(db: Session = Depends(get_db)):
    service = InsightService(db)
    insight = service.get_latest_insight()
    if not insight:
        raise HTTPException(status_code=404, detail="No insights found. Generate one first.")
    return insight
