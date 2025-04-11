from typing import Dict, Any
from sqlalchemy.sql import func
from ..db.database import SessionLocal
from ..db.models import ExtractedClaim

class PlaceholderExtractor:
    
    def extract(self, file_path: str) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            # Return a random row to simulate "new extraction"
            claim = db.query(ExtractedClaim).order_by(func.random()).first()
            if not claim:
                return {"error": "No data found in extracted_claims"}

            return {
                "id": claim.id,
                "age": claim.age,
                "sex": claim.sex,
                "bmi": claim.bmi,
                "children": claim.children,
                "region": claim.region,
                "charges": claim.charges
            }
        finally:
            db.close()
