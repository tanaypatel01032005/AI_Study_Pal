import logging
import json
from sqlalchemy.orm import Session
from backend.app.models.insight import LearningInsight
from backend.app.models.quiz import Quiz, Question
from backend.app.models.study_plan import StudyPlan, StudyMilestone
from backend.app.ai.llm_service import LLMService

logger = logging.getLogger("ai_study_pal")

class InsightService:
    """
    Analyzes learning data to generate insights and recommendations.
    """
    def __init__(self, db: Session):
        self.db = db
        self.llm = LLMService()

    def generate_insights(self) -> LearningInsight:
        """
        Gathers data and asks LLM to analyze user's strong/weak concepts and recommendations.
        """
        # Gather data
        quizzes = self.db.query(Quiz).all()
        plans = self.db.query(StudyPlan).all()
        
        # In a real app we'd fetch actual scores and milestone completion statuses.
        # Here we just pass the names and topics to the LLM as a mock user profile.
        quiz_topics = [q.title for q in quizzes]
        plan_topics = [p.title for p in plans]
        
        data_summary = (
            f"User has taken {len(quizzes)} quizzes on topics: {', '.join(quiz_topics)}. "
            f"User has {len(plans)} study plans covering: {', '.join(plan_topics)}. "
            "Assume some typical difficulties and successes based on these topics."
        )

        prompt = (
            f"You are an AI Learning Analyst.\n"
            f"Based on the following user study data, generate learning insights.\n\n"
            f"Data: {data_summary}\n\n"
            f"Output EXACTLY a JSON object with three keys: "
            f"'strong_concepts' (string), 'weak_concepts' (string), and 'recommendations' (string).\n"
            f"Do not include any markdown formatting, just the raw JSON."
        )

        try:
            logger.info("Generating learning insights.")
            response_text = self.llm.generate(prompt, max_new_tokens=400, temperature=0.5)
            
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
                
            insight_data = json.loads(response_text.strip())
            
            insight = LearningInsight(
                strong_concepts=insight_data.get("strong_concepts", "General knowledge"),
                weak_concepts=insight_data.get("weak_concepts", "Advanced topics"),
                recommendations=insight_data.get("recommendations", "Keep studying!")
            )
            self.db.add(insight)
            self.db.commit()
            self.db.refresh(insight)
            return insight

        except json.JSONDecodeError:
            logger.error("Failed to parse LLM response as JSON.")
            raise ValueError("The AI failed to generate insights in a valid format.")
        except Exception as e:
            logger.error(f"Insight generation error: {e}")
            raise ValueError("An error occurred while generating insights.")

    def get_latest_insight(self) -> LearningInsight:
        return self.db.query(LearningInsight).order_by(LearningInsight.created_at.desc()).first()
