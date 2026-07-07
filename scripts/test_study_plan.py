import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database.session import SessionLocal
from backend.app.models.document import Document
from backend.app.ai.study_planner_service import StudyPlanService

def test():
    db = SessionLocal()
    try:
        doc = db.query(Document).first()
        if not doc:
            print("No documents found.")
            return

        print(f"Generating 3-Day Study Plan for Document {doc.id}: {doc.title}")
        service = StudyPlanService(db)
        
        plan = service.generate_study_plan(doc.id, num_days=3)
        print(f"\nStudy Plan Generated: {plan.title}")
        
        for idx, milestone in enumerate(plan.milestones, 1):
            print(f"\nDay {milestone.day_number}: {milestone.topic}")
            print(f"Details: {milestone.description}")
            
    finally:
        db.close()

if __name__ == "__main__":
    test()
