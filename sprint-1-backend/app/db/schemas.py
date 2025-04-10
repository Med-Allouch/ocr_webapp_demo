# app/db/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class DocumentBase(BaseModel):
    """
    Base Pydantic model for document data
    """
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

class DocumentCreate(DocumentBase):
    """
    Model for creating a new document
    """
    pass

class DocumentResponse(DocumentBase):
    """
    Model for returning document data
    """
    id: UUID

    class Config:
        orm_mode = True