import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database.session import SessionLocal
from backend.app.ai.chat_agent import ChatAgent

def test():
    db = SessionLocal()
    try:
        agent = ChatAgent(db)
        
        # 1. Create Session
        print("Creating chat session...")
        session = agent.create_session("Test RAG Session")
        print(f"Created Session {session.id}: {session.title}")
        
        # 2. Send Message
        question = "What is thermodynamics?"
        print(f"\nUser: {question}")
        answer = agent.send_message(session.id, question)
        print(f"AI Tutor: {answer}")
        
        # 3. Check History
        print("\nRetrieving chat history...")
        history = agent.get_history(session.id)
        for h in history:
            print(f"[{h.created_at}] {h.role}: {h.content}")
            
    finally:
        db.close()

if __name__ == "__main__":
    test()
