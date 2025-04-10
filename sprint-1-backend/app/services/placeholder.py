# app/services/placeholder.py
from typing import Dict, Any
import uuid
from datetime import datetime

class PlaceholderExtractor:
    """
    Placeholder extractor to simulate document data extraction
    """
    def extract(self, file_path: str) -> Dict[str, Any]:
        """
        Generate mock document data
        
        :param file_path: Path to the file (not used in placeholder)
        :return: Mock extracted data
        """
        return {
            "id": str(uuid.uuid4()),
            "identifiant_unique": f"DOC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "regime_assurance": "General Health Insurance",
            "prenom_assure": "Jean",
            "nom_assure": "Dupont",
            "adress_assure": "123 Rue de la République, Paris",
            "code_postal_assure": "75001",
            "qualite_beneficiaire": "Titular",
            "prenom_malade": "Marie",
            "nom_malade": "Dupont",
            "date_naissance_malade": "1985-03-15",
            "n_tel_malade": "+33612345678",
            "signature_assure": "JD_Signature_Mock"
        }