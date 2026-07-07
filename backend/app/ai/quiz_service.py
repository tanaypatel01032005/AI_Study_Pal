import logging
import json
from sqlalchemy.orm import Session
from backend.app.models.quiz import Quiz, Question
from backend.app.models.document import Document
from backend.app.ai.llm_service import LLMService

logger = logging.getLogger("ai_study_pal")

class QuizService:
    """
    Generates dynamic quizzes from document content using LLM.
    """
    def __init__(self, db: Session):
        self.db = db
        self.llm = LLMService()

    def generate_quiz(self, document_id: int, num_questions: int = 5, difficulty: str = "Medium") -> Quiz:
        """
        Generate a quiz for a specific document.
        """
        doc = self.db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise ValueError(f"Document {document_id} not found.")

        # Limit text to fit context window
        context_text = doc.content[:3000]

        prompt = (
            f"Generate a {difficulty} difficulty multiple-choice quiz with {num_questions} questions "
            f"based on the following text.\n\n"
            f"Text: {context_text}\n\n"
            f"Output EXACTLY a JSON list of dictionaries. Each dictionary must have keys: "
            f"'question', 'options' (a list of 4 strings), 'correct_answer' (the exact string from options), "
            f"and 'explanation' (why the answer is correct).\n"
            f"Do not include any markdown formatting, just the raw JSON array."
        )

        try:
            logger.info(f"Generating quiz for Document {document_id}")
            response_text = self.llm.generate(prompt, max_new_tokens=800, temperature=0.3)
            
            # Simple cleanup of possible markdown block ticks
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
                
            questions_data = json.loads(response_text.strip())
            
            # Create Quiz
            quiz = Quiz(
                document_id=document_id,
                title=f"Quiz: {doc.title}",
                difficulty=difficulty
            )
            self.db.add(quiz)
            self.db.commit()
            self.db.refresh(quiz)

            # Create Questions
            for q_data in questions_data:
                question = Question(
                    quiz_id=quiz.id,
                    question_text=q_data.get("question", "Missing question"),
                    question_type="multiple_choice",
                    options=json.dumps(q_data.get("options", [])),
                    correct_answer=q_data.get("correct_answer", ""),
                    explanation=q_data.get("explanation", "")
                )
                self.db.add(question)
                
            self.db.commit()
            self.db.refresh(quiz)
            return quiz

        except json.JSONDecodeError:
            logger.error("Failed to parse LLM response as JSON.")
            raise ValueError("The AI failed to generate a valid quiz format. Please try again.")
        except Exception as e:
            logger.error(f"Quiz generation error: {e}")
            raise ValueError("An error occurred while generating the quiz.")

    def get_quiz(self, quiz_id: int) -> Quiz:
        return self.db.query(Quiz).filter(Quiz.id == quiz_id).first()
