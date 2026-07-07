import os
import io
import docx
import fitz  # PyMuPDF
from fastapi import UploadFile

class DocumentParserService:
    """
    Service for parsing uploaded documents and extracting text.
    Supports PDF, DOCX, and TXT files.
    """

    @staticmethod
    async def extract_text(file: UploadFile) -> str:
        """
        Extract text from an uploaded file based on its content type or extension.
        """
        content = await file.read()
        filename = file.filename.lower() if file.filename else ""
        
        try:
            if filename.endswith('.pdf') or file.content_type == 'application/pdf':
                return DocumentParserService._parse_pdf(content)
            elif filename.endswith('.docx') or file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                return DocumentParserService._parse_docx(content)
            elif filename.endswith('.txt') or file.content_type == 'text/plain':
                return content.decode('utf-8', errors='ignore')
            else:
                raise ValueError(f"Unsupported file type for {filename}. Supported formats are PDF, DOCX, TXT.")
        finally:
            # Reset file pointer if someone else needs to read it later
            await file.seek(0)

    @staticmethod
    def _parse_pdf(content: bytes) -> str:
        """Extract text from PDF bytes using PyMuPDF."""
        text_parts = []
        try:
            # fitz.open(stream=..., filetype=...)
            doc = fitz.open(stream=content, filetype="pdf")
            for page in doc:
                text_parts.append(page.get_text())
            doc.close()
            return "\n".join(text_parts)
        except Exception as e:
            raise ValueError(f"Error parsing PDF: {e}")

    @staticmethod
    def _parse_docx(content: bytes) -> str:
        """Extract text from DOCX bytes using python-docx."""
        try:
            doc = docx.Document(io.BytesIO(content))
            return "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text])
        except Exception as e:
            raise ValueError(f"Error parsing DOCX: {e}")

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize extracted text (remove excessive whitespace, etc).
        """
        import re
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
