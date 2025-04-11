# test_db_read.py
from app.db.database import SessionLocal
from app.db.models import ExtractedClaim

db = SessionLocal()
try:
    claims = db.query(ExtractedClaim).all()
    for claim in claims:
        print(f"ID: {claim.id}, Age: {claim.age}, Charges: {claim.charges}")
finally:
    db.close()
