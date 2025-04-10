# app/api/routes/extract.py
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ...services.extraction import ExtractionService

router = APIRouter()

@router.post("/extract/")
async def extract_document(file_path: str):
    """
    Trigger text extraction for a specific file
    
    :param file_path: Path to the file to extract
    :return: Extracted document data
    """
    try:
        extractor = ExtractionService()
        extracted_data = extractor.extract_document_data(file_path)
        
        return {
            "status": "success",
            "extracted_data": extracted_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))