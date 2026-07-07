import logging
from typing import List
from sqlalchemy.orm import Session
from backend.app.core.config import get_settings
from backend.app.embeddings.service import EmbeddingService
from backend.app.ai.llm_service import LLMService
from backend.app.rag.vector_store import FAISSStore
from backend.app.models.document import Document, DocumentChunk

settings = get_settings()
logger = logging.getLogger("ai_study_pal")

class RAGPipeline:
    def __init__(self, db: Session):
        self.db = db
        self.vector_store = FAISSStore()
        self.embedding_service = EmbeddingService()
        self.llm_service = LLMService()

    def _chunk_text(self, text: str, chunk_size: int = settings.CHUNK_SIZE, overlap: int = settings.CHUNK_OVERLAP) -> List[str]:
        """Simple overlap chunking mechanism."""
        if not text:
            return []
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            if end >= len(text):
                break
            start = end - overlap
        return chunks

    def index_document(self, document_id: int):
        """
        Chunks a document, saves chunks to DB, and indexes them in FAISS.
        """
        doc = self.db.query(Document).filter(Document.id == document_id).first()
        if not doc or not doc.content:
            logger.warning(f"Document {document_id} not found or empty.")
            return

        # Check if already chunked (simplified)
        existing_chunks = self.db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).first()
        if existing_chunks:
            logger.info(f"Document {document_id} is already chunked. Skipping indexing.")
            return

        # 1. Chunk text
        texts = self._chunk_text(doc.content)
        if not texts:
            return

        logger.info(f"Chunked Document {document_id} into {len(texts)} chunks.")

        # 2. Save chunks to DB
        db_chunks = []
        for i, chunk_text in enumerate(texts):
            db_chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=i,
                text=chunk_text
            )
            self.db.add(db_chunk)
            db_chunks.append(db_chunk)
            
        self.db.commit()
        for chunk in db_chunks:
            self.db.refresh(chunk)

        # 3. Generate embeddings
        # Batch generation can be done, but for safety with public APIs, we'll do smaller batches or all at once if small
        logger.info(f"Generating embeddings for Document {document_id}")
        embeddings = self.embedding_service.generate_embeddings(texts)

        # 4. Add to Vector Store
        chunk_ids = [c.id for c in db_chunks]
        self.vector_store.add_embeddings(embeddings, chunk_ids)
        logger.info(f"Successfully indexed Document {document_id} in FAISS.")

    def index_all_unindexed_documents(self):
        """Index all documents that don't have chunks yet."""
        docs = self.db.query(Document).all()
        for doc in docs:
            self.index_document(doc.id)

    def answer_question(self, query: str) -> str:
        """
        Answer a question using RAG.
        """
        # 1. Embed query
        query_embedding = self.embedding_service.generate_embedding(query)
        
        # 2. Retrieve top-k chunks from FAISS
        results = self.vector_store.search(query_embedding, top_k=settings.TOP_K_RETRIEVAL)
        if not results:
            return "I couldn't find any relevant information in your study materials."
            
        # 3. Fetch context text from DB
        context_texts = []
        for chunk_id, score in results:
            db_chunk = self.db.query(DocumentChunk).filter(DocumentChunk.id == chunk_id).first()
            if db_chunk:
                context_texts.append(db_chunk.text)
            
        context_str = "\n\n---\n\n".join(context_texts)
        
        # 4. Build prompt and generate answer
        prompt = (
            f"You are AI Study Pal, an intelligent tutor.\n"
            f"Use the following pieces of retrieved context to answer the question.\n"
            f"If you don't know the answer, just say that you don't know. Don't make up information.\n\n"
            f"Context:\n{context_str}\n\n"
            f"Question: {query}\n\n"
            f"Answer:"
        )
        
        logger.info(f"Generating answer for query: {query}")
        answer = self.llm_service.generate(prompt)
        return answer
