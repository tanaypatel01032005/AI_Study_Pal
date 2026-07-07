import logging
import json
from sqlalchemy.orm import Session
from backend.app.models.flashcard import FlashcardDeck, Flashcard
from backend.app.models.document import Document
from backend.app.ai.llm_service import LLMService

logger = logging.getLogger("ai_study_pal")

class FlashcardService:
    """
    Generates flashcards from document content using LLM.
    """
    def __init__(self, db: Session):
        self.db = db
        self.llm = LLMService()

    def generate_flashcards(self, document_id: int, num_cards: int = 10) -> FlashcardDeck:
        """
        Generate flashcards for a specific document.
        """
        doc = self.db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise ValueError(f"Document {document_id} not found.")

        # Limit text to fit context window
        context_text = doc.content[:3000]

        prompt = (
            f"Extract {num_cards} key concepts and definitions from the following text to create flashcards.\n\n"
            f"Text: {context_text}\n\n"
            f"Output EXACTLY a JSON list of dictionaries. Each dictionary must have keys: "
            f"'front' (the concept, term, or question) and "
            f"'back' (the definition or answer).\n"
            f"Do not include any markdown formatting, just the raw JSON array."
        )

        try:
            logger.info(f"Generating flashcards for Document {document_id}")
            response_text = self.llm.generate(prompt, max_new_tokens=800, temperature=0.3)
            
            # Simple cleanup of possible markdown block ticks
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
                
            cards_data = json.loads(response_text.strip())
            
            # Create Deck
            deck = FlashcardDeck(
                document_id=document_id,
                title=f"Flashcards: {doc.title}"
            )
            self.db.add(deck)
            self.db.commit()
            self.db.refresh(deck)

            # Create Cards
            for c_data in cards_data:
                card = Flashcard(
                    deck_id=deck.id,
                    front=c_data.get("front", "Missing front"),
                    back=c_data.get("back", "Missing back")
                )
                self.db.add(card)
                
            self.db.commit()
            self.db.refresh(deck)
            return deck

        except json.JSONDecodeError:
            logger.error("Failed to parse LLM response as JSON.")
            raise ValueError("The AI failed to generate a valid flashcard format. Please try again.")
        except Exception as e:
            logger.error(f"Flashcard generation error: {e}")
            raise ValueError("An error occurred while generating flashcards.")

    def get_deck(self, deck_id: int) -> FlashcardDeck:
        return self.db.query(FlashcardDeck).filter(FlashcardDeck.id == deck_id).first()
