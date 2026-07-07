import pandas as pd
import sys
import os

# Add the project root to the python path to allow importing backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database.session import SessionLocal
from backend.app.models.document import Document

def migrate_data():
    """Migrate data from legacy CSV to the new SQLite database."""
    print("Starting data migration from CSV...")
    
    csv_path = "educational_texts.csv"
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        return

    db = SessionLocal()
    
    docs_added = 0
    try:
        for _, row in df.iterrows():
            # Check if document already exists to avoid duplicates if run multiple times
            existing_doc = db.query(Document).filter(
                Document.subject == row['subject'],
                Document.content == row['text']
            ).first()
            
            if not existing_doc:
                doc = Document(
                    title=f"{row['subject']} - {row['text'][:30]}...",
                    subject=row['subject'],
                    content=row['text'],
                    word_count=row.get('word_count', 0),
                    sentence_count=row.get('sentence_count', 0)
                )
                db.add(doc)
                docs_added += 1
                
        db.commit()
        print(f"Successfully migrated {docs_added} new documents to the database.")
    except Exception as e:
        db.rollback()
        print(f"Database migration failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    migrate_data()
