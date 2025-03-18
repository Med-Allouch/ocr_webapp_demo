from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi.encoders import jsonable_encoder

from app.db.models import TreatmentReport
from app.schemas.reports import TreatmentReportCreate


class ReportRepository:
    """Repository for treatment report database operations."""
    
    @staticmethod
    async def create(db: Session, report: TreatmentReportCreate, file_path: str, fraud_score: int, fraud_flags: List[str] = None) -> TreatmentReport:
        """Create a new treatment report."""
        report_data = jsonable_encoder(report)
        db_report = TreatmentReport(
            **report_data,
            file_path=file_path,
            fraud_score=fraud_score,
            fraud_flags=str(fraud_flags) if fraud_flags else None,
            is_processed=True,
        )
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        return db_report
    
    @staticmethod
    async def get_by_id(db: Session, report_id: UUID) -> Optional[TreatmentReport]:
        """Get a treatment report by ID."""
        return db.query(TreatmentReport).filter(TreatmentReport.id == report_id).first()
    
    @staticmethod
    async def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[TreatmentReport]:
        """Get all treatment reports with pagination."""
        return db.query(TreatmentReport).order_by(desc(TreatmentReport.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    async def count(db: Session) -> int:
        """Count total number of reports."""
        return db.query(TreatmentReport).count()
    
    @staticmethod
    async def update_processing_status(db: Session, report_id: UUID, is_processed: bool, errors: Optional[str] = None) -> TreatmentReport:
        """Update processing status of a report."""
        db_report = db.query(TreatmentReport).filter(TreatmentReport.id == report_id).first()
        if db_report:
            db_report.is_processed = is_processed
            db_report.processing_errors = errors
            db.commit()
            db.refresh(db_report)
        return db_report