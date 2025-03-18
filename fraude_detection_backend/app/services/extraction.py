from datetime import datetime
import os
from typing import Dict, Any
from fastapi import UploadFile
import uuid
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class ExtractionService:
    """Service for extracting text from treatment report images."""
    
    @staticmethod
    async def save_file(file: UploadFile) -> str:
        """Save uploaded file and return the file path."""
        # Create a unique filename
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{file_id}{file_extension}"
        
        # Create the file path
        file_path = os.path.join(settings.UPLOAD_DIRECTORY, filename)
        
        # Write the file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return file_path
    
    @staticmethod
    async def extract_text_from_image(image_path: str) -> Dict[str, Any]:
        """
        Extract text from an image of a treatment report.
        
        This is currently a mock implementation. Replace with actual OCR model.
        """
        logger.info(f"Extracting text from {image_path}")
        
        # TODO: Replace this with your actual OCR model implementation
        # For now, this returns mock data
        return {
            "identifiant_unique": "13813928",
            "regime_assurance": "GENERAL",
            "prenom_assure": "Mohamed",
            "nom_assure": "Allouch",
            "adress_assure": "Sfax Manzel chekee km 3.5",
            "code_postal_assure": "3013",
            "qualite_beneficiaire": "Titulaire",
            "prenom_malade": "Ahmed",
            "nom_malade": "Lajmi",
            "date_naissance_malade": "01/01/2001",
            "n_tel_malade": "21 445 545",
            "signature_assure": "Present",
            "diagramme_dentaire": "Complete",
            "consultation_table": "Soins preventifs",
            "prothese_table": "Couronne ceramique"
        }
    
    @staticmethod
    async def cleanup_old_files(days_old: int = 7) -> None:
        """Delete files older than the specified number of days."""
        current_time = datetime.datetime.now()
        directory = settings.UPLOAD_DIRECTORY
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            # Check if it's a file (not a directory)
            if os.path.isfile(file_path):
                file_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if (current_time - file_modified_time).days > days_old:
                    try:
                        os.remove(file_path)
                        logger.info(f"Deleted old file: {file_path}")
                    except Exception as e:
                        logger.error(f"Error deleting file {file_path}: {e}")