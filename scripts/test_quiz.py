import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database.session import SessionLocal
from backend.app.models.document import Document
from backend.app.ai.quiz_service import QuizService

def test():
    db = SessionLocal()
    try:
        doc = db.query(Document).first()
        if not doc:
            print("No documents found.")
            return

        print(f"Generating Quiz for Document {doc.id}: {doc.title}")
        service = QuizService(db)
        
        quiz = service.generate_quiz(doc.id, num_questions=2)
        print(f"\nQuiz Generated: {quiz.title} (Difficulty: {quiz.difficulty})")
        
        for idx, q in enumerate(quiz.questions, 1):
            print(f"\nQ{idx}: {q.question_text}")
            print(f"Options: {q.options}")
            print(f"Answer: {q.correct_answer}")
            print(f"Explanation: {q.explanation}")
            
    finally:
        db.close()

if __name__ == "__main__":
    test()
