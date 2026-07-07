import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database.session import SessionLocal
from backend.app.rag.pipeline import RAGPipeline
from backend.app.models.document import Document

def test():
    db = SessionLocal()
    try:
        pipeline = RAGPipeline(db)
        
        # Ensure we have a document to index
        doc_count = db.query(Document).count()
        if doc_count == 0:
            print("No documents in DB to index. Please upload or migrate data first.")
            return

        print(f"Found {doc_count} documents. Indexing unindexed documents...")
        pipeline.index_all_unindexed_documents()
        
        print("\nIndexing complete. Testing QA...")
        question = "What is the capital of France?" # The DB might not have this, but let's test the pipeline
        print(f"Q: {question}")
        answer = pipeline.answer_question(question)
        print(f"A: {answer}")
        
    finally:
        db.close()

if __name__ == "__main__":
    test()
