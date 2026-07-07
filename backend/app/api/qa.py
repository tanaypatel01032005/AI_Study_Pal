from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any

from backend.app.database.session import get_db
from backend.app.rag.pipeline import RAGPipeline

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str

@router.post("/ask", response_model=QuestionResponse, summary="Ask a question using RAG")
def ask_question(request: QuestionRequest, db: Session = Depends(get_db)):
    """
    Submit a question to the AI Tutor. The system will retrieve relevant context
    from the uploaded documents and generate an answer using the LLM.
    """
    if not request.question.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Question cannot be empty.")
        
    try:
        pipeline = RAGPipeline(db)
        answer = pipeline.answer_question(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error generating answer: {str(e)}")

@router.post("/index-all", summary="Re-index all unindexed documents")
def index_all(db: Session = Depends(get_db)):
    """
    Admin endpoint to trigger indexing of all uploaded documents that haven't been chunked and embedded yet.
    """
    try:
        pipeline = RAGPipeline(db)
        pipeline.index_all_unindexed_documents()
        return {"message": "Indexing complete."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Indexing failed: {str(e)}")
