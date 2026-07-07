# Expose models for Alembic to autogenerate schemas
from backend.app.database.base import Base
from backend.app.models.document import Document, DocumentChunk
from backend.app.models.chat import ChatSession, ChatMessage
from backend.app.models.quiz import Quiz, Question
from backend.app.models.flashcard import FlashcardDeck, Flashcard
from backend.app.models.study_plan import StudyPlan, StudyMilestone
