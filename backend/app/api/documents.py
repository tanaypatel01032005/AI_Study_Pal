from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.document import Document
from backend.app.services.document_parser import DocumentParserService
from pydantic import BaseModel

router = APIRouter()

class DocumentResponse(BaseModel):
    id: int
    title: str
    subject: str | None
    word_count: int
    message: str

    class Config:
        from_attributes = True

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    subject: str = "General",
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a document, parse it, clean it, and store it in the database.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    # 1. Parse text from file
    try:
        raw_text = await DocumentParserService.extract_text(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract any text from the document.")

    # 2. Clean text
    clean_text = DocumentParserService.clean_text(raw_text)
    
    # Calculate simple metrics (later will be moved to AI processing)
    word_count = len(clean_text.split())
    sentence_count = clean_text.count('.') + clean_text.count('!') + clean_text.count('?')

    # 3. Store in DB
    title = file.filename
    new_doc = Document(
        title=title,
        subject=subject,
        content=clean_text,
        word_count=word_count,
        sentence_count=sentence_count
    )
    
    db.add(new_doc)
    try:
        db.commit()
        db.refresh(new_doc)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return DocumentResponse(
        id=new_doc.id,
        title=new_doc.title or "Untitled",
        subject=new_doc.subject,
        word_count=new_doc.word_count or 0,
        message="Document uploaded and processed successfully."
    )

class DocumentSummaryResponse(BaseModel):
    id: int
    summary: str

@router.get("/{doc_id}/summary", response_model=DocumentSummaryResponse, summary="Get or generate document summary")
def get_document_summary(doc_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the summary of a document. If it doesn't exist, generate it using the summarization model.
    """
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    if doc.summary:
        return {"id": doc.id, "summary": doc.summary}
        
    # Generate summary
    from backend.app.ai.llm_service import LLMService
    llm = LLMService()
    
    # Simple strategy: summarize the first 2000 chars to avoid exceeding context window
    # A robust strategy would chunk and map-reduce.
    text_to_summarize = doc.content[:2000]
    
    summary = llm.summarize(text_to_summarize)
    
    # Save to DB
    doc.summary = summary
    db.commit()
    
    return {"id": doc.id, "summary": doc.summary}
