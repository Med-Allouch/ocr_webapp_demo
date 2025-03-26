import uuid
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.db.database import Base


class TreatmentReport(Base):
    __tablename__ = "treatment_reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identifiant_unique = Column(String, index=True)
    regime_assurance = Column(String)
    prenom_assure = Column(String)
    nom_assure = Column(String)
    adress_assure = Column(Text)
    code_postal_assure = Column(String)
    qualite_beneficiaire = Column(String)
    prenom_malade = Column(String)
    nom_malade = Column(String)
    date_naissance_malade = Column(String)
    n_tel_malade = Column(String)
    signature_assure = Column(String)
    diagramme_dentaire = Column(Text)
    consultation_table = Column(Text)
    prothese_table = Column(Text)
    
    # Original file info
    original_filename = Column(String)
    file_path = Column(String)
    
    # Fraud detection
    fraud_score = Column(Integer)
    fraud_flags = Column(Text)  # JSON serialized list of flags
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Processing status
    is_processed = Column(Boolean, default=False)
    processing_errors = Column(Text, nullable=True)
    