import logging
from typing import List
from sqlalchemy.orm import Session
from backend.app.rag.pipeline import RAGPipeline
from backend.app.models.chat import ChatSession, ChatMessage
from backend.app.ai.llm_service import LLMService

logger = logging.getLogger("ai_study_pal")

class ChatAgent:
    """
    Handles conversational interactions, maintaining history
    and leveraging RAG for context-aware responses.
    """
    def __init__(self, db: Session):
        self.db = db
        self.rag = RAGPipeline(db)
        self.llm = LLMService()

    def create_session(self, title: str = "New Study Session") -> ChatSession:
        session = ChatSession(title=title)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_history(self, session_id: int) -> List[ChatMessage]:
        return self.db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()

    def send_message(self, session_id: int, message: str) -> str:
        # Save user message
        user_msg = ChatMessage(session_id=session_id, role="user", content=message)
        self.db.add(user_msg)
        self.db.commit()

        # Retrieve RAG context
        query_embedding = self.rag.embedding_service.generate_embedding(message)
        results = self.rag.vector_store.search(query_embedding, top_k=self.rag.vector_store.dimension) # using default k from settings inside RAG usually, but let's just search
        # Wait, pipeline already has `answer_question`, but we want to customize the prompt to include chat history.
        
        # Manually perform RAG steps
        from backend.app.core.config import get_settings
        settings = get_settings()
        
        results = self.rag.vector_store.search(query_embedding, top_k=settings.TOP_K_RETRIEVAL)
        context_texts = []
        if results:
            from backend.app.models.document import DocumentChunk
            for chunk_id, score in results:
                db_chunk = self.db.query(DocumentChunk).filter(DocumentChunk.id == chunk_id).first()
                if db_chunk:
                    context_texts.append(db_chunk.text)
                    
        context_str = "\n\n---\n\n".join(context_texts) if context_texts else "No relevant context found."

        # Fetch history (last 5 messages to avoid token overflow)
        history = self.get_history(session_id)[-6:-1] # excluding the current user message just added
        
        history_str = ""
        for h in history:
            role_label = "Student" if h.role == "user" else "Tutor"
            history_str += f"{role_label}: {h.content}\n"

        prompt = (
            f"You are AI Study Pal, an intelligent and encouraging tutor.\n"
            f"Use the following conversation history and retrieved context to answer the student's question.\n\n"
            f"[Context from Course Materials]\n{context_str}\n\n"
            f"[Conversation History]\n{history_str}\n"
            f"Student: {message}\n"
            f"Tutor:"
        )

        logger.info(f"Generating answer for session {session_id}")
        answer = self.llm.generate(prompt)

        # Save AI response
        ai_msg = ChatMessage(session_id=session_id, role="assistant", content=answer)
        self.db.add(ai_msg)
        self.db.commit()

        return answer
