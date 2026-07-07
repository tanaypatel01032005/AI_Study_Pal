from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from backend.app.database.base import Base

class LearningInsight(Base):
    """
    Stores AI-generated analytics and recommendations about the user's learning progress.
    Since this is a single-user portfolio app, we don't strictly require a User model.
    """
    __tablename__ = "learning_insights"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # JSON field storing aggregated metrics (e.g. quiz_scores, completed_milestones, chat_topics)
    metrics = Column(JSON, nullable=True) 
    
    # AI-generated analysis
    strong_concepts = Column(Text, nullable=True) # comma-separated or JSON
    weak_concepts = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
