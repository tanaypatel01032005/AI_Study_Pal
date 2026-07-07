from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database.base import Base

class Quiz(Base):
    """
    Represents an auto-generated quiz for a document or subject.
    """
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    title = Column(String, default="Untitled Quiz")
    difficulty = Column(String, default="Medium")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    document = relationship("Document")

class Question(Base):
    """
    Represents a single question within a Quiz.
    """
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String, default="multiple_choice") # multiple_choice, true_false, short_answer
    options = Column(Text, nullable=True) # JSON serialized list of options if multiple choice
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)

    quiz = relationship("Quiz", back_populates="questions")
