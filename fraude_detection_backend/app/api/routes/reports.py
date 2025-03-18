import math
from typing import Optional
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Query
from sqlalchemy.orm import Session
import logging

from app.db.database import get_db
from app.db.repositories.reports import ReportRepository
from app.schemas.reports import (
    TreatmentReportCreate, 
    TreatmentReportResponse,
    TreatmentReportListResponse,
)
from app.services.extraction import ExtractionService
from app.services.fraud_detection import FraudDetectionService
from app.utils.file_handling import validate_file_extension, validate_file_size

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/reports/extract", response_model=TreatmentReportResponse)
async def extract_text(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a treatment report image, extract text, and analyze for fraud.
    
    - **file**: The treatment report image file
    """
    # Validate file
    if not await validate_file_extension(file):
        raise HTTPException(status_code=400, detail="Invalid file type. Allowed types: jpg, jpeg, png, pdf, tiff, bmp")
    
    if not await validate_file_size(file):
        raise HTTPException(status_code=400, detail="File too large")
    
    try:
        # Save the file
        file_path = await ExtractionService.save_file(file)
        
        # Extract text from the image
        extracted_data = await ExtractionService.extract_text_from_image(file_path)
        
        # Check for fraud
        fraud_score, fraud_flags = await FraudDetectionService.check_fraud(extracted_data)
        
        # Create report object
        report_create = TreatmentReportCreate(
            **extracted_data,
            original_filename=file.filename
        )
        
        # Save to database
        db_report = await ReportRepository.create(
            db=db, 
            report=report_create, 
            file_path=file_path,
            fraud_score=fraud_score, 
            fraud_flags=fraud_flags
        )
        
        # Return response
        return TreatmentReportResponse(
            id=db_report.id,
            fraud_score=db_report.fraud_score,
            extracted_fields={key: getattr(db_report, key) for key in extracted_data.keys()},
            created_at=db_report.created_at,
            is_processed=db_report.is_processed,
            fraud_flags=eval(db_report.fraud_flags) if db_report.fraud_flags else []
        )
        
    except Exception as e:
        logger.error(f"Error processing report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing report: {str(e)}")


@router.get("/reports/{report_id}", response_model=TreatmentReportResponse)
async def get_report(
    report_id: str,
    db: Session = Depends(get_db)
):
    """
    Get details of a specific report by ID.
    
    - **report_id**: UUID of the report
    """
    db_report = await ReportRepository.get_by_id(db=db, report_id=report_id)
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return TreatmentReportResponse(
        id=db_report.id,
        fraud_score=db_report.fraud_score,
        extracted_fields={
            key: getattr(db_report, key)
            for key in [
                "identifiant_unique", "regime_assurance", "prenom_assure", 
                "nom_assure", "adress_assure", "code_postal_assure", 
                "qualite_beneficiaire", "prenom_malade", "nom_malade", 
                "date_naissance_malade", "n_tel_malade", "signature_assure", 
                "diagramme_dentaire", "consultation_table", "prothese_table"
            ]
        },
        created_at=db_report.created_at,
        is_processed=db_report.is_processed,
        fraud_flags=eval(db_report.fraud_flags) if db_report.fraud_flags else []
    )


@router.get("/reports", response_model=TreatmentReportListResponse)
async def list_reports(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    List all processed reports with pagination.
    
    - **page**: Page number (starts at 1)
    - **page_size**: Number of items per page
    """
    # Calculate skip for pagination
    skip = (page - 1) * page_size
    
    # Get reports with pagination
    reports = await ReportRepository.get_all(db=db, skip=skip, limit=page_size)
    
    # Get total count
    total_reports = await ReportRepository.count(db=db)
    
    # Calculate total pages
    total_pages = math.ceil(total_reports / page_size)
    
    return TreatmentReportListResponse(
        reports=reports,
        total=total_reports,
        page=page,
        page_size=page_size,
        pages=total_pages
    )