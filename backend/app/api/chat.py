from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any

from backend.app.database.session import get_db
from backend.app.ai.chat_agent import ChatAgent
from backend.app.models.chat import ChatSession

router = APIRouter()

class SessionResponse(BaseModel):
    id: int
    title: str

class ChatMessageRequest(BaseModel):
    message: str

class ChatMessageResponse(BaseModel):
    role: str
    content: str

@router.post("/sessions", response_model=SessionResponse, summary="Create a new chat session")
def create_session(title: str = "New Study Session", db: Session = Depends(get_db)):
    agent = ChatAgent(db)
    session = agent.create_session(title)
    return {"id": session.id, "title": session.title}

@router.get("/sessions/{session_id}/history", response_model=List[ChatMessageResponse], summary="Get chat history")
def get_history(session_id: int, db: Session = Depends(get_db)):
    agent = ChatAgent(db)
    history = agent.get_history(session_id)
    return [{"role": h.role, "content": h.content} for h in history]

@router.post("/sessions/{session_id}/message", response_model=ChatMessageResponse, summary="Send a message to AI Tutor")
def send_message(session_id: int, request: ChatMessageRequest, db: Session = Depends(get_db)):
    if not request.message.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message cannot be empty.")
    
    # Verify session
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")

    agent = ChatAgent(db)
    try:
        answer = agent.send_message(session_id, request.message)
        return {"role": "assistant", "content": answer}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error generating response: {str(e)}")
