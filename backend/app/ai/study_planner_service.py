import logging
import json
from sqlalchemy.orm import Session
from backend.app.models.study_plan import StudyPlan, StudyMilestone
from backend.app.models.document import Document
from backend.app.ai.llm_service import LLMService

logger = logging.getLogger("ai_study_pal")

class StudyPlanService:
    """
    Generates personalized study plans and milestones.
    """
    def __init__(self, db: Session):
        self.db = db
        self.llm = LLMService()

    def generate_study_plan(self, document_id: int, num_days: int = 7) -> StudyPlan:
        """
        Generate a study plan breaking down the document content into daily milestones.
        """
        doc = self.db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise ValueError(f"Document {document_id} not found.")

        # Limit text to fit context window
        context_text = doc.content[:3000]

        prompt = (
            f"Create a {num_days}-day study plan based on the following text.\n\n"
            f"Text: {context_text}\n\n"
            f"Output EXACTLY a JSON list of dictionaries, one for each day. Each dictionary must have keys: "
            f"'day_number' (integer starting from 1 to {num_days}), "
            f"'topic' (string, the main concept to study that day), and "
            f"'description' (string, brief instructions on what to read or do).\n"
            f"Do not include any markdown formatting, just the raw JSON array."
        )

        try:
            logger.info(f"Generating {num_days}-day study plan for Document {document_id}")
            response_text = self.llm.generate(prompt, max_new_tokens=800, temperature=0.4)
            
            # Simple cleanup of possible markdown block ticks
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
                
            milestones_data = json.loads(response_text.strip())
            
            # Create Plan
            plan = StudyPlan(
                document_id=document_id,
                title=f"{num_days}-Day Study Plan: {doc.title}"
            )
            self.db.add(plan)
            self.db.commit()
            self.db.refresh(plan)

            # Create Milestones
            for m_data in milestones_data:
                milestone = StudyMilestone(
                    plan_id=plan.id,
                    day_number=m_data.get("day_number", 1),
                    topic=m_data.get("topic", "General Study"),
                    description=m_data.get("description", "")
                )
                self.db.add(milestone)
                
            self.db.commit()
            self.db.refresh(plan)
            return plan

        except json.JSONDecodeError:
            logger.error("Failed to parse LLM response as JSON.")
            raise ValueError("The AI failed to generate a valid study plan format. Please try again.")
        except Exception as e:
            logger.error(f"Study plan generation error: {e}")
            raise ValueError("An error occurred while generating the study plan.")

    def get_plan(self, plan_id: int) -> StudyPlan:
        return self.db.query(StudyPlan).filter(StudyPlan.id == plan_id).first()
