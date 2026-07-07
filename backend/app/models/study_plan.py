from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database.base import Base

class StudyPlan(Base):
    """
    Represents an auto-generated study plan for a document or topic.
    """
    __tablename__ = "study_plans"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    title = Column(String, default="My Study Plan")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    milestones = relationship("StudyMilestone", back_populates="plan", cascade="all, delete-orphan", order_by="StudyMilestone.day_number")
    document = relationship("Document")

class StudyMilestone(Base):
    """
    Represents a specific milestone or task within a StudyPlan.
    """
    __tablename__ = "study_milestones"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("study_plans.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    topic = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)

    plan = relationship("StudyPlan", back_populates="milestones")
