# app/services/extraction.py
from typing import Dict, Any
from .placeholder import PlaceholderExtractor
from ..core.config import settings

class ExtractionService:
    """
    Main extraction service that can use different extraction methods
    """
    def __init__(self):
        """
        Initialize extraction service based on current configuration
        """
        if settings.EXTRACTION_MODE == "placeholder":
            self.extractor = PlaceholderExtractor()
        else:
            # Future: Add actual extraction logic
            raise NotImplementedError("Actual extraction method not implemented")
    
    def extract_document_data(self, file_path: str) -> Dict[str, Any]:
        """
        Extract data from a given file
        
        :param file_path: Path to the file to extract data from
        :return: Extracted document data
        """
        return self.extractor.extract(file_path)