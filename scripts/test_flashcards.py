import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database.session import SessionLocal
from backend.app.models.document import Document
from backend.app.ai.flashcard_service import FlashcardService

def test():
    db = SessionLocal()
    try:
        doc = db.query(Document).first()
        if not doc:
            print("No documents found.")
            return

        print(f"Generating Flashcards for Document {doc.id}: {doc.title}")
        service = FlashcardService(db)
        
        deck = service.generate_flashcards(doc.id, num_cards=2)
        print(f"\nFlashcard Deck Generated: {deck.title}")
        
        for idx, card in enumerate(deck.cards, 1):
            print(f"\nCard {idx}:")
            print(f"Front: {card.front}")
            print(f"Back:  {card.back}")
            
    finally:
        db.close()

if __name__ == "__main__":
    test()
