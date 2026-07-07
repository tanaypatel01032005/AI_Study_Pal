import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database.session import SessionLocal
from backend.app.ai.insight_service import InsightService

def test():
    db = SessionLocal()
    try:
        print("Generating Learning Insights...")
        service = InsightService(db)
        
        insight = service.generate_insights()
        
        print("\nLearning Insights Generated:")
        print(f"Strong Concepts: {insight.strong_concepts}")
        print(f"Weak Concepts:   {insight.weak_concepts}")
        print(f"Recommendations: {insight.recommendations}")
            
    finally:
        db.close()

if __name__ == "__main__":
    test()
