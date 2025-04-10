# app/api/routes/upload.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List
import os
from ...services.extraction import ExtractionService
from ...utils.file_handling import save_uploaded_file, validate_file_type

router = APIRouter()

@router.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Upload files and process them
    
    :param files: List of files to upload
    :return: Dictionary with upload details and extracted data
    """
    try:
        # Validate and process each file
        processed_files = []
        for file in files:
            # Validate file type
            if not validate_file_type(file):
                raise HTTPException(status_code=400, detail=f"Invalid file type: {file.filename}")
            
            # Save file
            file_path = await save_uploaded_file(file)
            
            # Extract data
            extractor = ExtractionService()
            extracted_data = extractor.extract_document_data(file_path)
            
            processed_files.append({
                "filename": file.filename,
                "saved_path": file_path,
                "extracted_data": extracted_data
            })
        
        return {
            "status": "success",
            "files": processed_files
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))