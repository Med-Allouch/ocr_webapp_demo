import os
import shutil
from pathlib import Path
from typing import List
from fastapi import UploadFile, HTTPException
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


async def validate_file_extension(file: UploadFile, allowed_extensions: List[str] = None) -> bool:
    """
    Validate file extension against allowed list.
    
    Args:
        file: The uploaded file
        allowed_extensions: List of allowed extensions (e.g., ['.jpg', '.png'])
        
    Returns:
        True if valid, False otherwise
    """
    if allowed_extensions is None:
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.tiff', '.bmp']
        
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        return False
    return True


async def validate_file_size(file: UploadFile, max_size: int = None) -> bool:
    """
    Validate file size against maximum allowed size.
    
    Args:
        file: The uploaded file
        max_size: Maximum allowed size in bytes
        
    Returns:
        True if valid, False otherwise
    """
    if max_size is None:
        max_size = settings.MAX_UPLOAD_SIZE
        
    # Read into memory to check size
    file_content = await file.read()
    file_size = len(file_content)
    
    # Reset file position for later use
    await file.seek(0)
    
    if file_size > max_size:
        return False
    return True


async def save_upload_file(upload_file: UploadFile, destination: str = None) -> Path:
    """
    Save an upload file to the specified destination.
    
    Args:
        upload_file: The uploaded file
        destination: Directory to save the file (defaults to settings.UPLOAD_DIRECTORY)
        
    Returns:
        Path to the saved file
    """
    if destination is None:
        destination = settings.UPLOAD_DIRECTORY
    
    try:
        os.makedirs(destination, exist_ok=True)
        
        # Create destination path with the original filename
        dest = Path(destination) / upload_file.filename
        
        with dest.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
            
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    finally:
        await upload_file.close()
        
    return dest