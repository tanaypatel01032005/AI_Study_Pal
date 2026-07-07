from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from backend.app.database.session import get_db
from backend.app.ai.study_planner_service import StudyPlanService

router = APIRouter()

class StudyMilestoneResponse(BaseModel):
    id: int
    day_number: int
    topic: str
    description: Optional[str] = None
    is_completed: bool
    
    class Config:
        from_attributes = True

class StudyPlanResponse(BaseModel):
    id: int
    document_id: Optional[int]
    title: str
    milestones: List[StudyMilestoneResponse]
    
    class Config:
        from_attributes = True

@router.post("/generate/{document_id}", response_model=StudyPlanResponse, summary="Generate a study plan from a document")
def generate_study_plan(document_id: int, num_days: int = 7, db: Session = Depends(get_db)):
    service = StudyPlanService(db)
    try:
        plan = service.generate_study_plan(document_id, num_days)
        return plan
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{plan_id}", response_model=StudyPlanResponse, summary="Get an existing study plan")
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    service = StudyPlanService(db)
    plan = service.get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Study plan not found")
    return plan
