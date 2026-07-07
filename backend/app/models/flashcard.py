from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database.base import Base

class FlashcardDeck(Base):
    """
    Represents a deck of flashcards generated for a document.
    """
    __tablename__ = "flashcard_decks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    title = Column(String, default="Untitled Deck")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    cards = relationship("Flashcard", back_populates="deck", cascade="all, delete-orphan")
    document = relationship("Document")

class Flashcard(Base):
    """
    Represents a single flashcard within a deck.
    """
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    deck_id = Column(Integer, ForeignKey("flashcard_decks.id"), nullable=False)
    front = Column(Text, nullable=False) # Concept or question
    back = Column(Text, nullable=False)  # Definition or answer
    
    deck = relationship("FlashcardDeck", back_populates="cards")
