from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from backend.app.database.session import get_db
from backend.app.ai.flashcard_service import FlashcardService

router = APIRouter()

class FlashcardResponse(BaseModel):
    id: int
    front: str
    back: str
    
    class Config:
        from_attributes = True

class FlashcardDeckResponse(BaseModel):
    id: int
    document_id: Optional[int]
    title: str
    cards: List[FlashcardResponse]
    
    class Config:
        from_attributes = True

@router.post("/generate/{document_id}", response_model=FlashcardDeckResponse, summary="Generate flashcards from a document")
def generate_flashcards(document_id: int, num_cards: int = 10, db: Session = Depends(get_db)):
    service = FlashcardService(db)
    try:
        deck = service.generate_flashcards(document_id, num_cards)
        return deck
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{deck_id}", response_model=FlashcardDeckResponse, summary="Get an existing flashcard deck")
def get_deck(deck_id: int, db: Session = Depends(get_db)):
    service = FlashcardService(db)
    deck = service.get_deck(deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Flashcard deck not found")
    return deck
