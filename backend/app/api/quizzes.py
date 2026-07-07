from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from backend.app.database.session import get_db
from backend.app.ai.quiz_service import QuizService

router = APIRouter()

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    options: str
    correct_answer: str
    explanation: Optional[str] = None
    
    class Config:
        from_attributes = True

class QuizResponse(BaseModel):
    id: int
    document_id: Optional[int]
    title: str
    difficulty: str
    questions: List[QuestionResponse]
    
    class Config:
        from_attributes = True

@router.post("/generate/{document_id}", response_model=QuizResponse, summary="Generate a quiz from a document")
def generate_quiz(document_id: int, num_questions: int = 5, difficulty: str = "Medium", db: Session = Depends(get_db)):
    service = QuizService(db)
    try:
        quiz = service.generate_quiz(document_id, num_questions, difficulty)
        return quiz
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{quiz_id}", response_model=QuizResponse, summary="Get an existing quiz")
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    service = QuizService(db)
    quiz = service.get_quiz(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz
