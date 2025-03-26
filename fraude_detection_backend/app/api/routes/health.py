from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {"status": "ok", "message": "CDC Fraud Detection API is running"}


@router.get("/health/db")
async def db_health_check(db: Session = Depends(get_db)):
    """
    Database health check endpoint.
    Tests the database connection is working properly.
    """
    try:
        # Execute a simple query to check DB connection
        db.execute("SELECT 1")
        return {"status": "ok", "message": "Database connection successful"}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}