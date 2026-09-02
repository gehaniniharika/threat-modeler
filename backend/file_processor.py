"""File processing utilities for extracting text from PDFs and Word documents"""

import PyPDF2
from docx import Document
from io import BytesIO
import os

async def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")

async def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from Word document"""
    try:
        doc = Document(BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

        # Also extract from tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text += cell.text + "\n"

        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to parse Word document: {str(e)}")

async def process_uploaded_file(filename: str, file_content: bytes) -> str:
    """Process uploaded file and extract text based on file type"""

    file_ext = os.path.splitext(filename)[1].lower()

    if file_ext == '.pdf':
        return await extract_text_from_pdf(file_content)
    elif file_ext in ['.docx', '.doc']:
        return await extract_text_from_docx(file_content)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}. Supported types: PDF, DOCX, DOC")

def validate_file(filename: str, file_size: int, max_size_mb: int = 10) -> bool:
    """Validate uploaded file"""
    max_size_bytes = max_size_mb * 1024 * 1024

    if file_size > max_size_bytes:
        raise ValueError(f"File size exceeds {max_size_mb}MB limit")

    file_ext = os.path.splitext(filename)[1].lower()
    allowed_extensions = ['.pdf', '.docx', '.doc']

    if file_ext not in allowed_extensions:
        raise ValueError(f"File type not allowed. Supported types: {', '.join(allowed_extensions)}")

    return True
