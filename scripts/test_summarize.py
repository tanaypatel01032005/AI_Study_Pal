import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database.session import SessionLocal
from backend.app.models.document import Document
from backend.app.ai.llm_service import LLMService

def test():
    db = SessionLocal()
    try:
        doc = db.query(Document).first()
        if not doc:
            print("No documents found.")
            return

        print(f"Summarizing Document {doc.id}: {doc.title}")
        llm = LLMService()
        text_to_summarize = doc.content[:2000]
        summary = llm.summarize(text_to_summarize)
        
        print("\nSummary generated:")
        print(summary)
            
    finally:
        db.close()

if __name__ == "__main__":
    test()
