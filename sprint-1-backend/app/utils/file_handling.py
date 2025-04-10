# app/utils/file_handling.py
import os
import uuid
from fastapi import UploadFile, HTTPException
from ..core.config import settings

def validate_file_type(file: UploadFile) -> bool:
    """
    Validate file type based on allowed extensions
    
    :param file: Uploaded file
    :return: Boolean indicating if file type is allowed
    """
    file_extension = file.filename.split('.')[-1].lower()
    
    if file_extension not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed types are: {', '.join(settings.ALLOWED_FILE_TYPES)}"
        )
    
    return True

async def save_uploaded_file(file: UploadFile) -> str:
    """
    Save an uploaded file with a unique filename
    
    :param file: Uploaded file
    :return: Path to the saved file
    """
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Generate unique filename
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # Check file size
    file_content = await file.read()
    if len(file_content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE / (1024 * 1024)} MB"
        )
    
    # Save the file
    with open(file_path, "wb") as buffer:
        buffer.write(file_content)
    
    return file_path