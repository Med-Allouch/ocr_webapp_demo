from typing import Optional, List, Any
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class TreatmentReportBase(BaseModel):
    """Base fields for treatment report."""
    identifiant_unique: Optional[str] = None
    regime_assurance: Optional[str] = None
    prenom_assure: Optional[str] = None
    nom_assure: Optional[str] = None
    adress_assure: Optional[str] = None
    code_postal_assure: Optional[str] = None
    qualite_beneficiaire: Optional[str] = None
    prenom_malade: Optional[str] = None
    nom_malade: Optional[str] = None
    date_naissance_malade: Optional[str] = None
    n_tel_malade: Optional[str] = None
    signature_assure: Optional[str] = None
    diagramme_dentaire: Optional[str] = None
    consultation_table: Optional[str] = None
    prothese_table: Optional[str] = None


class TreatmentReportCreate(TreatmentReportBase):
    """Data required to create a new treatment report."""
    original_filename: str


class TreatmentReportInDB(TreatmentReportBase):
    """Treatment report as stored in the database."""
    id: UUID
    fraud_score: int
    fraud_flags: Optional[List[str]] = []
    original_filename: str
    created_at: datetime
    updated_at: datetime
    is_processed: bool
    processing_errors: Optional[str] = None

    class Config:
        orm_mode = True


class TreatmentReportResponse(BaseModel):
    """Treatment report response for API."""
    id: UUID
    fraud_score: int
    extracted_fields: TreatmentReportBase
    created_at: datetime
    is_processed: bool
    fraud_flags: Optional[List[str]] = []

    class Config:
        orm_mode = True


class TreatmentReportList(BaseModel):
    """List of treatment reports."""
    id: UUID
    identifiant_unique: Optional[str] = None
    nom_assure: Optional[str] = None
    prenom_assure: Optional[str] = None
    fraud_score: int
    created_at: datetime
    is_processed: bool

    class Config:
        orm_mode = True


class TreatmentReportListResponse(BaseModel):
    """Response containing a list of treatment reports."""
    reports: List[TreatmentReportList]
    total: int
    page: int
    page_size: int
    pages: int